# ─────────────────────────────────────────────────────────────
# BOOKING SERVICE LAYER
# Handles all business logic, database queries, and
# inter-service communication with Guest & Room services.
# PATTERN: routes.py (HTTP) → service.py (logic) → Database
# ─────────────────────────────────────────────────────────────

from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import httpx
import models
import schemas

ROOM_SERVICE_URL  = "http://localhost:8002"
GUEST_SERVICE_URL = "http://localhost:8003"


# ── Inter-service helpers ──────────────────────────────────────
def verify_guest_exists(guest_id: int):
    try:
        response = httpx.get(f"{GUEST_SERVICE_URL}/guests/{guest_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=400,
                detail=f"Guest with ID {guest_id} does not exist.")
    except httpx.ConnectError:
        raise HTTPException(status_code=503,
            detail="Guest Service is unavailable.")


def verify_room_available(room_id: int):
    try:
        response = httpx.get(f"{ROOM_SERVICE_URL}/rooms/{room_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=400,
                detail=f"Room with ID {room_id} does not exist.")
        room_data = response.json()
        if not room_data.get("is_available", False):
            raise HTTPException(status_code=400,
                detail=f"Room with ID {room_id} is not available.")
        return room_data
    except httpx.ConnectError:
        raise HTTPException(status_code=503,
            detail="Room Service is unavailable.")


def update_room_availability(room_id: int, room_data: dict, is_available: bool):
    try:
        room_data["is_available"] = is_available
        httpx.put(f"{ROOM_SERVICE_URL}/rooms/{room_id}", json=room_data)
    except httpx.ConnectError:
        pass


# ─────────────────────────────────────────────────────────────
# GET ALL BOOKINGS (with filter & pagination)
#
# Supported filters:
#   GET /bookings?guest_id=1            → bookings by guest
#   GET /bookings?room_id=2             → bookings for room
#   GET /bookings?status=confirmed      → filter by status
#   GET /bookings?check_in_from=2026-04-01  → bookings from date
#   GET /bookings?check_in_to=2026-06-30    → bookings until date
#   GET /bookings?skip=0&limit=20      → pagination
# ─────────────────────────────────────────────────────────────
def get_all_bookings(
    db:             Session,
    guest_id:       Optional[int] = None,
    room_id:        Optional[int] = None,
    status:         Optional[str] = None,
    check_in_from:  Optional[str] = None,
    check_in_to:    Optional[str] = None,
    skip:  int = 0,
    limit: int = 20,
) -> list[models.Booking]:
    query = db.query(models.Booking)

    if guest_id      is not None: query = query.filter(models.Booking.guest_id == guest_id)
    if room_id       is not None: query = query.filter(models.Booking.room_id == room_id)
    if status:                    query = query.filter(models.Booking.status.ilike(f"%{status}%"))
    if check_in_from:             query = query.filter(models.Booking.check_in >= check_in_from)
    if check_in_to:               query = query.filter(models.Booking.check_in <= check_in_to)

    return query.offset(skip).limit(limit).all()


def get_booking_by_id(db: Session, booking_id: int) -> models.Booking | None:
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()


def create_booking(db: Session, booking: schemas.BookingCreate) -> models.Booking:
    verify_guest_exists(booking.guest_id)
    room_data = verify_room_available(booking.room_id)

    db_booking = models.Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    update_room_availability(booking.room_id, room_data, is_available=False)
    return db_booking


def update_booking(db: Session, booking: models.Booking, updated: schemas.BookingUpdate) -> models.Booking:
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(booking, key, value)
    db.commit()
    db.refresh(booking)
    return booking


def delete_booking(db: Session, booking: models.Booking) -> None:
    try:
        response = httpx.get(f"{ROOM_SERVICE_URL}/rooms/{booking.room_id}")
        if response.status_code == 200:
            update_room_availability(booking.room_id, response.json(), is_available=True)
    except httpx.ConnectError:
        pass

    db.delete(booking)
    db.commit()