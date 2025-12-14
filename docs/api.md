# Profile Intake Platform – API Documentation

This document describes the public REST API exposed by the **Profile Intake Platform**.
The API supports profile submission, PDF document upload, submission locking, and
asynchronous processing with status tracking.

All endpoints are versioned under `/api/v1`.

---

## Authentication

All endpoints require Bearer token authentication.

### Header

```
Authorization: Bearer <API_TOKEN>
```

Requests without a valid token will receive a `401 Unauthorized` response.

---

## Base URL

```
http://localhost:8000/api/v1
```

---

## Endpoints

### Health Check

**GET** `/healthz`

Used for service health monitoring.

**Response**
```json
{
  "ok": true
}
```

---

## Profiles

### Create Profile

**POST** `/profiles`

Creates a new profile resource.

**Request Body**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "email": "john.smith@test.com",
  "github_url": "github.com/johnsmith"
}
```

**Response**
```json
{
  "id": "uuid",
  "first_name": "John",
  "last_name": "Smith",
  "email": "john.smith@test.com",
  "github_url": "github.com/johnsmith"
}
```

---

## Submissions

### Upload Document

**POST** `/submissions`

Uploads a PDF document associated with a profile.

**Query Parameters**
- `profile_id` (string, required)

**Form Data**
- `file` (PDF only)

**Response**
```json
{
  "id": "uuid",
  "profile_id": "uuid",
  "status": "UPLOADED"
}
```

---

### Submit Document

**POST** `/submissions/{submission_id}/submit`

Locks the submission and starts asynchronous processing.

**Response**
```json
{
  "id": "uuid",
  "status": "PROCESSING",
  "locked": true
}
```

---

### Get Submission Status

**GET** `/submissions/{submission_id}`

Returns the current submission status.

**Response**
```json
{
  "id": "uuid",
  "status": "COMPLETED",
  "locked": true
}
```

---

## Status Lifecycle

Submissions move through the following states:

- `UPLOADED`
- `PROCESSING`
- `COMPLETED`
- `REJECTED`

Once a submission is locked, it cannot be resubmitted.

---

## Error Responses

| Status Code | Description |
|-----------|-------------|
| 400 | Invalid request (e.g. non-PDF upload) |
| 401 | Unauthorized |
| 404 | Resource not found |
| 409 | Invalid state transition |
| 500 | Internal server error |

---

## Notes

- All responses are JSON
- PDF validation is enforced server-side
- Processing is asynchronous but simulated for demo purposes

