# Book Store inventory
## Description

## Requirements
	- python 3.10
	- mySQL service running

## Used libraries
	- [fastAPI](https://fastapi.tiangolo.com)
	- [SQLAlchemy](https://www.sqlalchemy.org)

## Running the app
Install necessary dependencies
`pip install -r requirements`

Run the app in the terminal
`python main.py`

## Enviroment variables
A `.env` file with the following variables is needed to run the project.
```
APP_NAME="MyApp"                # string
APP_HOST="127.0.0.1"            # string
APP_PORT=3000                   # int

DB_USERNAME="db_user"           # string
DB_PASSWORD="db_user_password"  # string
DB_HOST="127.0.0.1"             # string
DB_PORT=3306                    # int
DB_NAME="db_name_to_connect"    # string
```

## Modules
### Config
The config module provides the `Config` class that is in charge of mantaining a single configuration accross the project.
This `Config` class contains the necessary information to establish a database connection and the FastAPI app configuration separated in two attributes `Config.DbConfig` and `Config.AppConfig`.
The value of the `Config` attributes is fetched from the `.env` file.

#### Config class structure
```python
{
  "AppConfig": {
    "name" : str,
    "host" : str,
    "port" : int
  },
  "DbConfig": {
    "usr"  : str,
    "pwd"  : str,
    "host" : str,
    "port" : int,
    "name" : str
  }
}
```

#### Config instantiation
```python
from config.config import Config

config = Config()
```

### Database
The database module provides a `DB` class that is an abstraction that uses the `SQLAlchemy` library to establish connections and sessions to the database.
The `DB` class must be initialized with a `DbConfig` in order to establish the parameters that are used to connect to the database.
This class also provides basic functions like `Insert`, `GetAll` and `GetById` that can be used by any of the `SQLAlchemy` models.

#### DB instantiation
```python
from config.config import Config
from database.database import DB

config = Config()
db = DB(config.DbConfig)
```

#### Functions
`DB` class provides some basic functions to interact with `SQLAlchemy` models.
In this examples we will use an example model to demonstrate the function executions.

##### Example model
```python
from database.database import Base

class ExampleModel(Base):
    __tablename__ = "example_model"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)

    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description

    def __rpr__(self):
        return f"<ExampleModel id={self.id}, name="{self.name}">
```

##### Insert
Insert expects an instance of an `SQLAlchemy` model and a `boolean` argument that `commits` the insertion to the database when set to `True`, otherwise it will just `flush` the insertion.
This functions returns the newly inserted element.

```python
from config.config import Config
from database.database import DB

config = Config()
db = DB(config.DbConfig)

new_insert = ExampleModel("my example")
db.Insert(new_insert)
print(new_insert) #<ExampleModel id=1, name="my example">
```

#### GetById
GetById expects a `SQLAlchemy` model and an `id` value. It returns an entrie from the database or `None`.

```python
from config.config import Config
from database.database import DB

config = Config()
db = DB(config.DbConfig)

by_id = db.GetById(ExampleModel, 1)
print(by_id) #<ExampleModel id=1, name="my example">
```

#### GetAll
GetAll expects a `SQLAlchemy` model and an returns a `list` containing all the entries for said model.

```python
from config.config import Config
from database.database import DB

config = Config()
db = DB(config.DbConfig)

all_examples = db.GetAll(ExampleModel)
print(all_examples) #[<ExampleModel id=1, name="my example">]
```

### Server
The server module provides a `Server` class that contains an instance of `DB` class and the `FastAPI` app.
The `Server` class is a wrapper to have both the database connection and the `FastAPI` app in one place.

The `Server` class must be initialized with a `Config` in order to create the database connection and start the app.
After that it also needs to be passed to the `setupServerRoutes` function to add all the endpoints.

#### Example of Server instantiation
```python
from config.config import Config
from server.server import Server
from routes.routes import setupServerRoutes

config = Config()
server = Server(config)
setupServerRoutes(server, config)
```

## Endpoints
As of now all the endpoints are public and there is no need to login.

**For the examples we will assume that the server is running in `127.0.0.1:3000`.**

### Users
#### [GET] /users
This endpoints return a `list` containing the `PublicUserInfo` for each user in the data base.
```bash
curl GET '127.0.0.1:3000/users'
# Response
[
  {
    "username":"user01",
    "is_active":true
  },
  {
    "username":"user02",
    "is_active":true
  }
]
```

#### [GET] /users/<id>
This endpoints return a `json` containing the `PublicUserInfo` for the requested user.
If the user does not exist a `404 HttpException` will be raised.
```bash
curl GET '127.0.0.1:3000/users/1'
# Response
{
  "username":"user01",
  "is_active":true
}
```

#### [POST] /users
This endpoints creates a new user and stores it in the database and it will return the `PublicUserInfo` for the new user.
The endpoints expects a `json` containing a `NewUser` pydantic shcema.
If the username is already taken a `409 HttpException` will be raised.

```bash
curl POST '127.0.0.1:3000/users' \
--header 'Content-Type: application/json' \
--data '{
    "username":"newUser",
    "password":"password",
    "roles": [
        1
    ]
}'
# Response
{
  "username":"newUser",
  "is_active":true
}
```