from fastapi import APIRouter, status, HTTPException
from database.database import DB
from schema.role_schema import RoleSchema
from models.user_model import Role



def setupRoleRoutes(db : DB):
    
    role_router = APIRouter(prefix= "roles")
    
    @role_router.post("", response_model=RoleSchema, status_code=status.HTTP_201_CREATED)
    async def create_role(role: RoleSchema):
        #Create a new role and save it in the database
        new_role = Role(role.name)
        db.Insert(new_role)
        db.CloseSession()
        return(new_role)
    
    return(role_router)