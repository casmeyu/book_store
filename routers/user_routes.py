from models.user_model import User, Role
from schema.user_schema import PublicUserInfo, NewUser
from database.database import DB, Hasher
from fastapi import HTTPException, status, APIRouter
from datetime import datetime


def setupUserRoutes(db : DB):

    user_router = APIRouter(prefix = "/users")

    @user_router.get("/{user_id}", response_model=PublicUserInfo)
    async def get_user_by_id(user_id):
        #Gets a user by its id
        user = db.GetById(User, user_id)
        db.CloseSession()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn`t exists")
        public_user = PublicUserInfo.model_validate(user)
        return public_user

    @user_router.get("", response_model=list[PublicUserInfo])
    async def get_all_users():
        #Gets all users on db
        users = db.GetAll(User)
        publicUsers = [PublicUserInfo.model_validate(u) for u in users]
        return(publicUsers)

    @user_router.post("", response_model=PublicUserInfo, status_code=status.HTTP_201_CREATED)
    async def create_user(user : NewUser):
        #Create a new user and save it in the database
        #Check roles existance
        db_roles = db.session.query(Role).filter(Role.id.in_(user.roles)).all()
        if len(db_roles) != len(user.roles):
            fail_id = []
            for role_id in user.roles:
                if role_id not in [r.id for r in db_roles]:
                    fail_id.append(role_id)        
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Roles problem, the next roles do not exist: {fail_id}")

        # Check user existance
        if (db.session.query(User).where(User.username == user.username).first()):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already exists on database")

        #ver documentacion pydantic response model error
        hash_password = Hasher.get_hash_password(user.password)
        new_user = User(user.username, hash_password, str(datetime.now()), True)
        new_user.roles = db_roles
        db.Insert(new_user)
        db.CloseSession()
        publicUser = PublicUserInfo.model_validate(new_user)
        return(publicUser)
    
    return(user_router)