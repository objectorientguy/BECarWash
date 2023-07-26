from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url = 'postgresql://postgres:Mun1chad$@localhost:5432/carwash'

    class Config:
        env_file = ".env"


settings = Settings()
