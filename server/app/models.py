"""
SQLAlchemy models for the Profile Intake service.

These ORM models define the persisted database schema.
They should stay aligned with the public API schemas (Pydantic models)
to avoid runtime response validation errors.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from .database import Base


def _uuid_str() -> str:
    """Generate a UUID string suitable for primary keys."""
    return str(uuid.uuid4())


class Profile(Base):
    """
    A Profile represents a single user identity record.

    Notes:
    - `created_at` is populated server-side.
    - The API returns `created_at`, so the DB must persist it.
    """

    __tablename__ = "profiles"

    id = Column(String, primary_key=True, default=_uuid_str, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    github_url = Column(String, nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    submissions = relationship(
        "Submission",
        back_populates="profile",
        cascade="all, delete-orphan",
    )


class Submission(Base):
    """
    A Submission represents a PDF upload tied to a Profile.

    Lifecycle fields:
    - `status`: UPLOADED -> PROCESSING -> COMPLETED
    - `locked`: once submitted, re-submission is blocked
    """

    __tablename__ = "submissions"

    id = Column(String, primary_key=True, default=_uuid_str, nullable=False)

    profile_id = Column(String, ForeignKey("profiles.id"), nullable=False, index=True)

    filename = Column(String, nullable=False)
    status = Column(String, nullable=False, default="UPLOADED")
    locked = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    profile = relationship("Profile", back_populates="submissions")
