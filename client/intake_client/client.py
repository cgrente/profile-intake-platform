"""
Typed HTTP client for interacting with the Profile Intake API.

This client acts as a thin SDK layer over the REST API, encapsulating
request construction, authentication headers, and endpoint paths.

Design principles:
- Keep business logic on the server
- Keep this client stateless and reusable
- Use a shared HTTP session for efficiency
- Return raw API responses to allow flexible consumption
"""

import requests


class IntakeClient:
    """
    Client for the Profile Intake API.

    This class provides a small, explicit interface over the API endpoints
    without embedding CLI concerns, retries, or output formatting.
    Those concerns are intentionally handled by higher-level layers
    (e.g. CLI, scripts, or applications).

    The client is designed to be:
    - easy to mock in tests
    - reusable across scripts and tools
    - explicit in its behavior
    """

    def __init__(self, base_url: str, token: str):
        """
        Initialize the API client.

        Args:
            base_url: Base URL of the API (e.g. http://localhost:8000/api/v1)
            token: Bearer token used for API authentication

        Notes:
            A requests.Session is used to:
            - reuse TCP connections
            - apply default headers once
            - improve performance for multiple calls
        """
        self.session = requests.Session()

        # Attach Authorization header once at construction time
        # to avoid repeating it for every request.
        self.session.headers["Authorization"] = f"Bearer {token}"

        # Store base URL separately to keep endpoint construction explicit.
        self.base_url = base_url.rstrip("/")

    def create_profile(self, payload: dict) -> dict:
        """
        Create a new profile resource.

        Args:
            payload: Dictionary containing profile attributes
                     (first_name, last_name, email, github_url)

        Returns:
            Parsed JSON response representing the created profile.
        """
        response = self.session.post(
            f"{self.base_url}/profiles",
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    def upload_pdf(self, profile_id: str, path: str) -> dict:
        """
        Upload a PDF document associated with a profile.

        Args:
            profile_id: Identifier of the profile to associate the document with
            path: Filesystem path to the PDF file

        Returns:
            Parsed JSON response representing the created submission.

        Notes:
            - File handling is kept minimal and explicit
            - The server enforces PDF-only validation
        """
        with open(path, "rb") as f:
            response = self.session.post(
                f"{self.base_url}/submissions",
                params={"profile_id": profile_id},
                files={"file": f},
            )

        response.raise_for_status()
        return response.json()

    def submit(self, submission_id: str) -> dict:
        """
        Submit an uploaded document for processing.

        Args:
            submission_id: Identifier of the submission to submit

        Returns:
            Parsed JSON response representing the updated submission.
        """
        response = self.session.post(f"{self.base_url}/submissions/{submission_id}/submit")
        response.raise_for_status()
        return response.json()

    def status(self, submission_id: str) -> dict:
        """
        Retrieve the current status of a submission.

        Args:
            submission_id: Identifier of the submission

        Returns:
            Parsed JSON response containing the submission status
            and associated metadata.
        """
        response = self.session.get(f"{self.base_url}/submissions/{submission_id}")
        response.raise_for_status()
        return response.json()
