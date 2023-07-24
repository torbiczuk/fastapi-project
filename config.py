from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

    class Config:
        env_file = ".env"  # Load environment variables from a .env file
        env_file_encoding = "utf-8"


settings = Settings()
