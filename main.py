from typing import Optional
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

class UserDataModel(BaseModel):
    user_name: str
    user_contact: int
    oauth: Optional [int]

class UserUpdateDataModel(BaseModel):
    user_name: str


@app.post('/createUser')
def create_user(userDataModel:UserDataModel):
    cursor.execute("""INSERT INTO users (user_name,user_contact,oauth) VALUES (%s,%s,%s) RETURNING *""",(userDataModel.user_name,userDataModel.user_contact,userDataModel.oauth))
    new_user_data = cursor.fetchone()
    conn.commit()
    return {"message": "New user successfully created!","data":new_user_data}

@app.get("/authenticateUser/{oauth}")
def fetched_user_data(oauth:int):
    cursor.execute("""SELECT * FROM users WHERE oauth = %s""",(str(oauth),))
    updated_user_data = cursor.fetchone()
    return {"message": "User exsists!","data":updated_user_data}

@app.post('/updateUserData/{user_id}')
def edit_user_data(user_id:int,userUpdateDataModel:UserUpdateDataModel):
    cursor.execute("""UPDATE users SET user_name = %s WHERE user_id = %s RETURNING *""",(userUpdateDataModel.user_name,str(user_id)))
    updated_user_data = cursor.fetchone()
    conn.commit()
    return {"message": "This API will help user to edit user profile"}



