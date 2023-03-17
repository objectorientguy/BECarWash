from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='carwash',
                                user='postgres', password='Mun1chad$', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connected successfully')
        break
    except Exception as error:
        print('Database connection failed because of - '+error)
        time.sleep(secs=2)


class CreateCustomerDataModel(BaseModel):
    customer_id: str
    customer_name: Optional[str]
    customer_contact: int
    is_new_customer: Optional[bool]


class LoginDataModel(BaseModel):
    customer_contact: int


class AuthenticatedUserDataModel(BaseModel):
    customer_id: str
    customer_name: str
    customer_contact: int
    is_new_customer: bool

    def __init__(self, customer_id, customer_name, customer_contact, is_new_customer):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_contact = customer_contact
        self.is_new_customer = is_new_customer


class UpdateUserDataModel(BaseModel):
    customer_name: str


class AddAddressDataModel(BaseModel):
    customer_contact: int
    address_details: str


class AddressesDataModel(BaseModel):
    address_id: int
    customer_contact: int
    address_details: str


@app.post('/getUser')
def create_user(createCustomerDataModel: CreateCustomerDataModel, response: Response):
    cursor.execute("""SELECT * FROM customers WHERE customer_contact = '%s'""",
                   ([createCustomerDataModel.customer_contact]))
    user_data = cursor.fetchone()

    if not user_data:
        try:
            cursor.execute("""INSERT INTO customers (customer_id,customer_name,customer_contact) VALUES (%s,%s,%s) RETURNING *""",
                           (createCustomerDataModel.customer_id, createCustomerDataModel.customer_name, createCustomerDataModel.customer_contact))
            new_user_data = cursor.fetchone()
            conn.commit()
            return {"message": "New user successfully created!", "data": new_user_data}
        except psycopg2.errors.NotNullViolation as err:
            response.status_code = 404
            return {"message": "No user found"}

    conn.commit()
    return {"message": "New user successfully Logged in!", "data": user_data}


@app.get("/authenticateUser/{customer_id}")
def fetched_user_data(customer_id: str):
    cursor.execute(
        """SELECT * FROM customers WHERE customer_id = %s""", (str(customer_id),))
    AuthenticatedUserDataModel = cursor.fetchone()
    return {"message": "User authenticated successfully!", "data": AuthenticatedUserDataModel}


@app.post('/updateUserData/{customer_id}')
def update_user_data(customer_id: int, userUpdateDataModel: UpdateUserDataModel):
    cursor.execute("""UPDATE customers SET customer_name = %s WHERE customer_id = %s RETURNING *""",
                   (userUpdateDataModel.customer_name, str(customer_id)))
    updated_user_data = cursor.fetchone()
    conn.commit()
    return {"message": "User details updated successfully!", "data": updated_user_data}


@app.post('/addAddress')
def add_address(addAddressDataModel: AddAddressDataModel):
    cursor.execute("""INSERT INTO address (customer_contact,address_details)VALUES (%s,%s) RETURNING *""",
                   (addAddressDataModel.customer_contact, addAddressDataModel.address_details))
    added_address_data = cursor.fetchone()
    conn.commit()
    return {"message": "New address added successfully!", "data": added_address_data}


@app.get('/getUsersAllAddresses/{customer_contact}')
def get_user_all_addresses(customer_contact: int):
    cursor.execute(
        """SELECT * FROM address WHERE customer_contact = %s""", (str(customer_contact),))
    AuthenticatedUserDataModel = [dict(item) for item in cursor.fetchall()]
    return {"message": "Address fetched successfully!", "data": AuthenticatedUserDataModel}
