# ─────────────────────────────────────────────────────────────
# HOTEL SERVICE ROUTES (Controller Layer)
#
# This file ONLY handles HTTP concerns:
#   - Receiving requests
#   - Reading query parameters (e.g. ?city=Colombo)
#   - Calling the service layer for business logic
#   - Returning responses with correct status codes
#
# It does NOT contain any database queries or business logic.
# All of that lives in service.py.
#
# PATTERN:
#   Request → routes.py (HTTP) → service.py (logic) → Database
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
import service
from database import get_db

# Create API router instance
router = APIRouter()


# ─────────────────────────────────────────────────────────────
# HELPER: Consistent error responses
#
# Instead of each route having different error formats, we use
# one function so every error looks the same:
#   {
#     "error": "Hotel not found",
#     "status_code": 404,
#     "detail": "No hotel exists with ID 99"
#   }
#
# This makes it easier for other services (or frontends) to
# parse and handle errors consistently.
# ─────────────────────────────────────────────────────────────
def hotel_not_found(hotel_id: int):
    """Raise a consistent 404 error for a missing hotel"""
    raise HTTPException(
        status_code=404,
        detail={
            "error": "Hotel not found",
            "status_code": 404,
            "detail": f"No hotel exists with ID {hotel_id}",
        }
    )


# ─────────────────────────────────────────
# GET ALL HOTELS (with search, filter & pagination)
#
# Query parameters are defined as function arguments with defaults.
# FastAPI automatically reads them from the URL.
#
# Examples:
#   GET /hotels                        → all hotels, first 20
#   GET /hotels?city=Colombo           → hotels in Colombo
#   GET /hotels?search=Hilton&stars=5  → 5-star hotels with "Hilton" in name
#   GET /hotels?skip=20&limit=10       → page 3 (items 21-30)
# ─────────────────────────────────────────
@router.get("/hotels", response_model=List[schemas.HotelResponse])
def get_all_hotels(
    # Each of these becomes a ?key=value in the URL
    search: Optional[str] = Query(default=None, description="Search hotels by name"),
    city: Optional[str] = Query(default=None, description="Filter by city"),
    country: Optional[str] = Query(default=None, description="Filter by country"),
    stars: Optional[int] = Query(default=None, ge=1, le=5, description="Filter by star rating (1-5)"),
    min_rating: Optional[float] = Query(default=None, ge=0, le=5, description="Filter by minimum user rating"),
    is_active: Optional[bool] = Query(default=None, description="Filter by active status"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip (for pagination)"),
    limit: int = Query(default=20, ge=1, le=100, description="Max records to return (1-100)"),
    db: Session = Depends(get_db),
):
    """Get list of hotels with optional search, filters & pagination"""
    return service.get_all_hotels(
        db,
        search=search,
        city=city,
        country=country,
        stars=stars,
        min_rating=min_rating,
        is_active=is_active,
        skip=skip,
        limit=limit,
    )


# ─────────────────────────────────────────
# GET HOTEL BY ID
# ─────────────────────────────────────────
@router.get("/hotels/{hotel_id}", response_model=schemas.HotelResponse)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """Get a single hotel by its ID"""
    hotel = service.get_hotel_by_id(db, hotel_id)

    if not hotel:
        hotel_not_found(hotel_id)
    return hotel


# ─────────────────────────────────────────
# CREATE NEW HOTEL
# ─────────────────────────────────────────
@router.post("/hotels", response_model=schemas.HotelResponse, status_code=201)
def create_hotel(hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
    """Create a new hotel record"""
    return service.create_hotel(db, hotel)


# ─────────────────────────────────────────
# UPDATE HOTEL (full update — all fields required)
# ─────────────────────────────────────────
@router.put("/hotels/{hotel_id}", response_model=schemas.HotelResponse)
def update_hotel(hotel_id: int, updated: schemas.HotelUpdate, db: Session = Depends(get_db)):
    """Update an existing hotel by its ID"""
    hotel = service.get_hotel_by_id(db, hotel_id)
    if not hotel:
        hotel_not_found(hotel_id)

    return service.update_hotel(db, hotel, updated)


# ─────────────────────────────────────────
# PATCH HOTEL (partial update — only send fields you want to change)
#
# Difference between PUT and PATCH:
#   PUT   → "replace everything" (send ALL fields)
#   PATCH → "update some things" (send ONLY what changed)
#
# Example: PATCH /hotels/1  body: {"rating": 4.8}
#   → only updates rating, everything else stays the same
# ─────────────────────────────────────────
@router.patch("/hotels/{hotel_id}", response_model=schemas.HotelResponse)
def patch_hotel(hotel_id: int, updated: schemas.HotelUpdate, db: Session = Depends(get_db)):
    """Partially update a hotel — only send the fields you want to change"""
    hotel = service.get_hotel_by_id(db, hotel_id)
    if not hotel:
        hotel_not_found(hotel_id)

    return service.update_hotel(db, hotel, updated)


# ─────────────────────────────────────────
# DELETE HOTEL
# ─────────────────────────────────────────
@router.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """Delete a hotel by its ID"""
    hotel = service.get_hotel_by_id(db, hotel_id)
    if not hotel:
        hotel_not_found(hotel_id)

    service.delete_hotel(db, hotel)
    return {"message": f"Hotel with ID {hotel_id} deleted successfully"}
