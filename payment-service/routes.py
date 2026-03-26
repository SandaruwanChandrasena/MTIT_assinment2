# Payment Service Routes
# Contains all CRUD endpoints for Payment management

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db

# Create API router instance
router = APIRouter()

# ─────────────────────────────────────────
# GET ALL PAYMENTS
# ─────────────────────────────────────────
@router.get("/payments", response_model=List[schemas.PaymentResponse])
def get_all_payments(db: Session = Depends(get_db)):
    """Get list of all payments"""
    payments = db.query(models.Payment).all()
    return payments

# ─────────────────────────────────────────
# GET PAYMENT BY ID
# ─────────────────────────────────────────
@router.get("/payments/{payment_id}", response_model=schemas.PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """Get a single payment by its ID"""
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    
    # Return 404 if payment not found
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

# ─────────────────────────────────────────
# CREATE NEW PAYMENT
# ─────────────────────────────────────────
@router.post("/payments", response_model=schemas.PaymentResponse)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    """Create a new payment record"""
    # Convert schema to database model
    db_payment = models.Payment(**payment.dict())
    
    db.add(db_payment)      # Add to database
    db.commit()             # Save changes
    db.refresh(db_payment)  # Refresh to get generated ID
    return db_payment

# ─────────────────────────────────────────
# UPDATE PAYMENT
# ─────────────────────────────────────────
@router.put("/payments/{payment_id}", response_model=schemas.PaymentResponse)
def update_payment(payment_id: int, updated: schemas.PaymentUpdate, db: Session = Depends(get_db)):
    """Update an existing payment by its ID"""
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    
    # Return 404 if payment not found
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    # Update each field dynamically
    for key, value in updated.dict().items():
        setattr(payment, key, value)
    
    db.commit()          # Save changes
    db.refresh(payment)  # Refresh updated data
    return payment

# ─────────────────────────────────────────
# DELETE PAYMENT
# ─────────────────────────────────────────
@router.delete("/payments/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    """Delete a payment by its ID"""
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    
    # Return 404 if payment not found
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    db.delete(payment)  # Delete from database
    db.commit()         # Save changes
    return {"message": f"Payment with ID {payment_id} deleted successfully"}