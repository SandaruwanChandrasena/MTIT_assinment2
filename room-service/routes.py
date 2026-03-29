# ─────────────────────────────────────────────────────────────
# ROOM SERVICE ROUTES (Controller Layer)
# Handles HTTP only — all logic lives in service.py
# PATTERN: Request → routes.py (HTTP) → service.py (logic) → DB
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import httpx
import schemas
import service
from database import get_db

router = APIRouter()

HOTEL_SERVICE_URL = "http://localhost:8001"


def room_not_found(room_id: int):
    raise HTTPException(status_code=404, detail=f"Room with ID {room_id} not found")


def verify_hotel_exists(hotel_id: int):
    try:
        response = httpx.get(f"{HOTEL_SERVICE_URL}/hotels/{hotel_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=400,
                detail=f"Hotel with ID {hotel_id} does not exist.")
    except httpx.ConnectError:
        raise HTTPException(status_code=503,
            detail="Hotel Service is unavailable.")


# ─────────────────────────────────────────
# GET ALL ROOMS (with filter & pagination)
#
# Examples:
#   GET /rooms                              → all rooms
#   GET /rooms?hotel_id=1                   → rooms in hotel 1
#   GET /rooms?room_type=Suite              → only suites
#   GET /rooms?is_available=true            → available only
#   GET /rooms?min_price=50&max_price=200   → by price range
#   GET /rooms?skip=0&limit=20             → pagination
# ─────────────────────────────────────────
@router.get("/rooms", response_model=List[schemas.RoomResponse])
def get_all_rooms(
    hotel_id:     Optional[int]   = Query(default=None, description="Filter by hotel ID"),
    room_type:    Optional[str]   = Query(default=None, description="Filter by room type (e.g. Suite, Double)"),
    is_available: Optional[bool]  = Query(default=None, description="Filter by availability"),
    min_price:    Optional[float] = Query(default=None, ge=0, description="Minimum price per night"),
    max_price:    Optional[float] = Query(default=None, ge=0, description="Maximum price per night"),
    skip:  int = Query(default=0,  ge=0,  description="Records to skip (pagination)"),
    limit: int = Query(default=20, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    """Get rooms with optional filters and pagination"""
    return service.get_all_rooms(
        db,
        hotel_id=hotel_id,
        room_type=room_type,
        is_available=is_available,
        min_price=min_price,
        max_price=max_price,
        skip=skip,
        limit=limit,
    )


@router.get("/rooms/{room_id}", response_model=schemas.RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    """Get a single room by its ID"""
    room = service.get_room_by_id(db, room_id)
    if not room:
        room_not_found(room_id)
    return room


@router.post("/rooms", response_model=schemas.RoomResponse, status_code=201)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    """Create a new room — verifies hotel exists via Hotel Service"""
    verify_hotel_exists(room.hotel_id)
    return service.create_room(db, room)


@router.put("/rooms/{room_id}", response_model=schemas.RoomResponse)
def update_room(room_id: int, updated: schemas.RoomUpdate, db: Session = Depends(get_db)):
    """Update an existing room by its ID"""
    room = service.get_room_by_id(db, room_id)
    if not room:
        room_not_found(room_id)
    return service.update_room(db, room, updated)


@router.patch("/rooms/{room_id}", response_model=schemas.RoomResponse)
def patch_room(room_id: int, updated: schemas.RoomUpdate, db: Session = Depends(get_db)):
    """Partially update a room"""
    room = service.get_room_by_id(db, room_id)
    if not room:
        room_not_found(room_id)
    return service.update_room(db, room, updated)


@router.delete("/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    """Delete a room by its ID"""
    room = service.get_room_by_id(db, room_id)
    if not room:
        room_not_found(room_id)
    service.delete_room(db, room)
    return {"message": f"Room with ID {room_id} deleted successfully"}