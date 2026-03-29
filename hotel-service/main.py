# ─────────────────────────────────────────────────────────────
# HOTEL SERVICE - MAIN ENTRY POINT
#
# This is the file that starts everything. When you run:
#   uvicorn main:app --reload --port 8001
#
# It does 3 things:
#   1. Creates the database tables (if they don't exist yet)
#   2. Creates the FastAPI app instance
#   3. Registers all routes from routes.py
# ─────────────────────────────────────────────────────────────

from fastapi import FastAPI
from database import engine, SessionLocal
import models
from routes import router
from sqlalchemy import text

# Create all database tables automatically on startup
# If tables already exist, this does nothing
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI(
    title="Hotel Service",
    description="Manages hotel information for the Hotel Booking System",
    version="1.0.0"
)

# Register all routes from routes.py
app.include_router(router)


# ─────────────────────────────────────────────────────────────
# HEALTH CHECK ENDPOINT
#
# WHY do we need this?
# In microservices, the API Gateway needs to know if each service
# is alive and working. This endpoint is like a heartbeat —
# the gateway (or a monitoring tool) pings it periodically.
#
# It checks TWO things:
#   1. Is the service running? (if you can reach this endpoint, yes)
#   2. Is the database connected? (tries to run a simple query)
#
# Returns:
#   {"status": "healthy", "service": "hotel-service", "database": "connected"}
#   or
#   {"status": "unhealthy", "service": "hotel-service", "database": "disconnected"}
# ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    """Check if the service and database are running"""
    try:
        # Try to open a database session and run a simple query
        # If this works, the database is connected
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "service": "hotel-service",
        "database": db_status,
    }
