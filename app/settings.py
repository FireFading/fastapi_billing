from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv(dotenv_path="../")


class Settings(BaseSettings):
    database_url: str = Field(env="DATABASE_URL")

    postgres_db: str = Field(env="POSTGRES_DB")
    postgres_host: str = Field(env="POSTGRES_HOST")
    postgres_user: str = Field(env="POSTGRES_USER")
    postgres_password: str = Field(env="POSTGRES_PASSWORD")

    class Config:
        env_file = "../.env.example"


class JWTSettings(BaseSettings):
    authjwt_secret_key: str = Field(env="AUTHJWT_SECRET_KEY")
    authjwt_header_type: str | None = Field(env="AUTH_HEADER_TYPE")
    authjwt_header_name: str = Field(env="AUTHJWT_HEADER_NAME")
    access_token_expires: int = Field(env="ACCESS_TOKEN_EXPIRES")
    refresh_token_expires: int = Field(env="REFRESH_TOKEN_EXPIRES")

    class Config:
        env_file = "../.env.example"
