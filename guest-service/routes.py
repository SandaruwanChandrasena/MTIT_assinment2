# Guest Service Routes
# Contains all CRUD endpoints for Guest management

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db

# Create API router instance
router = APIRouter()

# ─────────────────────────────────────────
# GET ALL GUESTS
# ─────────────────────────────────────────
@router.get("/guests", response_model=List[schemas.GuestResponse])
def get_all_guests(db: Session = Depends(get_db)):
    """Get list of all guests"""
    guests = db.query(models.Guest).all()
    return guests

# ─────────────────────────────────────────
# GET GUEST BY ID
# ─────────────────────────────────────────
@router.get("/guests/{guest_id}", response_model=schemas.GuestResponse)
def get_guest(guest_id: int, db: Session = Depends(get_db)):
    """Get a single guest by their ID"""
    guest = db.query(models.Guest).filter(models.Guest.id == guest_id).first()
    
    # Return 404 if guest not found
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest

# ─────────────────────────────────────────
# CREATE NEW GUEST
# ─────────────────────────────────────────
@router.post("/guests", response_model=schemas.GuestResponse)
def create_guest(guest: schemas.GuestCreate, db: Session = Depends(get_db)):
    """Create a new guest record"""
    # Convert schema to database model
    db_guest = models.Guest(**guest.dict())
    
    db.add(db_guest)      # Add to database
    db.commit()           # Save changes
    db.refresh(db_guest)  # Refresh to get generated ID
    return db_guest

# ─────────────────────────────────────────
# UPDATE GUEST
# ─────────────────────────────────────────
@router.put("/guests/{guest_id}", response_model=schemas.GuestResponse)
def update_guest(guest_id: int, updated: schemas.GuestUpdate, db: Session = Depends(get_db)):
    """Update an existing guest by their ID"""
    guest = db.query(models.Guest).filter(models.Guest.id == guest_id).first()
    
    # Return 404 if guest not found
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    
    # Update each field dynamically
    for key, value in updated.dict().items():
        setattr(guest, key, value)
    
    db.commit()        # Save changes
    db.refresh(guest)  # Refresh updated data
    return guest

# ─────────────────────────────────────────
# DELETE GUEST
# ─────────────────────────────────────────
@router.delete("/guests/{guest_id}")
def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    """Delete a guest by their ID"""
    guest = db.query(models.Guest).filter(models.Guest.id == guest_id).first()
    
    # Return 404 if guest not found
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    
    db.delete(guest)  # Delete from database
    db.commit()       # Save changes
    return {"message": f"Guest with ID {guest_id} deleted successfully"}