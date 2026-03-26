# Database connection setup for Hotel Service
# SQLite database file will be created automatically as hotels.db

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL - creates hotels.db file in hotel-service folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./hotels.db"

# Create database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()

# Dependency function to get database session
# Used in routes to interact with the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Always close the session after use