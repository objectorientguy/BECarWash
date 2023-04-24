from datetime import date
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, cast, Date
from . import models, schemas
from .database import engine, SessionLocal, get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def root():
    return {'message': 'hello world'}


@app.post('/authenticateUser')
def create_user(loginSignupAuth: schemas.LoginSignupAuth, response: Response, db: Session = Depends(get_db)):
    try:
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
                response.status_code = 200
                return {"status": "200", "message": "No user found", "data": {}}

        return {"status": "200", "message": "New user successfully Logged in!", "data": user_data}
    except IntegrityError as err:
        response.status_code = 200
        return {"status": "200", "message": "Error", "data": {}}


@app.get('/getUserDetails')
def get_user_details(response: Response, db: Session = Depends(get_db), id: Optional[int] = None):
    try:

        get_user = db.query(models.Authentication).filter(
            models.Authentication.customer_contact == id).all()

        if not get_user:
            response.status_code = 404
            return {"status": "404", "message": "No address found", "data": []}

        return {"status": "200", "message": "success", "data": get_user}
    except IntegrityError as err:
        response.status_code = 404
        return {"status": "404", "message": "Error", "data": {}}


@app.put('/editUser')
def edit_user(userDetail: schemas.UserData, response: Response, db: Session = Depends(get_db), id: Optional[str] = None):
    try:
        edit_uder_details = db.query(models.Authentication).filter(
            models.Authentication.customer_id == id)
        user_exist = edit_uder_details.first()
        if not user_exist:
            response.status_code = 404
            return {"status": "404", "message": "User doesn't exists", "data": {}}

        edit_uder_details.update(userDetail.dict(), synchronize_session=False)
        db.commit()
        return {"status": "200", "message": "user edited!", "data": edit_uder_details.first()}
    except IntegrityError as err:
        response.status_code = 404
        return {"status": "404", "message": "Error", "data": {}}


@app.post('/addAddress')
def add_address(createAddress: schemas.AddAddress, response: Response, db: Session = Depends(get_db)):
    try:
        new_address = models.Addresses(**createAddress.dict())
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        return {"status": "200", "message": "New address created!", "data": new_address}
    except IntegrityError as err:
        response.status_code = 404
        return {"status": "404", "message": "Error", "data": {}}


@app.get('/getAllAddresses')
def get_address(response: Response, db: Session = Depends(get_db), id: Optional[int] = None):
    try:
        user_addresses = db.query(models.Addresses).filter(
            models.Addresses.user_contact == id).all()

        if not user_addresses:
            response.status_code = 200
            return {"status": "200", "message": "No address found", "data": []}

        return {"status": "200", "message": "success", "data": user_addresses}
    except IntegrityError as err:
        response.status_code = 404
        return {"status": "404", "message": "Error", "data": {}}


@app.put('/editAddress')
def edit_address(editAddress: schemas.EditAddress, response: Response, db: Session = Depends(get_db),  id=int):
    try:
        edit_user_address = db.query(models.Addresses).filter(
            models.Addresses.address_id == id)
        address_exist = edit_user_address.first()
        if not address_exist:
            response.status_code = 200
            return {"status": "200", "message": "Address doesn't exists", "data": {}}

        edit_user_address.update(editAddress.dict(), synchronize_session=False)
        db.commit()
        return {"status": "200", "message": "address edited!", "data": edit_user_address}

    except IntegrityError as err:
        response.status_code = 404
        return {"status": "404", "message": "Error", "data": {}}


@app.delete('/deleteAddress')
def delete_user_address(response: Response, db: Session = Depends(get_db),  id=int):
    try:
        delete_address = db.query(models.Addresses).filter(
            models.Addresses.address_id == id)
        address_exist = delete_address.first()
        if not address_exist:
            response.status_code = 200
            return {"status": "200", "message": "Address doesn't exists", "data": {}}

        delete_address.delete(synchronize_session=False)
        db.commit()
        return {"status": "200", "message": "address edited!", "data": {}}
    except IntegrityError as err:
        response.status_code = 404
        return {"status": "404", "message": "Error", "data": {}}


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


@app.get('/getAllBookings', response_model=schemas.GetUserBookings)
def get_bookings(response: Response, db: Session = Depends(get_db), id: Optional[int] = None,
                 history: Optional[bool] = None):
    try:
        if history:
            user_history = db.query(models.Bookings).filter(
                models.Bookings.user_contact == id).order_by(models.Bookings.booking_date).all()
            return schemas.GetUserBookings(status=200, data=user_history, message="Booking data with customer and address no id")

        user_bookings = db.query(models.Bookings).filter(models.Bookings.user_contact == id).filter(
            models.Bookings.booking_date >= date.today().strftime('%d.%m.%Y')).order_by(
            models.Bookings.booking_time).all()

        return schemas.GetUserBookings(status=200, data=user_bookings, message="Booking data with customer and address no id")

    except IntegrityError as err:
        response.status_code = 404
        return {"status": "404", "message": "Error", "data": {}}


@app.delete('/deleteBooking')
def delete_booking(response: Response, db: Session = Depends(get_db),  id=int):
    try:
        delete_bookings = db.query(models.Bookings).filter(
            models.Bookings.booking_id == id)
        booking_exist = delete_bookings.first()
        if not booking_exist:
            response.status_code = 404
            return {"status": "404", "message": "Booking doesn't exists", "data": {}}

        delete_bookings.delete(synchronize_session=False)
        db.commit()
        return {"status": "200", "message": "booking delete!", "data": {}}
    except IntegrityError as err:
        response.status_code = 404
        return {"status": "404", "message": "Error", "data": {}}


@app.get('/getBookings', response_model=schemas.AllBookingData)
def portal_data(response: Response, db: Session = Depends(get_db), id: Optional[str] = None):
    try:
        if id:
            get_portal_data = db.query(models.Bookings).filter(
                models.Bookings.booking_date == id).all()
            return schemas.AllBookingData(status=200, data=get_portal_data, message="Booking data with customer and address with id")
        get_all_data = db.query(models.Bookings).all()
        return schemas.AllBookingData(status=200, data=get_all_data, message="Booking data with customer and address no id")
    except IntegrityError as err:
        response.status_code = 404
        return {"status": "404", "message": "Error", "data": {}}
