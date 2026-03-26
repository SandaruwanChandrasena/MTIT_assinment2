# Pydantic Schemas for Payment Service
# Defines the shape of data coming IN and going OUT of the API

from pydantic import BaseModel

# Schema for creating a new payment
class PaymentCreate(BaseModel):
    booking_id: int
    amount: float
    method: str   # cash, card, online
    status: str   # paid, pending, failed

# Schema for updating an existing payment
class PaymentUpdate(BaseModel):
    booking_id: int
    amount: float
    method: str
    status: str

# Schema for returning payment data in API response
class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    amount: float
    method: str
    status: str

    # Allows Pydantic to read data from SQLAlchemy model
    class Config:
        from_attributes = True