# ─────────────────────────────────────────────────────────────
# PAYMENT SERVICE ROUTES
#
# INTER-SERVICE COMMUNICATION:
#   When creating a payment, this service calls Booking Service
#   to verify that the booking_id actually exists.
#
#   Payment Service ──HTTP call──> Booking Service (port 8004)
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import httpx
import models
import schemas
from database import get_db

router = APIRouter()

# URL of the Booking Service (for inter-service communication)
BOOKING_SERVICE_URL = "http://localhost:8004"


# ─────────────────────────────────────────────────────────────
# HELPER: Verify a booking exists by calling Booking Service
# ─────────────────────────────────────────────────────────────
def verify_booking_exists(booking_id: int):
    try:
        response = httpx.get(f"{BOOKING_SERVICE_URL}/bookings/{booking_id}")
        if response.status_code == 404:
            raise HTTPException(
                status_code=400,
                detail=f"Booking with ID {booking_id} does not exist. Cannot create payment for non-existent booking."
            )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Booking Service is unavailable. Cannot verify booking."
        )


# ─────────────────────────────────────────
# GET ALL PAYMENTS
# ─────────────────────────────────────────
@router.get("/payments", response_model=List[schemas.PaymentResponse])
def get_all_payments(db: Session = Depends(get_db)):
    """Get list of all payments"""
    return db.query(models.Payment).all()


# ─────────────────────────────────────────
# GET PAYMENT BY ID
# ─────────────────────────────────────────
@router.get("/payments/{payment_id}", response_model=schemas.PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """Get a single payment by its ID"""
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


# ─────────────────────────────────────────
# CREATE NEW PAYMENT
# Now validates that the booking exists first!
# ─────────────────────────────────────────
@router.post("/payments", response_model=schemas.PaymentResponse)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    """Create a new payment — verifies booking exists via Booking Service"""

    # INTER-SERVICE CALL: Check if the booking exists
    verify_booking_exists(payment.booking_id)

    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


# ─────────────────────────────────────────
# UPDATE PAYMENT
# ─────────────────────────────────────────
@router.put("/payments/{payment_id}", response_model=schemas.PaymentResponse)
def update_payment(payment_id: int, updated: schemas.PaymentUpdate, db: Session = Depends(get_db)):
    """Update an existing payment by its ID"""
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    for key, value in updated.dict().items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment


# ─────────────────────────────────────────
# DELETE PAYMENT
# ─────────────────────────────────────────
@router.delete("/payments/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    """Delete a payment by its ID"""
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    db.delete(payment)
    db.commit()
    return {"message": f"Payment with ID {payment_id} deleted successfully"}
