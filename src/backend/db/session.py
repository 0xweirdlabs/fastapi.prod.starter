"""
Database session setup for SQLite.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.backend.core.config import get_settings

settings = get_settings()

# Create database engine for SQLite
engine = create_engine(
    settings.DATABASE_URL,
    # For SQLite, we need to enable same thread checking
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
    # These settings can be adjusted based on your requirements
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.DEBUG,
)

# Create sessionmaker for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a session dependency
def get_db():
    """
    Dependency for database sessions.
    Creates a new session for each request and closes it when done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
