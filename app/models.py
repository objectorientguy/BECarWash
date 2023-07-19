from sqlalchemy import Column, String, Boolean, BIGINT, ForeignKey, Date, Time
from sqlalchemy.orm import validates, relationship
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime

from .database import Base


class Authentication(Base):
    __tablename__ = "customers"

    customer_id = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_contact = Column(BIGINT, primary_key=True, nullable=False)
    customer_birthdate = Column(Date, nullable=True)
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
    user_contact = Column(BIGINT, ForeignKey(
        "customers.customer_contact", ondelete="CASCADE"), nullable=False)
    address_title = Column(String, nullable=False)
    address_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    pincode = Column(BIGINT, nullable=False)

    customer = relationship(
        "Authentication")

    @validates('user_contact', 'address_title', 'address_name', 'city', 'pincode')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value


class Bookings(Base):
    __tablename__ = "bookings"

    booking_id = Column(BIGINT, nullable=False, primary_key=True)
    user_contact = Column(BIGINT, ForeignKey(
        "customers.customer_contact", ondelete="CASCADE"), nullable=False)
    address_id = Column(BIGINT, ForeignKey(
        "address.address_id", ondelete="CASCADE"), nullable=False)
    booking_time = Column(Time, nullable=False)
    booking_date = Column(Date, nullable=False)
    services = Column(String, nullable=False)
    final_amount = Column(String, nullable=False)
    payment_mode = Column(String, nullable=False)
    employee = Column(String, nullable=True)

    customer = relationship("Authentication")
    address = relationship("Addresses")

    @validates('user_contact', 'address_id', 'services', 'final_amount', 'payment_mode')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value


class Centers(Base):
    __tablename__ = "centers"

    center_id = Column(BIGINT, primary_key=True, nullable=False)
    center_name = Column(String, nullable=False)
    center_address = Column(String,  nullable=False)
    center_ratings = Column(BIGINT, nullable=True)
    center_details = Column(String, nullable=False)
    likes = Column(Boolean, nullable=False, server_default='FALSE')

    @validates('center_name', 'center_address', 'center_ratings', 'center_details')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value
