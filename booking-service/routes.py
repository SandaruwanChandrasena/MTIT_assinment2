# Booking Service Routes
# Contains all CRUD endpoints for Booking management

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db

# Create API router instance
router = APIRouter()

# ─────────────────────────────────────────
# GET ALL BOOKINGS
# ─────────────────────────────────────────
@router.get("/bookings", response_model=List[schemas.BookingResponse])
def get_all_bookings(db: Session = Depends(get_db)):
    """Get list of all bookings"""
    bookings = db.query(models.Booking).all()
    return bookings

# ─────────────────────────────────────────
# GET BOOKING BY ID
# ─────────────────────────────────────────
@router.get("/bookings/{booking_id}", response_model=schemas.BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get a single booking by its ID"""
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    
    # Return 404 if booking not found
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

# ─────────────────────────────────────────
# CREATE NEW BOOKING
# ─────────────────────────────────────────
@router.post("/bookings", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking record"""
    # Convert schema to database model
    db_booking = models.Booking(**booking.dict())
    
    db.add(db_booking)      # Add to database
    db.commit()             # Save changes
    db.refresh(db_booking)  # Refresh to get generated ID
    return db_booking

# ─────────────────────────────────────────
# UPDATE BOOKING
# ─────────────────────────────────────────
@router.put("/bookings/{booking_id}", response_model=schemas.BookingResponse)
def update_booking(booking_id: int, updated: schemas.BookingUpdate, db: Session = Depends(get_db)):
    """Update an existing booking by its ID"""
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    
    # Return 404 if booking not found
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Update each field dynamically
    for key, value in updated.dict().items():
        setattr(booking, key, value)
    
    db.commit()          # Save changes
    db.refresh(booking)  # Refresh updated data
    return booking

# ─────────────────────────────────────────
# DELETE BOOKING
# ─────────────────────────────────────────
@router.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """Delete a booking by its ID"""
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    
    # Return 404 if booking not found
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    db.delete(booking)  # Delete from database
    db.commit()         # Save changes
    return {"message": f"Booking with ID {booking_id} deleted successfully"}