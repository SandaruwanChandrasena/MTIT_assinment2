# ─────────────────────────────────────────────────────────────
# BOOKING SERVICE ROUTES (Controller Layer)
# Handles HTTP only — all logic lives in service.py
# PATTERN: Request → routes.py (HTTP) → service.py (logic) → DB
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
import service
from database import get_db

router = APIRouter()


def booking_not_found(booking_id: int):
    raise HTTPException(status_code=404, detail=f"Booking with ID {booking_id} not found")


# ─────────────────────────────────────────
# GET ALL BOOKINGS (with filter & pagination)
#
# Examples:
#   GET /bookings?guest_id=1               → bookings by guest
#   GET /bookings?room_id=2                → bookings for room
#   GET /bookings?status=confirmed         → filter by status
#   GET /bookings?check_in_from=2026-04-01 → from date
#   GET /bookings?check_in_to=2026-06-30   → until date
#   GET /bookings?skip=0&limit=20         → pagination
# ─────────────────────────────────────────
@router.get("/bookings", response_model=List[schemas.BookingResponse])
def get_all_bookings(
    guest_id:      Optional[int] = Query(default=None, description="Filter by guest ID"),
    room_id:       Optional[int] = Query(default=None, description="Filter by room ID"),
    status:        Optional[str] = Query(default=None, description="Filter by status (confirmed/pending/cancelled)"),
    check_in_from: Optional[str] = Query(default=None, description="Check-in date from (YYYY-MM-DD)"),
    check_in_to:   Optional[str] = Query(default=None, description="Check-in date until (YYYY-MM-DD)"),
    skip:  int = Query(default=0,  ge=0,  description="Records to skip (pagination)"),
    limit: int = Query(default=20, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    """Get bookings with optional filters and pagination"""
    return service.get_all_bookings(
        db,
        guest_id=guest_id,
        room_id=room_id,
        status=status,
        check_in_from=check_in_from,
        check_in_to=check_in_to,
        skip=skip,
        limit=limit,
    )


@router.get("/bookings/{booking_id}", response_model=schemas.BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get a single booking by its ID"""
    booking = service.get_booking_by_id(db, booking_id)
    if not booking:
        booking_not_found(booking_id)
    return booking


@router.post("/bookings", response_model=schemas.BookingResponse, status_code=201)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking — verifies guest and room via other services"""
    return service.create_booking(db, booking)


@router.put("/bookings/{booking_id}", response_model=schemas.BookingResponse)
def update_booking(booking_id: int, updated: schemas.BookingUpdate, db: Session = Depends(get_db)):
    """Update an existing booking by its ID"""
    booking = service.get_booking_by_id(db, booking_id)
    if not booking:
        booking_not_found(booking_id)
    return service.update_booking(db, booking, updated)


@router.patch("/bookings/{booking_id}", response_model=schemas.BookingResponse)
def patch_booking(booking_id: int, updated: schemas.BookingUpdate, db: Session = Depends(get_db)):
    """Partially update a booking"""
    booking = service.get_booking_by_id(db, booking_id)
    if not booking:
        booking_not_found(booking_id)
    return service.update_booking(db, booking, updated)


@router.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """Delete a booking — marks the room as available again"""
    booking = service.get_booking_by_id(db, booking_id)
    if not booking:
        booking_not_found(booking_id)
    service.delete_booking(db, booking)
    return {"message": f"Booking with ID {booking_id} deleted successfully"}