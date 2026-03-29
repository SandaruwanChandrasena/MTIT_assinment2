# ─────────────────────────────────────────────────────────────
# ROOM SERVICE LAYER
# Handles all business logic and database queries.
# PATTERN: routes.py (HTTP) → service.py (logic) → Database
# ─────────────────────────────────────────────────────────────

from sqlalchemy.orm import Session
from typing import Optional
import models
import schemas


# ─────────────────────────────────────────────────────────────
# GET ALL ROOMS (with filter & pagination)
#
# Supported filters:
#   GET /rooms?hotel_id=1                   → rooms in hotel 1
#   GET /rooms?room_type=Suite              → only suites
#   GET /rooms?is_available=true            → only available rooms
#   GET /rooms?min_price=100&max_price=300  → rooms in price range
#   GET /rooms?skip=0&limit=20              → pagination
# ─────────────────────────────────────────────────────────────
def get_all_rooms(
    db:           Session,
    hotel_id:     Optional[int]   = None,
    room_type:    Optional[str]   = None,
    is_available: Optional[bool]  = None,
    min_price:    Optional[float] = None,
    max_price:    Optional[float] = None,
    skip:  int = 0,
    limit: int = 20,
) -> list[models.Room]:
    query = db.query(models.Room)

    if hotel_id     is not None: query = query.filter(models.Room.hotel_id == hotel_id)
    if room_type:                query = query.filter(models.Room.room_type.ilike(f"%{room_type}%"))
    if is_available is not None: query = query.filter(models.Room.is_available == is_available)
    if min_price    is not None: query = query.filter(models.Room.price_per_night >= min_price)
    if max_price    is not None: query = query.filter(models.Room.price_per_night <= max_price)

    return query.offset(skip).limit(limit).all()


def get_room_by_id(db: Session, room_id: int) -> models.Room | None:
    return db.query(models.Room).filter(models.Room.id == room_id).first()


def create_room(db: Session, room: schemas.RoomCreate) -> models.Room:
    db_room = models.Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def update_room(db: Session, room: models.Room, updated: schemas.RoomUpdate) -> models.Room:
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(room, key, value)
    db.commit()
    db.refresh(room)
    return room


def delete_room(db: Session, room: models.Room) -> None:
    db.delete(room)
    db.commit()