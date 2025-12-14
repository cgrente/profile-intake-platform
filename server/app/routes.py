"""
API route definitions for the Profile Intake service.

This module defines all HTTP endpoints exposed by the service.
Routes are intentionally kept thin: they handle request/response
concerns and delegate business logic to other layers where possible.
"""

import os
import shutil
import time

from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from .auth import require_auth
from .database import SessionLocal
from .models import Profile, Submission

# Router instance for versioned API endpoints.
# All routes in this module are prefixed with `/api/v1`.
router = APIRouter(prefix="/api/v1")


def get_db():
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


@router.post("/profiles")
def create_profile(
    payload: dict,
    db: Session = Depends(get_db),
    _=Depends(require_auth),
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

    return profile


@router.post("/submissions")
def upload_submission(
    profile_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(require_auth),
):
    """
    Upload a document associated with a profile.

    Only PDF files are accepted. A new Submission entity is created
    with an initial status of `UPLOADED`.
    """
    # Enforce server-side validation of file type.
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    submission = Submission(
        profile_id=profile_id,
        filename=file.filename,
    )
    db.add(submission)
    db.commit()

    # Persist the uploaded file to disk using the submission ID
    # as a stable, collision-free filename.
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{submission.id}.pdf"

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return submission


@router.post("/submissions/{submission_id}/submit")
def submit(
    submission_id: str,
    bg: BackgroundTasks,
    db: Session = Depends(get_db),
    _=Depends(require_auth),
):
    """
    Submit an uploaded document for processing.

    Once submitted, the submission is locked and enters
    asynchronous processing. Re-submission is not allowed.
    """
    submission = db.get(Submission, submission_id)

    if submission.locked:
        raise ValueError("Submission has already been submitted")

    submission.locked = True
    submission.status = "PROCESSING"
    db.commit()

    # Trigger asynchronous processing without blocking
    # the HTTP request lifecycle.
    bg.add_task(process_submission, submission_id)

    return submission


@router.get("/submissions/{submission_id}")
def status(
    submission_id: str,
    db: Session = Depends(get_db),
    _=Depends(require_auth),
):
    """
    Retrieve the current status of a submission.

    Returns the full submission resource, including its
    lifecycle status and metadata.
    """
    return db.get(Submission, submission_id)


def process_submission(submission_id: str):
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
        submission.status = "COMPLETED"
        db.commit()
    finally:
        db.close()
