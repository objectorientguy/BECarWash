from typing import Optional
from pydantic import BaseModel


class UserData(BaseModel):
    customer_id: str
    customer_name: Optional[str]
    customer_contact: int
    is_new_customer: Optional[bool]


class LoginSignupAuth(UserData):
    pass


class Address(BaseModel):
    address_id: Optional[int]
    user_contact: int
    address_title: str
    address_name: str
    city: str
    pincode: int

    class Config:
        orm_mode = True


class addAddress(Address):
    pass


class Bookings(BaseModel):
    booking_id: Optional[int]
    user_contact: int
    address_id: int
    booking_time: str
    booking_date: str
    services: str
    final_amount: str
    payment_mode: str

    class Config:
        orm_mode = True
