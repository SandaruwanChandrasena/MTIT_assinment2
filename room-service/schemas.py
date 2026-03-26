# Pydantic Schemas for Room Service
# Defines the shape of data coming IN and going OUT of the API

from pydantic import BaseModel

# Schema for creating a new room
class RoomCreate(BaseModel):
    hotel_id: int
    room_type: str
    price_per_night: float
    is_available: bool

# Schema for updating an existing room
class RoomUpdate(BaseModel):
    hotel_id: int
    room_type: str
    price_per_night: float
    is_available: bool

# Schema for returning room data in API response
class RoomResponse(BaseModel):
    id: int
    hotel_id: int
    room_type: str
    price_per_night: float
    is_available: bool

    # Allows Pydantic to read data from SQLAlchemy model
    class Config:
        from_attributes = True