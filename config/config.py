import os

class AppConfig:
    def __init__(self):
        self.name = os.getenv("APP_NAME")
        self.host = os.getenv("APP_HOST")
        self.port = int(os.getenv("APP_PORT")) if os.getenv("APP_PORT") else 3000

class DbConfig:
    def __init__(self):
        self.usr = os.getenv("DB_USERNAME")
        self.pwd = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT")) if os.getenv("DB_PORT") else 3306
        self.name = os.getenv("DB_NAME")


class Config:
    def __init__(self):
        self.AppConfig = AppConfig()
        self.DbConfig = DbConfig()