# Hotel Service Routes
# Contains all CRUD endpoints for Hotel management

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db

# Create API router instance
router = APIRouter()

# ─────────────────────────────────────────
# GET ALL HOTELS
# ─────────────────────────────────────────
@router.get("/hotels", response_model=List[schemas.HotelResponse])
def get_all_hotels(db: Session = Depends(get_db)):
    """Get list of all hotels"""
    hotels = db.query(models.Hotel).all()
    return hotels

# ─────────────────────────────────────────
# GET HOTEL BY ID
# ─────────────────────────────────────────
@router.get("/hotels/{hotel_id}", response_model=schemas.HotelResponse)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """Get a single hotel by its ID"""
    hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    
    # Return 404 if hotel not found
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel

# ─────────────────────────────────────────
# CREATE NEW HOTEL
# ─────────────────────────────────────────
@router.post("/hotels", response_model=schemas.HotelResponse)
def create_hotel(hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
    """Create a new hotel record"""
    # Convert schema to database model
    db_hotel = models.Hotel(**hotel.dict())
    
    db.add(db_hotel)      # Add to database
    db.commit()           # Save changes
    db.refresh(db_hotel)  # Refresh to get generated ID
    return db_hotel

# ─────────────────────────────────────────
# UPDATE HOTEL
# ─────────────────────────────────────────
@router.put("/hotels/{hotel_id}", response_model=schemas.HotelResponse)
def update_hotel(hotel_id: int, updated: schemas.HotelUpdate, db: Session = Depends(get_db)):
    """Update an existing hotel by its ID"""
    hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    
    # Return 404 if hotel not found
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    # Update each field dynamically
    for key, value in updated.dict().items():
        setattr(hotel, key, value)
    
    db.commit()           # Save changes
    db.refresh(hotel)     # Refresh updated data
    return hotel

# ─────────────────────────────────────────
# DELETE HOTEL
# ─────────────────────────────────────────
@router.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """Delete a hotel by its ID"""
    hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    
    # Return 404 if hotel not found
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    db.delete(hotel)  # Delete from database
    db.commit()       # Save changes
    return {"message": f"Hotel with ID {hotel_id} deleted successfully"}