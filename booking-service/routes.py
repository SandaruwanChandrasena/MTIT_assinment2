# ─────────────────────────────────────────────────────────────
# BOOKING SERVICE ROUTES
#
# INTER-SERVICE COMMUNICATION:
#   This service talks to TWO other services:
#
#   1. Guest Service (port 8003) — verify the guest exists
#   2. Room Service  (port 8002) — verify room exists,
#      check availability, and update availability
#
#   Flow when creating a booking:
#     Client → Booking Service → Guest Service (verify guest)
#                              → Room Service  (verify room + check available)
#                              → Room Service  (mark room unavailable)
#                              → Save booking
#
#   Flow when deleting a booking:
#     Client → Booking Service → Room Service (mark room available again)
#                              → Delete booking
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import httpx
import models
import schemas
from database import get_db

router = APIRouter()

# URLs of other microservices (for inter-service communication)
ROOM_SERVICE_URL = "http://localhost:8002"
GUEST_SERVICE_URL = "http://localhost:8003"


# ─────────────────────────────────────────────────────────────
# HELPER: Verify a guest exists by calling Guest Service
# ─────────────────────────────────────────────────────────────
def verify_guest_exists(guest_id: int):
    try:
        response = httpx.get(f"{GUEST_SERVICE_URL}/guests/{guest_id}")
        if response.status_code == 404:
            raise HTTPException(
                status_code=400,
                detail=f"Guest with ID {guest_id} does not exist."
            )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Guest Service is unavailable. Cannot verify guest."
        )


# ─────────────────────────────────────────────────────────────
# HELPER: Verify a room exists AND is available
# Returns the room data so we can use it later
# ─────────────────────────────────────────────────────────────
def verify_room_available(room_id: int):
    try:
        response = httpx.get(f"{ROOM_SERVICE_URL}/rooms/{room_id}")
        if response.status_code == 404:
            raise HTTPException(
                status_code=400,
                detail=f"Room with ID {room_id} does not exist."
            )
        room_data = response.json()
        if not room_data.get("is_available", False):
            raise HTTPException(
                status_code=400,
                detail=f"Room with ID {room_id} is not available. It is already booked."
            )
        return room_data
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Room Service is unavailable. Cannot verify room."
        )


# ─────────────────────────────────────────────────────────────
# HELPER: Update room availability in Room Service
#
# After creating a booking → mark room as unavailable (False)
# After deleting a booking → mark room as available again (True)
# ─────────────────────────────────────────────────────────────
def update_room_availability(room_id: int, room_data: dict, is_available: bool):
    try:
        room_data["is_available"] = is_available
        httpx.put(f"{ROOM_SERVICE_URL}/rooms/{room_id}", json=room_data)
    except httpx.ConnectError:
        # Room update failed but booking was already created/deleted
        # In production you'd use a message queue to retry this
        pass


# ─────────────────────────────────────────
# GET ALL BOOKINGS
# ─────────────────────────────────────────
@router.get("/bookings", response_model=List[schemas.BookingResponse])
def get_all_bookings(db: Session = Depends(get_db)):
    """Get list of all bookings"""
    return db.query(models.Booking).all()


# ─────────────────────────────────────────
# GET BOOKING BY ID
# ─────────────────────────────────────────
@router.get("/bookings/{booking_id}", response_model=schemas.BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get a single booking by its ID"""
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


# ─────────────────────────────────────────
# CREATE NEW BOOKING
#
# This is where inter-service communication happens:
#   1. Verify guest exists (call Guest Service)
#   2. Verify room exists + is available (call Room Service)
#   3. Create the booking
#   4. Mark room as unavailable (call Room Service)
# ─────────────────────────────────────────
@router.post("/bookings", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking — verifies guest and room via other services"""

    # INTER-SERVICE CALL 1: Verify guest exists
    verify_guest_exists(booking.guest_id)

    # INTER-SERVICE CALL 2: Verify room exists and is available
    room_data = verify_room_available(booking.room_id)

    # All checks passed — create the booking
    db_booking = models.Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    # INTER-SERVICE CALL 3: Mark room as unavailable
    update_room_availability(booking.room_id, room_data, is_available=False)

    return db_booking


# ─────────────────────────────────────────
# UPDATE BOOKING
# ─────────────────────────────────────────
@router.put("/bookings/{booking_id}", response_model=schemas.BookingResponse)
def update_booking(booking_id: int, updated: schemas.BookingUpdate, db: Session = Depends(get_db)):
    """Update an existing booking by its ID"""
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    for key, value in updated.dict().items():
        setattr(booking, key, value)

    db.commit()
    db.refresh(booking)
    return booking


# ─────────────────────────────────────────
# DELETE BOOKING
#
# When a booking is deleted, the room should become
# available again. So we call Room Service to update it.
# ─────────────────────────────────────────
@router.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """Delete a booking — marks the room as available again"""
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # INTER-SERVICE CALL: Get room data and mark it as available again
    try:
        response = httpx.get(f"{ROOM_SERVICE_URL}/rooms/{booking.room_id}")
        if response.status_code == 200:
            room_data = response.json()
            update_room_availability(booking.room_id, room_data, is_available=True)
    except httpx.ConnectError:
        pass  # Room service is down, continue with deletion anyway

    db.delete(booking)
    db.commit()
    return {"message": f"Booking with ID {booking_id} deleted successfully"}
