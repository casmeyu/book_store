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
APP_NAME="MyApp"				# string
APP_HOST="127.0.0.1"			# string
APP_PORT=3000					# int

DB_USERNAME="db_user"			# string
DB_PASSWORD="db_user_password"	# string
DB_HOST="127.0.0.1"				# string
DB_PORT=3306					# int
DB_NAME="db_name_to_connect"	# string
```

## Modules
### Config
The config module provides the `Config` class that is in charge of mantaining a single configuration accross the project.
This `Config` class contains the necessary information to establish a database connection and the FastAPI app configuration.
The value of the `Config` attributes is fetched from the `.env` file.

#### Config class structure
```json
{
	"AppConfig": {
		"name" : string,
		"host" : string,
		"port" : int
	},
	"DbConfig": {
		"usr"  : string,
		"pwd"  : string,
		"host" : string,
		"port" : int,
		"name" : name
	}
}
```

### Database
The database module provides a `DB` class that is an abstraction that uses the `SQLAlchemy` library to establish connections and sessions to the database.
The `DB` class must be initialized with a `Config` in order to establish the parameters that are used to connect to the database.
This class also provides basic functions like `Insert`, `GetAll` and `GetById` that can be used by any of the `SQLAlchemy` models.

#### Example of Config instantiation
```python
from config.config import Config

config = Config()
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