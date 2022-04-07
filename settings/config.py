from pydantic import BaseSettings

class Settings(BaseSettings):
    db_name: str
    db_user: str
    db_password: str
    db_port: int
    db_host: str

    class Config:
        env_file = ".env"

settings = Settings()