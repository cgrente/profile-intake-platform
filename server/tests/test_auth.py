def test_requires_auth_missing_token(client):
    """
    Requests without an Authorization header should be rejected.

    Depending on FastAPI configuration, a missing required header
    may result in:
    - 401 Unauthorized (custom auth handling), or
    - 422 Unprocessable Entity (header validation failure)

    Both responses are acceptable as long as unauthenticated
    access is denied.
    """
    resp = client.post("/api/v1/profiles", json={})

    assert resp.status_code in (401, 422)


def test_requires_auth_invalid_token(client):
    """
    Requests with an invalid Bearer token should be rejected
    with a 401 Unauthorized response.
    """
    resp = client.post(
        "/api/v1/profiles",
        json={
            "first_name": "A",
            "last_name": "B",
            "email": "a@b.com",
            "github_url": "https://x.com",
        },
        headers={"Authorization": "Bearer wrong"},
    )

    assert resp.status_code == 401
