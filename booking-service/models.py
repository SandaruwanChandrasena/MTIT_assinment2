# SQLAlchemy Database Model for Booking
# This defines the actual table structure in SQLite

from sqlalchemy import Column, Integer, String
from database import Base

class Booking(Base):
    # Table name in SQLite database
    __tablename__ = "bookings"

    # Table columns
    id        = Column(Integer, primary_key=True, index=True)  # Auto increment ID
    guest_id  = Column(Integer, nullable=False)                 # Reference to guest
    room_id   = Column(Integer, nullable=False)                 # Reference to room
    check_in  = Column(String, nullable=False)                  # Check-in date
    check_out = Column(String, nullable=False)                  # Check-out date
    status    = Column(String, nullable=False)                  # confirmed/pending/cancelled