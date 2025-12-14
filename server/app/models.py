"""
ORM models for the Profile Intake API.

This module defines the database schema using SQLAlchemy ORM.
Models represent persistent domain entities and should remain
focused on data structure rather than business logic.
"""

import uuid

from sqlalchemy import Boolean, Column, String

from .database import Base


class Profile(Base):
    """
    Profile entity.

    Represents an individual profile submitted to the system.
    This model stores identity and metadata only; no workflow
    or processing logic is embedded here.
    """

    __tablename__ = "profiles"

    # Primary identifier for the profile.
    # UUIDs are used to avoid exposing sequential IDs.
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Basic profile attributes.
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    github_url = Column(String)


class Submission(Base):
    """
    Submission entity.

    Represents a document submission associated with a profile.
    This model tracks the submission lifecycle and enforces
    immutability once the submission is locked.
    """

    __tablename__ = "submissions"

    # Primary identifier for the submission.
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Identifier of the associated profile.
    # Stored as a string UUID for simplicity.
    profile_id = Column(String)

    # Current lifecycle status of the submission.
    # Expected values include: UPLOADED, PROCESSING, COMPLETED, REJECTED.
    status = Column(String, default="UPLOADED")

    # Indicates whether the submission has been finalized.
    # Once locked, the submission cannot be resubmitted or modified.
    locked = Column(Boolean, default=False)

    # Original filename of the uploaded document.
    # Stored for reference and traceability.
    filename = Column(String)
