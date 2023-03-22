from sqlalchemy import Column, String, Boolean, BIGINT
from sqlalchemy.orm import validates
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Authentication(Base):
    __tablename__ = "customers"

    customer_id = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_contact = Column(BIGINT, primary_key=True, nullable=False)
    is_new_customer = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    @validates('customer_name')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value


class Addresses(Base):
    __tablename__ = "address"

    address_id = Column(BIGINT, nullable=False, primary_key=True)
    user_contact = Column(BIGINT, nullable=False)
    address_title = Column(String, nullable=False)
    address_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    pincode = Column(BIGINT, nullable=False)

    @validates('user_contact', 'address_title', 'address_name', 'city', 'pincode')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value


class Bookings(Base):
    __tablename__ = "bookings"

    booking_id = Column(BIGINT, nullable=False, primary_key=True)
    user_contact = Column(BIGINT, nullable=False)
    address_id = Column(BIGINT, nullable=False)
    booking_time = Column(String, nullable=False)
    booking_date = Column(String, nullable=False)
    services = Column(String, nullable=False)
    final_amount = Column(String, nullable=False)
    payment_mode = Column(String, nullable=False)

    @validates('user_contact', 'address_id', 'booking_time', 'booking_date', 'services', 'final_amount', 'payment_mode')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value
