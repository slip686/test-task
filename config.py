from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class DBConfig(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    name: str

    class Config:
        env_prefix = "DB_"

    @property
    def dsn(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    db: DBConfig


settings = Settings(db=DBConfig())


class Config:
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', settings.db.dsn)
    DEBUG = True
    PORT = 5000
    RESTFUL_JSON = {'ensure_ascii': False}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
