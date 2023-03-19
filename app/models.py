from sqlalchemy import Column, String, Boolean, BIGINT
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
