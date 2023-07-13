from typing import Optional, List
from pydantic import BaseModel
from datetime import date, time


class UserData(BaseModel):
    customer_id: str
    customer_name: Optional[str]
    customer_contact: int
    customer_birthdate: Optional[date]
    is_new_customer: Optional[bool]

    class Config:
        orm_mode = True


class GetUserData(BaseModel):
    customer_id: str
    customer_name: Optional[str]
    customer_birthdate: Optional[date]
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


class Bookings(BaseModel):
    booking_id: Optional[int]
    user_contact: int
    address_id: int
    booking_time: time
    booking_date: date
    services: str
    final_amount: str
    payment_mode: str
    employee: Optional[str]

    class Config:
        orm_mode = True


class EditBookings(BaseModel):
    user_contact: int
    address_id: int
    booking_time: time
    booking_date: date
    services: str
    final_amount: str
    payment_mode: str
    employee: Optional[str]

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


class Center(BaseModel):
    center_id: Optional[int]
    center_name: str
    center_address: str
    center_ratings: int
    center_details: str

    class Config:
        orm_mode = True


class EditCenter(BaseModel):
    center_name: str
    center_address: str
    center_ratings: int
    center_details: str

    class Config:
        orm_mode = True


class AllCenters(BaseModel):
    status: int
    data: List[Center]
    message: str

    class Config:
        orm_mode = True


class AddServices(BaseModel):
    service_id: Optional[int]
    center_id: int
    service_title: str
    service_cost: int
    service_discount: int
    service_details: str

    class Config:
        orm_mode = True


class Services(BaseModel):
    service_id: Optional[int]
    service_title: str
    service_cost: int
    service_discount: int
    service_details: str

    class Config:
        orm_mode = True


class EditServices(BaseModel):
    service_title: str
    service_cost: int
    service_discount: int
    service_details: str

    class Config:
        orm_mode = True


class AllCenterServices(BaseModel):
    status: int
    data: List[Services]
    message: str

    class Config:
        orm_mode = True
