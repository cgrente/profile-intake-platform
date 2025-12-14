"""
Application entrypoint for the Profile Intake API.

This module is responsible for:
- initializing the FastAPI application
- creating database tables at startup
- registering API routes
- exposing a health check endpoint

It intentionally contains no business logic.
"""

from fastapi import FastAPI

from .routes import router
from .database import Base, engine


# Create all database tables on application startup.
#
# This is suitable for local development and demo environments.
# In production systems, schema migrations (e.g. Alembic)
# would typically be used instead.
Base.metadata.create_all(bind=engine)

# Instantiate the FastAPI application.
#
# The title is used in generated OpenAPI documentation
# and interactive API docs.
app = FastAPI(title="Profile Intake API")

# Register all API routes under their defined prefixes.
# Routing logic is kept in separate modules to maintain
# a clean separation of concerns.
app.include_router(router)


@app.get("/healthz")
def health():
    """
    Health check endpoint.

    Used by:
    - container orchestrators
    - load balancers
    - monitoring systems

    Returns a simple static response indicating
    that the service is running and responsive.
    """
    return {"ok": True}