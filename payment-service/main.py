# Payment Service - Main Entry Point
# Starts the FastAPI app and creates database tables

from fastapi import FastAPI
from database import engine
import models
from routes import router

# Create all database tables automatically on startup
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI(
    title="Payment Service",
    description="Manages payment information for the Hotel Booking System",
    version="1.0.0"
)

# Register all routes from routes.py
app.include_router(router)
