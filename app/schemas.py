from typing import Optional, List
from pydantic import BaseModel


class UserData(BaseModel):
    customer_id: str
    customer_name: Optional[str]
    customer_contact: int
    is_new_customer: Optional[bool]

    class Config:
        orm_mode = True


class GetUserData(BaseModel):
    customer_id: str
    customer_name: Optional[str]
    is_new_customer: Optional[bool]

    class Config:
        orm_mode = True


class LoginSignupAuth(UserData):
    pass


class UpdateCustomer(UserData):
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


class AddAddress(Address):
    pass


class GetAddress(Address):
    customer: UserData

    class Config:
        orm_mode = True


class EditAddress(BaseModel):
    user_contact: int
    address_title: str
    address_name: str
    city: str
    pincode: int

    class Config:
        orm_mode = True


class ResponseData(BaseModel):
    status: int
    data: List[GetAddress]


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


class GetBooking(Bookings):
    customer: GetUserData
    address: Address

    class Config:
        orm_mode = True


class AllBookingData(BaseModel):
    status: int
    data: List[GetBooking]
    message: str


class GetBookingUser(Bookings):
    address: Address

    class Config:
        orm_mode = True


class GetUserBookings(BaseModel):
    status: int
    data: List[GetBookingUser]
    message: str

    class Config:
        orm_mode = True
