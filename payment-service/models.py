# SQLAlchemy Database Model for Payment
# This defines the actual table structure in SQLite

from sqlalchemy import Column, Integer, String, Float
from database import Base

class Payment(Base):
    # Table name in SQLite database
    __tablename__ = "payments"

    # Table columns
    id         = Column(Integer, primary_key=True, index=True)  # Auto increment ID
    booking_id = Column(Integer, nullable=False)                 # Reference to booking
    amount     = Column(Float, nullable=False)                   # Payment amount
    method     = Column(String, nullable=False)                  # cash, card, online
    status     = Column(String, nullable=False)                  # paid, pending, failed