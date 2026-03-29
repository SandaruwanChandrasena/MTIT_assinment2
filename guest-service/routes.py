# ─────────────────────────────────────────────────────────────
# GUEST SERVICE ROUTES (Controller Layer)
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


def guest_not_found(guest_id: int):
    raise HTTPException(status_code=404, detail=f"Guest with ID {guest_id} not found")


# ─────────────────────────────────────────
# GET ALL GUESTS (with search, filter & pagination)
#
# Examples:
#   GET /guests                          → all guests
#   GET /guests?search=John              → search name or email
#   GET /guests?nationality=Sri Lankan   → filter by nationality
#   GET /guests?skip=0&limit=20         → pagination
# ─────────────────────────────────────────
@router.get("/guests", response_model=List[schemas.GuestResponse])
def get_all_guests(
    search:      Optional[str] = Query(default=None, description="Search by name or email"),
    nationality: Optional[str] = Query(default=None, description="Filter by nationality"),
    skip:  int = Query(default=0,  ge=0,  description="Records to skip (pagination)"),
    limit: int = Query(default=20, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    """Get guests with optional search, filters and pagination"""
    return service.get_all_guests(
        db,
        search=search,
        nationality=nationality,
        skip=skip,
        limit=limit,
    )


@router.get("/guests/{guest_id}", response_model=schemas.GuestResponse)
def get_guest(guest_id: int, db: Session = Depends(get_db)):
    """Get a single guest by their ID"""
    guest = service.get_guest_by_id(db, guest_id)
    if not guest:
        guest_not_found(guest_id)
    return guest


@router.post("/guests", response_model=schemas.GuestResponse, status_code=201)
def create_guest(guest: schemas.GuestCreate, db: Session = Depends(get_db)):
    """Create a new guest record"""
    return service.create_guest(db, guest)


@router.put("/guests/{guest_id}", response_model=schemas.GuestResponse)
def update_guest(guest_id: int, updated: schemas.GuestUpdate, db: Session = Depends(get_db)):
    """Update an existing guest by their ID"""
    guest = service.get_guest_by_id(db, guest_id)
    if not guest:
        guest_not_found(guest_id)
    return service.update_guest(db, guest, updated)


@router.patch("/guests/{guest_id}", response_model=schemas.GuestResponse)
def patch_guest(guest_id: int, updated: schemas.GuestUpdate, db: Session = Depends(get_db)):
    """Partially update a guest"""
    guest = service.get_guest_by_id(db, guest_id)
    if not guest:
        guest_not_found(guest_id)
    return service.update_guest(db, guest, updated)


@router.delete("/guests/{guest_id}")
def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    """Delete a guest by their ID"""
    guest = service.get_guest_by_id(db, guest_id)
    if not guest:
        guest_not_found(guest_id)
    service.delete_guest(db, guest)
    return {"message": f"Guest with ID {guest_id} deleted successfully"}