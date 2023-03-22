from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from .database import engine, SessionLocal, get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def root():
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
            return {"status": "200", "message": "New user successfully created!", "data": new_user_data}
        except IntegrityError as err:
            response.status_code = 404
            return {"status": "404", "message": "No user found", "data": {}}

    return {"status": "200", "message": "New user successfully Logged in!", "data": user_data}


@app.post('/addAddress')
def add_address(createAddress: schemas.Address, response: Response, db: Session = Depends(get_db)):
    try:
        new_address = models.Addresses(**createAddress.dict())
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        return {"status": "200", "message": "New address created!", "data": new_address}
    except IntegrityError as err:
        response.status_code = 404
        return {"status": "404", "message": "Error", "data": {}}


@app.get('/getAddress/address_id={id}')
def get_address(response: Response, db: Session = Depends(get_db), id=int):
    user_address = db.query(models.Addresses).get(id)

    if not user_address:
        response.status_code = 404
        return {"status": "404", "message": "No address found", "data": {}}

    return {"status": "200", "message": "success", "data": user_address}


@app.post('/addBooking')
def create_booking(addBookings: schemas.Bookings, response: Response, db: Session = Depends(get_db)):
    try:
        new_booking = models.Bookings(**addBookings.dict())
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        return {"status": "200", "message": "New address created!", "data": new_booking}
    except IntegrityError as err:
        response.status_code = 404
        return {"status": "404", "message": "Error", "data": {}}


@app.get('/getbooking/booking_id={id}')
def get_address(response: Response, db: Session = Depends(get_db), id=int):
    booking = db.query(models.Bookings).get(id)

    if not booking:
        response.status_code = 404
        return {"status": "404", "message": "No address found", "data": {}}

    return {"status": "200", "message": "success", "data": booking}
