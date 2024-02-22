import uvicorn
from dotenv import load_dotenv
from config.config import Config
from server.server import Server
from routers.routes import setupServerRoutes


load_dotenv()


def main():
    config = Config()
    server = Server(config)
    setupServerRoutes(server, config)
    uvicorn.run(server.app, host=config.AppConfig.host, port=config.AppConfig.port)

if __name__ == "__main__":
    main()