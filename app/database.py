from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = 'postgresql://carwashdb_gv4e_user:8sv7IryuQE7R8yDfTNSHF97HqLATIgJD@dpg-cicnvmiip7vnjjl9ecmg-a.singapore-postgres.render.com/carwashdb_gv4e'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
