# Pydantic Schemas for Guest Service
# Defines the shape of data coming IN and going OUT of the API

from pydantic import BaseModel

# Schema for creating a new guest
class GuestCreate(BaseModel):
    name: str
    email: str
    phone: str
    nationality: str

# Schema for updating an existing guest
class GuestUpdate(BaseModel):
    name: str
    email: str
    phone: str
    nationality: str

# Schema for returning guest data in API response
class GuestResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    nationality: str

    # Allows Pydantic to read data from SQLAlchemy model
    class Config:
        from_attributes = True