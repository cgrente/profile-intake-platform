def test_healthz_ok(client):
    """
    The health check endpoint should respond successfully.

    This test verifies that:
    - the service is reachable
    - the application has started correctly
    - no authentication is required for basic health probing

    Health endpoints are typically used by load balancers,
    container orchestrators, and monitoring systems.
    """
    resp = client.get("/healthz")

    assert resp.status_code == 200
    assert resp.json().get("ok") is True