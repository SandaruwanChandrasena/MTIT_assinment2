# ─────────────────────────────────────────────────────────────
# HOTEL SERVICE LAYER
# This is the "brain" of the hotel service.
#
# WHY does this file exist?
# In proper microservices, we separate concerns:
#   - routes.py  → handles HTTP stuff (requests, responses, status codes)
#   - service.py → handles BUSINESS LOGIC (database queries, validation, rules)
#
# This way, routes.py doesn't need to know anything about the database.
# It just calls functions from this file and returns the result.
#
# PATTERN:
#   Request comes in → routes.py receives it → calls service.py → returns result
# ─────────────────────────────────────────────────────────────

from sqlalchemy.orm import Session
import models
import schemas


# ─────────────────────────────────────────────────────────────
# GET ALL HOTELS (with search, filter & pagination)
#
# Instead of dumping the ENTIRE database every time, this function:
#   1. Starts with ALL hotels as a base query
#   2. Applies FILTERS one by one (only if the client sent them)
#   3. Applies PAGINATION at the end (skip X, return Y)
#
# Example requests this supports:
#   GET /hotels                          → all hotels, first 20
#   GET /hotels?city=Colombo             → only hotels in Colombo
#   GET /hotels?min_rating=4             → only 4+ star rated hotels
#   GET /hotels?search=Hilton            → hotels with "Hilton" in the name
#   GET /hotels?city=Colombo&stars=5     → 5-star hotels in Colombo
#   GET /hotels?skip=20&limit=10         → hotels 21-30 (page 3)
#
# HOW FILTERING WORKS:
#   query.filter() adds a WHERE clause to the SQL query.
#   We chain multiple filters — each one narrows down the results.
#   It's like: SELECT * FROM hotels WHERE city='Colombo' AND stars=5
# ─────────────────────────────────────────────────────────────
def get_all_hotels(
    db: Session,
    search: str | None = None,       # search hotel name
    city: str | None = None,         # filter by city
    country: str | None = None,      # filter by country
    stars: int | None = None,        # filter by exact star rating
    min_rating: float | None = None, # filter by minimum user rating
    is_active: bool | None = None,   # filter by active status
    skip: int = 0,                   # how many to skip (for pagination)
    limit: int = 20,                 # how many to return (max per page)
) -> list[models.Hotel]:

    # Start with ALL hotels
    query = db.query(models.Hotel)

    # Apply each filter ONLY if the client sent it (not None)
    # .ilike() = case-insensitive search. % = wildcard (matches anything)
    # so "%hilton%" matches "Hilton Colombo", "The Hilton", etc.
    if search:
        query = query.filter(models.Hotel.name.ilike(f"%{search}%"))

    if city:
        query = query.filter(models.Hotel.city.ilike(f"%{city}%"))

    if country:
        query = query.filter(models.Hotel.country.ilike(f"%{country}%"))

    # Exact match for stars (e.g. stars=5 means ONLY 5-star hotels)
    if stars is not None:
        query = query.filter(models.Hotel.stars == stars)

    # Greater than or equal for rating (e.g. min_rating=4 means 4.0 and above)
    if min_rating is not None:
        query = query.filter(models.Hotel.rating >= min_rating)

    # Filter by active/inactive status
    if is_active is not None:
        query = query.filter(models.Hotel.is_active == is_active)

    # PAGINATION:
    # .offset(skip) = skip the first N results
    # .limit(limit) = only return N results after skipping
    # e.g. skip=20, limit=10 → skip first 20, return next 10 (items 21-30)
    return query.offset(skip).limit(limit).all()


# ─────────────────────────────────────────────────────────────
# GET HOTEL BY ID
# Looks up a single hotel by its ID.
# Returns the hotel object if found, or None if it doesn't exist.
# (routes.py is responsible for turning None into a 404 error)
# ─────────────────────────────────────────────────────────────
def get_hotel_by_id(db: Session, hotel_id: int) -> models.Hotel | None:
    return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()


# ─────────────────────────────────────────────────────────────
# CREATE HOTEL
# Takes the validated data from the request (schema),
# converts it into a database model, saves it, and returns it.
#
# Step by step:
#   1. hotel.dict() converts the Pydantic schema into a plain dictionary
#      e.g. {"name": "Hilton", "location": "Colombo", "rating": 4.5, ...}
#   2. models.Hotel(**...) creates a new Hotel database object from that dict
#   3. db.add() stages it for saving (like git add)
#   4. db.commit() actually saves it to the database (like git commit)
#   5. db.refresh() reloads it from DB to get the auto-generated ID
# ─────────────────────────────────────────────────────────────
def create_hotel(db: Session, hotel: schemas.HotelCreate) -> models.Hotel:
    db_hotel = models.Hotel(**hotel.dict())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel


# ─────────────────────────────────────────────────────────────
# UPDATE HOTEL
# Takes an existing hotel object and new data, updates each field.
#
# How it works:
#   1. updated.dict() gives us {"name": "New Name", "rating": 4.8, ...}
#   2. We loop through each key-value pair
#   3. setattr(hotel, "name", "New Name") is the same as hotel.name = "New Name"
#   4. After updating all fields, we commit (save) and refresh
#
# NOTE: "hotel" is the existing hotel object fetched from the DB.
#        The caller (routes.py) is responsible for fetching it first.
# ─────────────────────────────────────────────────────────────
def update_hotel(db: Session, hotel: models.Hotel, updated: schemas.HotelUpdate) -> models.Hotel:
    # exclude_unset=True means: only loop through fields the client ACTUALLY sent
    # e.g. if they only sent {"rating": 4.8}, we skip name/location/amenities
    # without this, all fields would be set to None and wipe out existing data
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(hotel, key, value)
    db.commit()
    db.refresh(hotel)
    return hotel


# ─────────────────────────────────────────────────────────────
# DELETE HOTEL
# Removes a hotel from the database permanently.
#
# NOTE: "hotel" is the existing hotel object fetched from the DB.
#        The caller (routes.py) is responsible for fetching it first
#        and returning 404 if it doesn't exist.
# ─────────────────────────────────────────────────────────────
def delete_hotel(db: Session, hotel: models.Hotel) -> None:
    db.delete(hotel)
    db.commit()
