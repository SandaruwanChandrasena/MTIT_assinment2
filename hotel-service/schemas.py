# Pydantic Schemas for Hotel Service
# Defines the shape of data coming IN and going OUT of the API

from pydantic import BaseModel

# Schema for creating a new hotel (no ID needed - DB generates it)
class HotelCreate(BaseModel):
    name: str
    location: str
    rating: float
    amenities: str

# Schema for updating an existing hotel
class HotelUpdate(BaseModel):
    name: str
    location: str
    rating: float
    amenities: str

# Schema for returning hotel data in API response (includes ID)
class HotelResponse(BaseModel):
    id: int
    name: str
    location: str
    rating: float
    amenities: str

    # Allows Pydantic to read data from SQLAlchemy model
    class Config:
        from_attributes = True