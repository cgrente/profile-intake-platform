def test_reject_non_pdf(client, auth_headers):
    """
    The API should reject uploads that are not valid PDF files.

    This test verifies that server-side validation is enforced
    regardless of file name or client behavior.
    """
    # Step 1: Create a valid profile to associate the submission with
    profile_payload = {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@test.com",
        "github_url": "https://github.com/johnsmith",
    }

    r1 = client.post(
        "/api/v1/profiles",
        json=profile_payload,
        headers=auth_headers,
    )

    assert r1.status_code in (200, 201)
    profile_id = r1.json()["id"]

    # Step 2: Attempt to upload a non-PDF file while pretending it is valid.
    # The content type and file signature indicate a PNG file.
    files = {
        "file": ("img.png", b"\x89PNG\r\n\x1a\nfake", "image/png"),
    }

    r2 = client.post(
        "/api/v1/submissions",
        params={"profile_id": profile_id},
        files=files,
        headers=auth_headers,
    )

    # The server should reject invalid file types.
    # Depending on implementation details, this may return:
    # - 400 Bad Request (explicit validation failure), or
    # - 422 Unprocessable Entity (request validation error)
    assert r2.status_code in (400, 422)
