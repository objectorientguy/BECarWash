from pydantic import BaseSettings

import urllib.parse

class Settings(BaseSettings):
    password = 'sakshishukla@2335'
    encoded_password = urllib.parse.quote(password)
    db_url = 'postgresql://postgres:{encoded_password}@localhost:5432/fastapi'
    # db_url = 'postgresql://carwashdb_gv4e_user:8sv7IryuQE7R8yDfTNSHF97HqLATIgJD@dpg-cicnvmiip7vnjjl9ecmg-a.singapore-postgres.render.com/carwashdb_gv4e'

    class Config:
        env_file = ".env"


settings = Settings()
