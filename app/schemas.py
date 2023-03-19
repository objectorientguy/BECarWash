from typing import Optional
from pydantic import BaseModel


class UserData(BaseModel):
    customer_id: str
    customer_name: Optional[str]
    customer_contact: int
    is_new_customer: Optional[bool]


class LoginSignupAuth(UserData):
    pass
