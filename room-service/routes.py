# ─────────────────────────────────────────────────────────────
# ROOM SERVICE ROUTES
#
# INTER-SERVICE COMMUNICATION:
#   When creating a room, this service calls Hotel Service
#   to verify that the hotel_id actually exists.
#   This is how microservices validate data across services.
#
#   Room Service ──HTTP call──> Hotel Service (port 8001)
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import httpx
import models
import schemas
from database import get_db

router = APIRouter()

# URL of the Hotel Service (for inter-service communication)
HOTEL_SERVICE_URL = "http://localhost:8001"


# ─────────────────────────────────────────────────────────────
# HELPER: Verify a hotel exists by calling Hotel Service
#
# This is INTER-SERVICE COMMUNICATION in action.
# Instead of querying the hotels database directly (which would
# break microservices isolation), we make an HTTP request to
# the Hotel Service and ask it "does this hotel exist?"
# ─────────────────────────────────────────────────────────────
def verify_hotel_exists(hotel_id: int):
    try:
        response = httpx.get(f"{HOTEL_SERVICE_URL}/hotels/{hotel_id}")
        if response.status_code == 404:
            raise HTTPException(
                status_code=400,
                detail=f"Hotel with ID {hotel_id} does not exist. Cannot create room for non-existent hotel."
            )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Hotel Service is unavailable. Cannot verify hotel exists."
        )


# ─────────────────────────────────────────
# GET ALL ROOMS
# ─────────────────────────────────────────
@router.get("/rooms", response_model=List[schemas.RoomResponse])
def get_all_rooms(db: Session = Depends(get_db)):
    """Get list of all rooms"""
    return db.query(models.Room).all()


# ─────────────────────────────────────────
# GET ROOM BY ID
# ─────────────────────────────────────────
@router.get("/rooms/{room_id}", response_model=schemas.RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    """Get a single room by its ID"""
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


# ─────────────────────────────────────────
# CREATE NEW ROOM
# Now validates that the hotel exists first!
# ─────────────────────────────────────────
@router.post("/rooms", response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    """Create a new room — verifies hotel exists via Hotel Service"""

    # INTER-SERVICE CALL: Check if the hotel exists
    verify_hotel_exists(room.hotel_id)

    db_room = models.Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


# ─────────────────────────────────────────
# UPDATE ROOM
# ─────────────────────────────────────────
@router.put("/rooms/{room_id}", response_model=schemas.RoomResponse)
def update_room(room_id: int, updated: schemas.RoomUpdate, db: Session = Depends(get_db)):
    """Update an existing room by its ID"""
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    for key, value in updated.dict().items():
        setattr(room, key, value)

    db.commit()
    db.refresh(room)
    return room


# ─────────────────────────────────────────
# DELETE ROOM
# ─────────────────────────────────────────
@router.delete("/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    """Delete a room by its ID"""
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    db.delete(room)
    db.commit()
    return {"message": f"Room with ID {room_id} deleted successfully"}
