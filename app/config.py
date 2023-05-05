from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url = 'carwashdevs:YbaPElydvXjLYoRzdVD23n91u0q3196W@dpg-cgbu2d5269v4ictdp800-a/carwashdb'

    class Config:
        env_file = ".env"


settings = Settings()
