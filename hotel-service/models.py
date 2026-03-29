# ─────────────────────────────────────────────────────────────
# SQLAlchemy Database Model for Hotel
#
# This defines the actual TABLE STRUCTURE in the SQLite database.
# Each field here = a column in the "hotels" table.
#
# When the app starts, SQLAlchemy reads this class and creates
# the table automatically if it doesn't exist yet.
# ─────────────────────────────────────────────────────────────

from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base


class Hotel(Base):
    # The name of the table in the SQLite database file
    __tablename__ = "hotels"

    # ── Primary Key ──
    # Auto-incrementing ID — database generates this automatically
    # index=True makes lookups by ID faster
    id = Column(Integer, primary_key=True, index=True)

    # ── Hotel Identity ──
    name        = Column(String(100), nullable=False)     # Hotel name (required)
    description = Column(String(1000), nullable=False)    # Short description (required)

    # ── Location Info ──
    address = Column(String(300), nullable=False)         # Full street address
    city    = Column(String(100), nullable=False)         # City name
    country = Column(String(100), nullable=False)         # Country name

    # ── Contact Info ──
    phone = Column(String(20), nullable=False)            # Contact phone number
    email = Column(String(100), nullable=False)           # Contact email

    # ── Hotel Details ──
    stars           = Column(Integer, nullable=False)     # Star classification (1-5)
    price_per_night = Column(Float, nullable=False)       # Base price in USD
    amenities       = Column(String(500), nullable=False) # Comma-separated amenities
    rating          = Column(Float, default=0.0)          # Average user rating (0-5)
    image_url       = Column(String(500), nullable=True)  # Photo URL (optional)
    is_active       = Column(Boolean, default=True)       # Accepting bookings? (default: yes)
