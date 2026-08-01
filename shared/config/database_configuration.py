
from pydantic_settings import BaseSettings
from functools import lru_cache

class DatabaseConfiguration(BaseSettings):

    host: str
    port: str
    database_name: str
    username: str
    password: str

    model_config = {
        "extra": "ignore",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "env_prefix": "DATABASE_"
    }

    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"
    #     env_prefix = "DATABASE_"

@lru_cache
def get_database_configuration() -> DatabaseConfiguration:
    return DatabaseConfiguration()