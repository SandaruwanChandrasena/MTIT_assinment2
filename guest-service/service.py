# ─────────────────────────────────────────────────────────────
# GUEST SERVICE LAYER
# Handles all business logic and database queries.
# PATTERN: routes.py (HTTP) → service.py (logic) → Database
# ─────────────────────────────────────────────────────────────

from sqlalchemy.orm import Session
from typing import Optional
import models
import schemas


# ─────────────────────────────────────────────────────────────
# GET ALL GUESTS (with search, filter & pagination)
#
# Supported filters:
#   GET /guests?search=John            → search by name or email
#   GET /guests?nationality=Sri Lankan → filter by nationality
#   GET /guests?skip=0&limit=20       → pagination
# ─────────────────────────────────────────────────────────────
def get_all_guests(
    db:          Session,
    search:      Optional[str] = None,
    nationality: Optional[str] = None,
    skip:  int = 0,
    limit: int = 20,
) -> list[models.Guest]:
    query = db.query(models.Guest)

    # Search by name OR email (case-insensitive)
    if search:
        query = query.filter(
            models.Guest.name.ilike(f"%{search}%") |
            models.Guest.email.ilike(f"%{search}%")
        )

    if nationality:
        query = query.filter(models.Guest.nationality.ilike(f"%{nationality}%"))

    return query.offset(skip).limit(limit).all()


def get_guest_by_id(db: Session, guest_id: int) -> models.Guest | None:
    return db.query(models.Guest).filter(models.Guest.id == guest_id).first()


def create_guest(db: Session, guest: schemas.GuestCreate) -> models.Guest:
    db_guest = models.Guest(**guest.dict())
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest


def update_guest(db: Session, guest: models.Guest, updated: schemas.GuestUpdate) -> models.Guest:
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(guest, key, value)
    db.commit()
    db.refresh(guest)
    return guest


def delete_guest(db: Session, guest: models.Guest) -> None:
    db.delete(guest)
    db.commit()