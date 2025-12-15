"""
Pydantic schemas for request and response validation.

This module defines the public API contract for the Profile Intake service.
Schemas here are used by:
- FastAPI for request validation
- OpenAPI/Swagger for documentation
- Internal code to enforce clear boundaries between layers

Design principles:
- Separate input (Create) and output (Out) models
- Explicit field validation
- Minimal but realistic constraints
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ProfileCreate(BaseModel):
    """
    Request schema for creating a new Profile.

    This model represents the minimal identity information
    required to create a profile before any document submission.
    """

    # User's first name (required, non-empty)
    first_name: str = Field(
        min_length=1,
        description="First name of the profile owner",
        examples=["John"],
    )

    # User's last name (required, non-empty)
    last_name: str = Field(
        min_length=1,
        description="Last name of the profile owner",
        examples=["Smith"],
    )

    # Primary contact email, validated using RFC-compliant rules
    email: EmailStr = Field(
        description="Email address associated with the profile",
        examples=["john.smith@example.com"],
    )

    # Optional GitHub profile URL for enrichment purposes
    github_url: str | None = Field(
        default=None,
        description="Optional GitHub profile URL",
        examples=["https://github.com/johnsmith"],
    )


class ProfileOut(ProfileCreate):
    """
    Response schema returned after a Profile is created or fetched.

    Extends ProfileCreate with server-generated metadata.
    """

    # Enables compatibility with ORM objects (SQLAlchemy models)
    model_config = ConfigDict(from_attributes=True)

    # Unique identifier assigned by the server
    id: str = Field(
        description="Unique profile identifier",
        examples=["prof_123456789"],
    )

    # Timestamp of profile creation (UTC)
    created_at: datetime = Field(
        description="Profile creation timestamp (UTC)",
        examples=["2025-01-01T12:00:00Z"],
    )


class SubmissionCreate(BaseModel):
    """
    Request schema for submitting a document for a Profile.

    A submission represents a single document upload attempt
    tied to an existing profile.
    """

    # Identifier of the profile this submission belongs to
    profile_id: str = Field(
        min_length=1,
        description="ID of the profile associated with this submission",
        examples=["prof_123456789"],
    )

    # Base64-encoded PDF content
    # (Used to keep transport simple and avoid multipart complexity)
    pdf_content: str = Field(
        min_length=1,
        description="Base64-encoded PDF document",
    )


class SubmissionOut(SubmissionCreate):
    """
    Response schema returned after a submission is created or queried.

    Extends SubmissionCreate with processing state and metadata.
    """

    # Enables compatibility with ORM objects (SQLAlchemy models)
    model_config = ConfigDict(from_attributes=True)

    # Unique submission identifier
    id: str = Field(
        description="Unique submission identifier",
        examples=["sub_abcdef123"],
    )

    # Current processing status of the submission
    status: str = Field(
        description="Current submission status",
        examples=["pending", "processing", "completed", "failed"],
    )

    # Timestamp of submission creation (UTC)
    created_at: datetime = Field(
        description="Submission creation timestamp (UTC)",
        examples=["2025-01-01T12:05:00Z"],
    )
