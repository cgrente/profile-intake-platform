"""
API route definitions for the Profile Intake service.

This module defines all HTTP endpoints exposed by the service.
Routes are intentionally kept thin: they handle request/response
concerns and delegate business logic to other layers where possible.
"""

from __future__ import annotations

import os
import shutil
import time
from typing import Generator

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from .auth import require_auth
from .config import settings
from .database import SessionLocal
from .models import Profile, Submission

# Router instance for versioned API endpoints.
# All routes in this module are prefixed with `/api/v1`.
router = APIRouter(prefix="/api/v1")


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency.

    Creates a new SQLAlchemy session per request and ensures
    it is properly closed once the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _ensure_pdf_upload(file: UploadFile) -> None:
    """
    Validate that the uploaded file is a PDF.

    We validate both the reported MIME type and the filename extension.
    Neither is perfect alone, but together they significantly reduce
    accidental non-PDF uploads without requiring heavy content inspection.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    filename = file.filename or ""
    _, ext = os.path.splitext(filename)
    if ext.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")


@router.post("/profiles")
def create_profile(
    payload: dict,
    db: Session = Depends(get_db),  # noqa: B008
    _: None = Depends(require_auth),  # noqa: B008
):
    """
    Create a new profile.

    Accepts basic identity and metadata information and persists
    it as a Profile entity.

    Authentication is enforced via dependency injection.
    """
    profile = Profile(**payload)
    db.add(profile)
    db.commit()
    db.refresh(profile)  # ensures generated fields (id) are available

    return profile


@router.post("/submissions")
def upload_submission(
    profile_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),  # noqa: B008
    _: None = Depends(require_auth),  # noqa: B008
):
    """
    Upload a PDF document associated with a profile.

    Only PDF files are accepted. A new Submission entity is created
    with an initial status of `UPLOADED`.
    """
    # Validate profile exists
    profile = db.get(Profile, profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    _ensure_pdf_upload(file)

    submission = Submission(
        profile_id=profile_id,
        filename=file.filename,
        status="UPLOADED",
        locked=False,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # Persist the uploaded file to disk using the submission ID
    # as a stable, collision-free filename.
    os.makedirs(settings.upload_dir, exist_ok=True)
    file_path = os.path.join(settings.upload_dir, f"{submission.id}.pdf")

    # Copy file stream to disk
    with open(file_path, "wb") as out_file:
        shutil.copyfileobj(file.file, out_file)

    return submission


@router.post("/submissions/{submission_id}/submit")
def submit(
    submission_id: str,
    bg: BackgroundTasks,
    db: Session = Depends(get_db),  # noqa: B008
    _: None = Depends(require_auth),  # noqa: B008
):
    """
    Submit an uploaded document for processing.

    Once submitted, the submission is locked and enters
    asynchronous processing. Re-submission is not allowed.
    """
    submission = db.get(Submission, submission_id)
    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")

    if submission.locked:
        raise HTTPException(status_code=409, detail="Submission has already been submitted")

    # NOTE: If your SQLAlchemy models are declared using `Column(...)` without
    # SQLAlchemy 2.0 `Mapped[...]` typing, mypy may treat attributes as `Column[T]`.
    # These assignments are correct at runtime; the ignores keep type-checking green
    # until models are migrated to `Mapped[...]`.
    submission.locked = True  # type: ignore[assignment]
    submission.status = "PROCESSING"  # type: ignore[assignment]

    db.commit()
    db.refresh(submission)

    # Trigger asynchronous processing without blocking
    # the HTTP request lifecycle.
    bg.add_task(process_submission, submission_id)

    return submission


@router.get("/submissions/{submission_id}")
def status(
    submission_id: str,
    db: Session = Depends(get_db),  # noqa: B008
    _: None = Depends(require_auth),  # noqa: B008
):
    """
    Retrieve the current status of a submission.

    Returns the full submission resource, including its
    lifecycle status and metadata.
    """
    submission = db.get(Submission, submission_id)
    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission


def process_submission(submission_id: str) -> None:
    """
    Background task to process a submission.

    This simulates asynchronous processing without introducing
    external infrastructure (e.g. message queues or workers).

    In a production system, this would typically be replaced by:
    - a task queue
    - a background worker
    - or an external processing service
    """
    # Simulate processing delay
    time.sleep(2)

    db = SessionLocal()
    try:
        submission = db.get(Submission, submission_id)
        if submission is None:
            return

        submission.status = "COMPLETED"  # type: ignore[assignment]
        db.commit()
    finally:
        db.close()
