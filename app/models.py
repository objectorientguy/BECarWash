from sqlalchemy import Column, String, Boolean, BIGINT, ForeignKey, Date, Time,Float
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
    subscription_id = Column(BIGINT, ForeignKey(
        "book_subscription.subscription_id", ondelete="CASCADE"), nullable=True)
    booking_time = Column(Time, nullable=False)
    booking_date = Column(Date, nullable=False)
    services = Column(String, nullable=False)
    final_amount = Column(String, nullable=False)
    payment_mode = Column(String, nullable=False)
    employee = Column(String, nullable=True)
    
    payment_breakdown = Column(String, nullable=False)
    review = Column(BIGINT, nullable=True)
    feedback = Column(String, nullable=True)
    center_id = Column(BIGINT, nullable=False)
    coupons_applied = Column(String, nullable=True)
    coupon_discount = Column(String, nullable=True)

    customer = relationship("Authentication")
    address = relationship("Addresses")
    subscription = relationship("BookSubscription")

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
    favourite = Column(Boolean, default=False, nullable=False)

    @validates('center_name', 'center_address', 'center_ratings', 'center_details','favourite')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value


class CenterServices(Base):
    __tablename__ = "center_services"

    service_id = Column(BIGINT, nullable=False, primary_key=True)
    center_id = Column(BIGINT, ForeignKey(
        "centers.center_id", ondelete="CASCADE"), nullable=False)
    service_title = Column(String, nullable=False)
    service_cost = Column(BIGINT, nullable=False)
    service_discount = Column(BIGINT, nullable=False)
    service_details = Column(String, nullable=False)

    customer = relationship("Centers")

    @validates('service_title', 'service_cost', 'service_discount', 'service_details')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value

class PortalAuthenticate(Base):
    __tablename__ = "portal_user"
    portal_user_id = Column(BIGINT, nullable=False, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    login_created_at = Column(TIMESTAMP(timezone=True),
                              nullable=False, server_default=text('now()'))
    @validates('email', 'password', 'portal_user_id')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value
        


class BookSubscription(Base):
    __tablename__ = "book_subscription"
    subscription_id = Column(BIGINT, index=True, primary_key=True,nullable=False)
    customer_id = Column(BIGINT, nullable=False)
    subscribed_on = Column(Date, nullable=False)
    ends_on = Column(Date, nullable=False)
    num_bookings = Column(BIGINT, nullable=False)
    num_bookings_pending = Column(BIGINT, nullable=False)
    cost = Column(Float, nullable=False)

    @validates('customer_id', 'num_bookings', 'num_bookings_pending')
    def validate_BIGINT_values(self, key, value):
        if isinstance(value, int) and value < 0:
            raise ValueError(f"{key} must be a positive BIGINT")
        return value  

