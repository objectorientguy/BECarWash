from fastapi import Body, FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
        try:
            conn = psycopg2.connect(host='localhost',database='carwash',user='postgres',password='Aditya123',cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print('Database connected successfully')
            break
        except Exception as error:
            print('Database connection failed because of - '+error)
            time.sleep(secs=2)

class AuthenticationModel(BaseModel):
    auth_id: int

class UserDataModel(BaseModel):
    user_name: str
    user_contact: int
    auth_id: str

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post('/createUser')
def create_user(userDataModel:UserDataModel):
    cursor.execute("""INSERT INTO users (user_name,user_contact,auth_id) VALUES (%s,%s,%s) RETURNING *""",(userDataModel.user_name,userDataModel.user_contact,userDataModel.auth_id))
    new_user_data = cursor.fetchone()
    conn.commit()
    return {"message": "New user successfully created","data":new_user_data}

@app.get("/getUser/{auth_id}")
def get_user_by_id(auth_id:int):
    cursor.execute("""SELECT * FROM users WHERE auth_id = 1""")
    fetched_user_data = cursor.fetchone()
    print(fetched_user_data)
    return {"message": "User successfully found","data":fetched_user_data}


@app.get("/getAllUser")
def root():
    cursor.execute("""SELECT * FROM users""")
    users = cursor.fetchall()
    return {"data": users}

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

