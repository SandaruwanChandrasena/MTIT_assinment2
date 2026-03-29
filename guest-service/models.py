# SQLAlchemy Database Model for Guest
# This defines the actual table structure in SQLite

from sqlalchemy import Column, Integer, String
from database import Base

class Guest(Base):
    # Table name in SQLite database
    __tablename__ = "guests"

    # Table columns
    id          = Column(Integer, primary_key=True, index=True)  # Auto increment ID
    name        = Column(String, nullable=False)                  # Guest full name
    email       = Column(String, nullable=False)                  # Guest email
    phone       = Column(String, nullable=False)                  # Guest phone number
    nationality = Column(String, nullable=False)                  # Guest nationality