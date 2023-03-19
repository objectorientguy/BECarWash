from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel, BaseSettings
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from .database import engine, SessionLocal, get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def get_message():
    return {'message': 'hello world'}


@app.post('/getUser')
def create_user(loginSignupAuth: schemas.LoginSignupAuth, response: Response, db: Session = Depends(get_db)):
    user_data = db.query(models.Authentication).get(
        loginSignupAuth.customer_contact)

    if not user_data:
        try:
            new_user_data = models.Authentication(
                **loginSignupAuth.dict())
            db.add(new_user_data)
            db.commit()
            db.refresh(new_user_data)
            return {"message": "New user successfully created!", "data": new_user_data}
        except IntegrityError as err:
            response.status_code = 404
            return {"message": "No user found"}

    return {"message": "New user successfully Logged in!", "data": user_data}
