# Pydantic Schemas for Booking Service
# Defines the shape of data coming IN and going OUT of the API

from pydantic import BaseModel

# Schema for creating a new booking
class BookingCreate(BaseModel):
    guest_id: int
    room_id: int
    check_in: str
    check_out: str
    status: str  # confirmed, pending, cancelled

# Schema for updating an existing booking
class BookingUpdate(BaseModel):
    guest_id: int
    room_id: int
    check_in: str
    check_out: str
    status: str

# Schema for returning booking data in API response
class BookingResponse(BaseModel):
    id: int
    guest_id: int
    room_id: int
    check_in: str
    check_out: str
    status: str

    # Allows Pydantic to read data from SQLAlchemy model
    class Config:
        from_attributes = True