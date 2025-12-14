"""
Database configuration and session management.

This module initializes the SQLAlchemy engine, session factory,
and declarative base used throughout the application.

All database access in the service should be routed through
these shared objects to ensure consistent configuration
and connection handling.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

# Create the SQLAlchemy engine using the configured database URL.
#
# The `check_same_thread=False` flag is required when using SQLite
# in multi-threaded environments such as FastAPI, where requests
# may be handled concurrently.
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)

# Session factory used to create new database sessions per request.
#
# Sessions should be short-lived and explicitly closed after use
# (typically via dependency injection in FastAPI routes).
SessionLocal = sessionmaker(bind=engine)

# Base class for all ORM models.
#
# All SQLAlchemy models should inherit from this base so metadata
# can be created and managed centrally.
Base = declarative_base()
