import os 
from pydantic import BaseSettings
from pydantic.main import BaseModel

class DB(BaseModel):
    id : str = "root"
    password : str = ""
    url : str = ""
    name : str = ""
    port : int = 5000
    
db = DB()

class Config(BaseSettings):
    DEBUG : bool = True
    APP_HOST : str = "0.0.0.0"
    APP_PORT : int = 5000
    DB_URL: str = f"mysql+pymysql://{db.id}:{db.password}@{db.url}:{db.port}/{db.name}"
    JWT_SECRET_KEY: str = None
    JWT_ALGORITHM : str ="HS256"
    CLOVA_API_KEY_ID_NAME : str = None
    CLOVA_API_KEY_ID: str = None
    CLOVA_API_KEY_NAME: str = None
    CLOVA_API_KEY: str = None
    
def get_config():
    config_type = {
        "production" : Config(),
    }
    return config_type['production']

config = get_config()