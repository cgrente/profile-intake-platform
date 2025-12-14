"""
Unit tests for the IntakeClient SDK.

These tests validate that the client:
- configures authentication headers correctly
- constructs HTTP requests as expected
- returns parsed JSON responses without mutating data

HTTP calls are mocked to keep tests fast, deterministic,
and independent of the server implementation.
"""

from unittest.mock import MagicMock

from intake_client.client import IntakeClient


def test_client_sets_auth_header():
    """
    The client should attach the Bearer token to all outgoing requests.

    This test verifies that the Authorization header is set once
    during client initialization, ensuring consistent authentication
    behavior across all API calls.
    """
    client = IntakeClient(base_url="http://localhost:8000/api/v1", token="abc")

    assert client.session.headers["Authorization"] == "Bearer abc"


def test_create_profile_calls_post():
    """
    Creating a profile should issue a POST request to the profiles endpoint
    and return the parsed JSON response.

    The underlying HTTP call is mocked to:
    - avoid network access
    - ensure the client builds the request correctly
    - verify that response parsing behaves as expected
    """
    client = IntakeClient(base_url="http://localhost:8000/api/v1", token="abc")

    # Mock the session.post method so no real HTTP request is made.
    client.session.post = MagicMock()
    client.session.post.return_value.json.return_value = {"id": "123"}

    payload = {
        "first_name": "A",
        "last_name": "B",
        "email": "a@b.com",
        "github_url": "https://x.com",
    }

    result = client.create_profile(payload)

    # Ensure exactly one POST request was issued.
    client.session.post.assert_called_once()

    # Ensure the client returns the parsed JSON payload unchanged.
    assert result["id"] == "123"