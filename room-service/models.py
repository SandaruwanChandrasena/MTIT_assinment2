# SQLAlchemy Database Model for Room
# This defines the actual table structure in SQLite

from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Room(Base):
    # Table name in SQLite database
    __tablename__ = "rooms"

    # Table columns
    id              = Column(Integer, primary_key=True, index=True)  # Auto increment ID
    hotel_id        = Column(Integer, nullable=False)                 # Reference to hotel
    room_type       = Column(String, nullable=False)                  # Single, Double, Suite
    price_per_night = Column(Float, nullable=False)                   # Price per night
    is_available    = Column(Boolean, default=True)                   # Availability status