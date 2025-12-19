# Use a slim Python base image to minimize image size and attack surface.
# Python 3.12 is aligned with the project’s runtime and CI configuration.
FROM python:3.12-slim

# Set the working directory inside the container.
# All subsequent paths are relative to this directory.
WORKDIR /app

# Copy dependency metadata first.
# Doing this before copying application code allows Docker
# to cache dependency installation layers when code changes.
COPY pyproject.toml .

# Install runtime dependencies.
#
# Only required production dependencies are installed here to keep
# the image small and avoid shipping dev/test tooling.
# (In larger projects, this step could be replaced with a lockfile.)
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    sqlalchemy \
    python-multipart \
    pydantic-settings \
    email-validator

# Copy the application source code into the container.
COPY app app

# Expose the application via Uvicorn.
#
# - Binds to 0.0.0.0 so the service is accessible outside the container
# - Uses port 8000, the standard FastAPI/Uvicorn default
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
