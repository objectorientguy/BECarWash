from fastapi import Body, FastAPI
from pydantic import BaseModel



app = FastAPI()
class AuthenticationModel(BaseModel):
    authId: int


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post('/authenticateUser')
def authenticate_user(authenticationModel:AuthenticationModel):
    print(authenticationModel)
    return {"message": "This API will authenticate user and send back user id, user contact, user membership type"}

@app.post('/editUserProfile')
def root():
    return {"message": "This API will help user to edit user profile"}

@app.get('/userCarWashHistory')
def root():
    return {"message": "This API will give user car wash history"}

@app.post('/bookCarWash')
def root():
    return {"message": "This API will book a single car wash"}

@app.post('/bookCarWashSubscriptionWise')
def root():
    return {"message": "This API will book a car wash in subscription mode"}

@app.get('/fetchNotification')
def root():
    return {"message": "This API will give user car wash history"}

@app.post('/addNewAddress')
def root():
    return {"message": "This API will book a single car wash"}

@app.get('/carWashedDetails')
def root():
    return {"message": "This API will give particular car washs details"}

