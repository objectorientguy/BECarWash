from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url = 'postgresql://carwashdb_gv4e_user:8sv7IryuQE7R8yDfTNSHF97HqLATIgJD@dpg-cicnvmiip7vnjjl9ecmg-a.singapore-postgres.render.com/carwashdb_gv4e'

    class Config:
        env_file = ".env"


settings = Settings()
