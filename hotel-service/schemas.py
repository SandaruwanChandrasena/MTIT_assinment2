# ─────────────────────────────────────────────────────────────
# PYDANTIC SCHEMAS FOR HOTEL SERVICE
#
# Schemas define the SHAPE and RULES for data coming IN and going OUT.
# Think of them as bouncers at a club — they check if the data
# meets the requirements before letting it through.
#
# Pydantic automatically returns a 422 error with a clear message
# if any validation rule fails. You don't need to write error handling.
#
# We have 3 schemas:
#   - HotelCreate  → what the client sends when CREATING a hotel
#   - HotelUpdate  → what the client sends when UPDATING a hotel
#   - HotelResponse → what we send BACK to the client
# ─────────────────────────────────────────────────────────────

from pydantic import BaseModel, Field, EmailStr
from typing import Optional


# ─────────────────────────────────────────────────────────────
# CREATE SCHEMA
# Used for: POST /hotels
# All fields without "Optional" are REQUIRED when creating a new hotel.
#
# Field() lets us add validation rules:
#   - min_length = can't be empty
#   - max_length = can't be absurdly long
#   - ge (greater or equal) / le (less or equal) = number range
#   - examples = shows up in the Swagger docs as example values
# ─────────────────────────────────────────────────────────────
class HotelCreate(BaseModel):
    # ── Required fields (must be provided) ──
    name: str = Field(
        min_length=1,
        max_length=100,
        examples=["Grand Hyatt"],
        description="Hotel name (1-100 characters)"
    )
    description: str = Field(
        min_length=1,
        max_length=1000,
        examples=["A luxury 5-star hotel with ocean views and world-class dining"],
        description="Short description of the hotel"
    )
    address: str = Field(
        min_length=1,
        max_length=300,
        examples=["123 Galle Face Road"],
        description="Full street address"
    )
    city: str = Field(
        min_length=1,
        max_length=100,
        examples=["Colombo"],
        description="City where the hotel is located"
    )
    country: str = Field(
        min_length=1,
        max_length=100,
        examples=["Sri Lanka"],
        description="Country where the hotel is located"
    )
    phone: str = Field(
        min_length=7,
        max_length=20,
        examples=["+94 11 234 5678"],
        description="Contact phone number"
    )
    email: str = Field(
        min_length=5,
        max_length=100,
        examples=["info@grandhyatt.com"],
        description="Contact email address"
    )
    stars: int = Field(
        ge=1,
        le=5,
        examples=[5],
        description="Star classification (1-5). This is the official hotel class, not user reviews"
    )
    price_per_night: float = Field(
        gt=0,
        examples=[150.00],
        description="Base price per night in USD (must be greater than 0)"
    )
    amenities: str = Field(
        min_length=1,
        max_length=500,
        examples=["WiFi, Pool, Gym, Spa, Restaurant, Bar"],
        description="Comma-separated list of amenities"
    )

    # ── Optional fields (have default values) ──
    rating: Optional[float] = Field(
        default=0.0,
        ge=0.0,
        le=5.0,
        examples=[4.5],
        description="Average user rating from 0.0 to 5.0 (defaults to 0 for new hotels)"
    )
    image_url: Optional[str] = Field(
        default=None,
        max_length=500,
        examples=["https://example.com/hotel-photo.jpg"],
        description="URL to hotel photo (optional)"
    )
    is_active: Optional[bool] = Field(
        default=True,
        examples=[True],
        description="Whether the hotel is currently accepting bookings (defaults to True)"
    )


# ─────────────────────────────────────────────────────────────
# UPDATE SCHEMA
# Used for: PUT /hotels/{id}
#
# ALL fields are Optional — client only sends what they want to change.
# e.g. {"rating": 4.8} will only update the rating.
# Same validation rules apply to any field that IS sent.
# ─────────────────────────────────────────────────────────────
class HotelUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None, min_length=1, max_length=100,
        description="Hotel name (1-100 characters)"
    )
    description: Optional[str] = Field(
        default=None, min_length=1, max_length=1000,
        description="Short description of the hotel"
    )
    address: Optional[str] = Field(
        default=None, min_length=1, max_length=300,
        description="Full street address"
    )
    city: Optional[str] = Field(
        default=None, min_length=1, max_length=100,
        description="City where the hotel is located"
    )
    country: Optional[str] = Field(
        default=None, min_length=1, max_length=100,
        description="Country where the hotel is located"
    )
    phone: Optional[str] = Field(
        default=None, min_length=7, max_length=20,
        description="Contact phone number"
    )
    email: Optional[str] = Field(
        default=None, min_length=5, max_length=100,
        description="Contact email address"
    )
    stars: Optional[int] = Field(
        default=None, ge=1, le=5,
        description="Star classification (1-5)"
    )
    price_per_night: Optional[float] = Field(
        default=None, gt=0,
        description="Base price per night in USD"
    )
    amenities: Optional[str] = Field(
        default=None, min_length=1, max_length=500,
        description="Comma-separated list of amenities"
    )
    rating: Optional[float] = Field(
        default=None, ge=0.0, le=5.0,
        description="Average user rating from 0.0 to 5.0"
    )
    image_url: Optional[str] = Field(
        default=None, max_length=500,
        description="URL to hotel photo"
    )
    is_active: Optional[bool] = Field(
        default=None,
        description="Whether the hotel is currently accepting bookings"
    )


# ─────────────────────────────────────────────────────────────
# RESPONSE SCHEMA
# Used for: ALL responses that return hotel data
#
# This is what the client sees. Includes "id" which the DB generates.
#
# "from_attributes = True" tells Pydantic:
#   "The data I'm getting is a SQLAlchemy object (not a dict),
#    so read its attributes like hotel.name instead of hotel['name']"
# ─────────────────────────────────────────────────────────────
class HotelResponse(BaseModel):
    id: int
    name: str
    description: str
    address: str
    city: str
    country: str
    phone: str
    email: str
    stars: int
    price_per_night: float
    amenities: str
    rating: float
    image_url: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True
