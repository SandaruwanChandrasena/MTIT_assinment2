# Room Service Routes
# Contains all CRUD endpoints for Room management

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db

# Create API router instance
router = APIRouter()

# ─────────────────────────────────────────
# GET ALL ROOMS
# ─────────────────────────────────────────
@router.get("/rooms", response_model=List[schemas.RoomResponse])
def get_all_rooms(db: Session = Depends(get_db)):
    """Get list of all rooms"""
    rooms = db.query(models.Room).all()
    return rooms

# ─────────────────────────────────────────
# GET ROOM BY ID
# ─────────────────────────────────────────
@router.get("/rooms/{room_id}", response_model=schemas.RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    """Get a single room by its ID"""
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    
    # Return 404 if room not found
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

# ─────────────────────────────────────────
# CREATE NEW ROOM
# ─────────────────────────────────────────
@router.post("/rooms", response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    """Create a new room record"""
    # Convert schema to database model
    db_room = models.Room(**room.dict())
    
    db.add(db_room)      # Add to database
    db.commit()          # Save changes
    db.refresh(db_room)  # Refresh to get generated ID
    return db_room

# ─────────────────────────────────────────
# UPDATE ROOM
# ─────────────────────────────────────────
@router.put("/rooms/{room_id}", response_model=schemas.RoomResponse)
def update_room(room_id: int, updated: schemas.RoomUpdate, db: Session = Depends(get_db)):
    """Update an existing room by its ID"""
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    
    # Return 404 if room not found
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Update each field dynamically
    for key, value in updated.dict().items():
        setattr(room, key, value)
    
    db.commit()       # Save changes
    db.refresh(room)  # Refresh updated data
    return room

# ─────────────────────────────────────────
# DELETE ROOM
# ─────────────────────────────────────────
@router.delete("/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    """Delete a room by its ID"""
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    
    # Return 404 if room not found
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    db.delete(room)  # Delete from database
    db.commit()      # Save changes
    return {"message": f"Room with ID {room_id} deleted successfully"}