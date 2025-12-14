"""
Command-line interface (CLI) for the Profile Intake Platform.

This module provides a thin CLI wrapper around the IntakeClient SDK.
It is intentionally kept lightweight: argument parsing, environment
configuration, and human-readable output formatting live here, while
all HTTP/business logic remains in the client layer.

Design goals:
- Clear separation between SDK and CLI
- Environment-based configuration (no hardcoded secrets)
- JSON output by default (machine- and human-friendly)
"""

import json
import os
import typer

from intake_client.client import IntakeClient

# Typer application instance.
# This defines the root CLI command group (e.g. `intake <command>`).
app = typer.Typer(help="Profile Intake CLI")


def get_client() -> IntakeClient:
    """
    Construct and return an IntakeClient using environment configuration.

    Configuration is intentionally read from environment variables to:
    - avoid hardcoding secrets
    - mirror common production/CI deployment patterns
    - keep CLI usage consistent across environments

    Required environment variables:
    - INTAKE_API_TOKEN: Bearer token for API authentication

    Optional environment variables:
    - INTAKE_API_URL: Base URL of the API (defaults to local server)

    Raises:
        typer.BadParameter: if required configuration is missing
    """
    base_url = os.getenv("INTAKE_API_URL", "http://localhost:8000/api/v1")
    token = os.getenv("INTAKE_API_TOKEN")

    if not token:
        # Typer-specific exception to produce a clean CLI error message
        # instead of a Python traceback.
        raise typer.BadParameter(
            "Missing INTAKE_API_TOKEN environment variable"
        )

    return IntakeClient(base_url=base_url, token=token)


@app.command()
def create_profile(
    first_name: str,
    last_name: str,
    email: str,
    github_url: str,
):
    """
    Create a new profile in the intake system.

    This command submits basic identity and metadata information
    to the API and returns the created profile resource.

    Example:
        intake create-profile \
            --first-name Joel \
            --last-name Grente \
            --email cgrente@gmail.com \
            --github-url https://github.com/cgrente
    """
    client = get_client()

    # Build the payload explicitly to keep CLI parameters decoupled
    # from the underlying API schema.
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "github_url": github_url,
    }

    result = client.create_profile(payload)

    # Output formatted JSON so results are easy to read
    # and can be piped into other tools if needed.
    typer.echo(json.dumps(result, indent=2))


@app.command()
def upload(
    profile_id: str,
    file: str = typer.Argument(..., help="Path to PDF file"),
):
    """
    Upload a PDF document for an existing profile.

    The API enforces PDF-only uploads and associates the document
    with the provided profile ID.

    Example:
        intake upload <profile_id> ./resume.pdf
    """
    client = get_client()
    result = client.upload_pdf(profile_id, file)
    typer.echo(json.dumps(result, indent=2))


@app.command()
def submit(
    submission_id: str,
):
    """
    Submit an uploaded document for processing.

    Once submitted, the submission becomes locked and enters
    asynchronous processing. Re-submission is not allowed.

    Example:
        intake submit <submission_id>
    """
    client = get_client()
    result = client.submit(submission_id)
    typer.echo(json.dumps(result, indent=2))


@app.command()
def status(
    submission_id: str,
):
    """
    Retrieve the current status of a submission.

    Possible statuses typically include:
    - UPLOADED
    - PROCESSING
    - COMPLETED
    - REJECTED

    Example:
        intake status <submission_id>
    """
    client = get_client()
    result = client.status(submission_id)
    typer.echo(json.dumps(result, indent=2))


def main():
    """
    CLI entrypoint.

    This function is exposed via the project’s console script
    configuration so users can invoke the CLI as a standalone
    command (e.g. `intake ...`).
    """
    app()


if __name__ == "__main__":
    main()