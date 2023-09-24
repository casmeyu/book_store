import uvicorn
from dotenv import load_dotenv

from config.config import Config
from server.server import createServer

load_dotenv()
server = createServer()


if __name__ == "__main__":
    config = Config()
    
    uvicorn.run(server, host=config.AppConfig.host, port=config.AppConfig.port)