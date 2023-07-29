from datetime import date,timedelta,datetime
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, Query, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
import requests
from typing import Dict
import firebase_admin
from firebase_admin import credentials, storage
from fastapi.responses import JSONResponse
import shutil
import time
import firebase_admin
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, cast, Date
from . import models, schemas
from sqlalchemy import desc
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

   # code to connect database
while True:
    try:
      conn =psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='sakshishukla@2335',cursor_factory=RealDictCursor) 
      cursor = conn.cursor()
      print("Database connection was successful!!")
      break
    except Exception as error:   
        print("connection to database failed!!")
        print("Error:",error)
        time.sleep(2)




@app.post('/authenticateUser')
def create_user(loginSignupAuth: schemas.LoginSignupAuth, response: Response, db: Session = Depends(get_db)):
    try:
        user_data = db.query(models.Authentication).get(
            loginSignupAuth.customer_contact)

        if not user_data:
            try:
                new_portal_user = models.Authentication(
                    **loginSignupAuth.dict())
                db.add(new_portal_user)
                db.commit()
                db.refresh(new_portal_user)
                return {"status": 200, "message": "New user successfully created!", "data": new_portal_user}
            except IntegrityError as err:
                response.status_code = 200
                return {"status": 404, "message": "User is Not Registered please Singup", "data": {}}

        return {"status": 200, "message": "New user successfully Logged in!", "data": user_data}
    except IntegrityError as err:
        response.status_code = 404
        return {"status": 404, "message": "Error", "data": {}}


@app.get('/getUserDetails')
def get_user_details(response: Response, db: Session = Depends(get_db), id: Optional[int] = None):
    try:

        get_user = db.query(models.Authentication).filter(
            models.Authentication.customer_contact == id).all()

        if not get_user:
            response.status_code = 404
            return {"status": 404, "message": "No address found", "data": []}

        return {"status": 200, "message": "success", "data": get_user}
    except IntegrityError as err:
        response.status_code = 404
        return {"status": 404, "message": "Error", "data": {}}


@app.put('/editUser')
def edit_user(userDetail: schemas.UserData, response: Response, db: Session = Depends(get_db), id: Optional[str] = None):
    try:
        edit_uder_details = db.query(models.Authentication).filter(
            models.Authentication.customer_id == id)
        user_exist = edit_uder_details.first()
        if not user_exist:
            response.status_code = 404
            return {"status": 404, "message": "User doesn't exists", "data": {}}

        edit_uder_details.update(userDetail.dict(), synchronize_session=False)
        db.commit()
        return {"status": 200, "message": "user edited!", "data": edit_uder_details.first()}
    except IntegrityError as err:
        response.status_code = 404
        return {"status": 404, "message": "Error", "data": {}}


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
def edit_address(editAddress: schemas.EditAddress, response: Response, db: Session = Depends(get_db), id: Optional[int] = None):
    try:
        edit_user_address = db.query(models.Addresses).filter(
            models.Addresses.address_id == id)
        address_exist = edit_user_address.first()
        if not address_exist:
            response.status_code = 200
            return {"status": 404, "message": "Address doesn't exists", "data": {}}

        edit_user_address.update(editAddress.dict(
            exclude_unset=True), synchronize_session=False)
        db.commit()
        return {"status": "200", "message": "address edited!", "data": edit_user_address.first()}

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
        return {"status": "200", "message": "address deleted!", "data": {}}
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
        return {"status": "200", "message": "New Booking created!", "data": new_booking}
    except IntegrityError as err:
        response.status_code = 404
        return {"status": "404", "message": "Error", "data": {}}


@app.get('/getAllBookings', response_model=schemas.GetUserBookings)
def get_bookings(response: Response, db: Session = Depends(get_db), id: Optional[int] = None,
                 history: Optional[bool] = None):
    try:
        if history:
            user_history = db.query(models.Bookings).filter(
                models.Bookings.user_contact == id).order_by(desc(models.Bookings.booking_id)).all()
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
            response.status_code = 200
            return {"status": 404, "message": "Booking doesn't exists", "data": {}}

        delete_bookings.delete(synchronize_session=False)
        db.commit()
        return {"status": 200, "message": "booking delete!", "data": {}}
    except IntegrityError as err:
        response.status_code = 404
        return {"status": 404, "message": "Error", "data": {}}


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


@app.put('/editBookings')
def edit_booking(bookingDetails: schemas.EditBookings, response: Response, db: Session = Depends(get_db), id: Optional[int] = None):
    try:
        edit_booking_details = db.query(models.Bookings).filter(
            models.Bookings.booking_id == id)
        booking_exist = edit_booking_details.first()
        if not booking_exist:
            response.status_code = 200
            return {"status": 404, "message": "Booking doesn't exists", "data": {}}

        edit_booking_details.update(
            bookingDetails.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
        return {"status": 200, "message": "Booking edited!", "data": edit_booking_details.first()}
    except IntegrityError as err:
        response.status_code = 404
        return {"status": 404, "message": "Error", "data": {}}



@app.post('/authenticatePortal')
def create_portal_user(portalLoginSignup: schemas.PortalAuthentication, response: Response, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(models.PortalAuthenticate).filter_by(email=portalLoginSignup.email).first()

        if existing_user:
            if existing_user.password == portalLoginSignup.password:
                return {"status": 200, "message": "Portal user successfully logged in!", "data": existing_user}
            else:
                return {"status": 401, "message": "invalid password."}

        try:
            new_portal_user_ = models.PortalAuthenticate(**portalLoginSignup.dict())
            db.add(new_portal_user_)
            db.commit() 
            db.refresh(new_portal_user_)
            return {"status": 200, "message": "New Portal user successfully created!", "data": new_portal_user_}

        except IntegrityError as err:
            response.status_code = 200
            return {"status": 401, "message": "Please login."}

    except IntegrityError as err:
        response.status_code = 500
        return {"status": 500, "message": "Error", "data": {}}
    


@app.get('/subscriptionInfo')
def get_subscription_info(user_id: int = Query(..., description="User ID"), db: Session = Depends(get_db)):
    user = db.query(models.BookSubscription).filter_by(customer_id=user_id).first()

    if user:
        subscription_info = get_user_subscription_info(user, db)
        return {"status": 200, "message": "Subscription information retrieved successfully!", "data": subscription_info}

    return {"status": 404, "message": "No subscription for this id", "data": {}}

def get_user_subscription_info(user: models.BookSubscription, db: Session):
    subscription = db.query(models.BookSubscription).filter_by(customer_id=user.customer_id).first()

    print(f"Subscription: {subscription}")  # Check if subscription object is retrieved

    if subscription:
        pending_washes = subscription.num_bookings_pending
        last_booking_date = calculate_last_booking_date(subscription.subscribed_on, subscription.num_bookings)

        print(f"Pending Washes: {pending_washes}")
        print(f"Last Booking Date: {last_booking_date}")

        subscription_info = {
            "customer_id": subscription.customer_id,
            "subscribed_on": subscription.subscribed_on,
            "ends_on": subscription.ends_on,
            "num_bookings": subscription.num_bookings,
            "num_bookings_pending": subscription.num_bookings_pending,
            "cost": subscription.cost,
            "pending_washes": pending_washes
        }
        print(f"Subscription Info: {subscription_info}")
        return subscription_info
    return {}

def calculate_last_booking_date(subscribed_on: datetime, num_bookings: int):
    last_booking_date = subscribed_on + timedelta(days=num_bookings)
    return last_booking_date 


#deleting subscription

@app.delete('/subscriptionInfo')
def delete_subscription_info(user_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        subscription = db.query(models.BookSubscription).filter_by(customer_id=user_id).first()

        if not subscription:
            response.status_code = 404
            return {"status": 404, "message": "Subscription not found.", "data": {}}

        db.delete(subscription)
        db.commit()

        return {"status": 200, "message": "Subscription deleted successfully!", "data": {}}

    except IntegrityError as err:
        response.status_code = 500
        return {"status": 500, "message": "Error", "data": {}}
    
  
def get_booking_by_id(db: Session, booking_id: int):
    return db.query(models.Bookings).filter(models.Bookings.booking_id == booking_id).first()

#check booking subscription 
@app.get("/booking_subscription_info/")
def booking_subscription_info(booking_id: int = Query(..., description="The ID of the booking"), db: Session = Depends(get_db)):
    booking = get_booking_by_id(db, booking_id)

    if not booking:
        return {
            "status": 400,
            "message": "Booking not found for this id",
            "data": {}
        }

    booking_data = {k: v for k, v in booking.__dict__.items() if not k.startswith('_')}
    booking_data.pop("subscription_id", None)

    subscription_data = None
    message = "Booking is not associated with subscription"

    if booking.subscription_id is not None:
        subscription_data = {
            "subscription_id": booking.subscription.subscription_id,
            "customer_id": booking.subscription.customer_id,
            "subscribed_on": booking.subscription.subscribed_on,
            "ends_on": booking.subscription.ends_on,
            "num_bookings": booking.subscription.num_bookings,
            "num_bookings_pending": booking.subscription.num_bookings_pending,
            "cost": booking.subscription.cost,
        }
        message = "Booking is associated with subscription"

    return {
        "status": 200,
        "message": message,
        "data": {
            "booking": booking_data,
            "subscription": subscription_data,
        }
    }


cred = credentials.Certificate("app/carwash-b9a26-firebase-adminsdk-x8l5f-f18978c5a4.json")
firebase_admin.initialize_app(cred, {"storageBucket": "carwash-b9a26.appspot.com"})

app = FastAPI()

def save_upload_file(upload_file: UploadFile, destination: str):
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

@app.post("/upload_images/")
async def upload_images(upload_files: List[UploadFile] = File(...)):
    image_urls = []
    for upload_file in upload_files:
        destination = os.path.join("app", "uploaded_images", upload_file.filename)
        save_upload_file(upload_file, destination)

        bucket = storage.bucket()
        blob = bucket.blob(f"uploaded_images/{upload_file.filename}")
        blob.upload_from_filename(destination)

        image_url = blob.generate_signed_url(method="GET", expiration=timedelta(days=7))
        image_urls.append(image_url)

    response_data = {
        "status": 200,
        "message": "Images uploaded successfully.",
        "data": {"image_urls": image_urls}
    }

    return JSONResponse(content=response_data)
