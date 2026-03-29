# ─────────────────────────────────────────────────────────────
# PAYMENT SERVICE ROUTES (Controller Layer)
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


def payment_not_found(payment_id: int):
    raise HTTPException(status_code=404, detail=f"Payment with ID {payment_id} not found")


# ─────────────────────────────────────────
# GET ALL PAYMENTS (with filter & pagination)
#
# Examples:
#   GET /payments?booking_id=1          → payments for booking
#   GET /payments?status=paid           → paid only
#   GET /payments?method=card           → card payments only
#   GET /payments?min_amount=100        → amount >= 100
#   GET /payments?max_amount=500        → amount <= 500
#   GET /payments?skip=0&limit=20      → pagination
# ─────────────────────────────────────────
@router.get("/payments", response_model=List[schemas.PaymentResponse])
def get_all_payments(
    booking_id: Optional[int]   = Query(default=None, description="Filter by booking ID"),
    status:     Optional[str]   = Query(default=None, description="Filter by status (paid/pending/failed)"),
    method:     Optional[str]   = Query(default=None, description="Filter by method (card/cash/online)"),
    min_amount: Optional[float] = Query(default=None, ge=0, description="Minimum payment amount"),
    max_amount: Optional[float] = Query(default=None, ge=0, description="Maximum payment amount"),
    skip:  int = Query(default=0,  ge=0,  description="Records to skip (pagination)"),
    limit: int = Query(default=20, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    """Get payments with optional filters and pagination"""
    return service.get_all_payments(
        db,
        booking_id=booking_id,
        status=status,
        method=method,
        min_amount=min_amount,
        max_amount=max_amount,
        skip=skip,
        limit=limit,
    )


@router.get("/payments/{payment_id}", response_model=schemas.PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """Get a single payment by its ID"""
    payment = service.get_payment_by_id(db, payment_id)
    if not payment:
        payment_not_found(payment_id)
    return payment


@router.post("/payments", response_model=schemas.PaymentResponse, status_code=201)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    """Create a new payment — verifies booking exists via Booking Service"""
    return service.create_payment(db, payment)


@router.put("/payments/{payment_id}", response_model=schemas.PaymentResponse)
def update_payment(payment_id: int, updated: schemas.PaymentUpdate, db: Session = Depends(get_db)):
    """Update an existing payment by its ID"""
    payment = service.get_payment_by_id(db, payment_id)
    if not payment:
        payment_not_found(payment_id)
    return service.update_payment(db, payment, updated)


@router.patch("/payments/{payment_id}", response_model=schemas.PaymentResponse)
def patch_payment(payment_id: int, updated: schemas.PaymentUpdate, db: Session = Depends(get_db)):
    """Partially update a payment"""
    payment = service.get_payment_by_id(db, payment_id)
    if not payment:
        payment_not_found(payment_id)
    return service.update_payment(db, payment, updated)


@router.delete("/payments/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    """Delete a payment by its ID"""
    payment = service.get_payment_by_id(db, payment_id)
    if not payment:
        payment_not_found(payment_id)
    service.delete_payment(db, payment)
    return {"message": f"Payment with ID {payment_id} deleted successfully"}