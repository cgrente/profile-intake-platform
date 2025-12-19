"""
Pydantic schemas for request and response validation.

These schemas power:
- request validation (Swagger request bodies)
- response validation (FastAPI response_model)
- accurate OpenAPI documentation
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ProfileCreate(BaseModel):
    """
    Request body for creating a Profile.
    """

    first_name: str = Field(min_length=1, description="Given name")
    last_name: str = Field(min_length=1, description="Family name")
    email: EmailStr = Field(description="Unique email address")
    github_url: str | None = Field(default=None, description="Optional GitHub profile URL")


class ProfileOut(ProfileCreate):
    """
    Response body for Profile resources.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(description="Profile UUID")
    created_at: datetime = Field(description="Server timestamp when the profile was created")


class SubmissionOut(BaseModel):
    """
    Response body for Submission resources.

    Note:
    - Upload is multipart/form-data, so there is no JSON request model for the file.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(description="Submission UUID")
    profile_id: str = Field(description="Owning Profile UUID")
    filename: str = Field(description="Original uploaded filename")
    status: str = Field(description="Submission lifecycle status")
    locked: bool = Field(description="True after /submit is called (prevents re-submission)")
    created_at: datetime = Field(description="Server timestamp when the submission was created")
