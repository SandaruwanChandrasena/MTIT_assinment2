# ─────────────────────────────────────────────────────────────
# PAYMENT SERVICE LAYER
# Handles all business logic, database queries, and
# inter-service communication with Booking Service.
# PATTERN: routes.py (HTTP) → service.py (logic) → Database
# ─────────────────────────────────────────────────────────────

from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import httpx
import models
import schemas

BOOKING_SERVICE_URL = "http://localhost:8004"


def verify_booking_exists(booking_id: int):
    try:
        response = httpx.get(f"{BOOKING_SERVICE_URL}/bookings/{booking_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=400,
                detail=f"Booking with ID {booking_id} does not exist.")
    except httpx.ConnectError:
        raise HTTPException(status_code=503,
            detail="Booking Service is unavailable.")


# ─────────────────────────────────────────────────────────────
# GET ALL PAYMENTS (with filter & pagination)
#
# Supported filters:
#   GET /payments?booking_id=1          → payments for booking
#   GET /payments?status=paid           → filter by status
#   GET /payments?method=card           → filter by method
#   GET /payments?min_amount=100        → minimum amount
#   GET /payments?max_amount=500        → maximum amount
#   GET /payments?skip=0&limit=20      → pagination
# ─────────────────────────────────────────────────────────────
def get_all_payments(
    db:         Session,
    booking_id: Optional[int]   = None,
    status:     Optional[str]   = None,
    method:     Optional[str]   = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    skip:  int = 0,
    limit: int = 20,
) -> list[models.Payment]:
    query = db.query(models.Payment)

    if booking_id is not None: query = query.filter(models.Payment.booking_id == booking_id)
    if status:                 query = query.filter(models.Payment.status.ilike(f"%{status}%"))
    if method:                 query = query.filter(models.Payment.method.ilike(f"%{method}%"))
    if min_amount is not None: query = query.filter(models.Payment.amount >= min_amount)
    if max_amount is not None: query = query.filter(models.Payment.amount <= max_amount)

    return query.offset(skip).limit(limit).all()


def get_payment_by_id(db: Session, payment_id: int) -> models.Payment | None:
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()


def create_payment(db: Session, payment: schemas.PaymentCreate) -> models.Payment:
    verify_booking_exists(payment.booking_id)
    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def update_payment(db: Session, payment: models.Payment, updated: schemas.PaymentUpdate) -> models.Payment:
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(payment, key, value)
    db.commit()
    db.refresh(payment)
    return payment


def delete_payment(db: Session, payment: models.Payment) -> None:
    db.delete(payment)
    db.commit()