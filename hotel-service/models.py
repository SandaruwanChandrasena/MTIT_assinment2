# SQLAlchemy Database Model for Hotel
# This defines the actual table structure in SQLite

from sqlalchemy import Column, Integer, String, Float
from database import Base

class Hotel(Base):
    # Table name in SQLite database
    __tablename__ = "hotels"

    # Table columns
    id        = Column(Integer, primary_key=True, index=True)  # Auto increment ID
    name      = Column(String, nullable=False)                  # Hotel name
    location  = Column(String, nullable=False)                  # Hotel location
    rating    = Column(Float, nullable=False)                   # Hotel rating (e.g 4.5)
    amenities = Column(String, nullable=False)                  # Hotel amenities