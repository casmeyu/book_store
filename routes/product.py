from fastapi import APIRouter
from config.config import Config, DbConfig
from database.database import Open, Close

productr = APIRouter

config = Config()
conn = Open(config.DbConfig)

