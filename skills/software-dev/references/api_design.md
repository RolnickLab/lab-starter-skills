# API Design & Architecture Standards

This document serves as the authoritative guide for designing robust, scalable, and developer-friendly APIs.

## 1. Interface Design Patterns

### REST (Representational State Transfer)
Use REST for public-facing APIs or resource-oriented internal services.

*   **Resources:** Nouns, plural (e.g., `/users`, not `/getUsers`).
*   **Hierarchy:** `/users/{id}/posts` (User's posts). Avoid > 2 levels of nesting.
*   **Filtering/Pagination:**
    *   `GET /users?role=admin&limit=20&offset=40`
    *   `GET /users?sort=-created_at` (descending)
*   **Versioning:** URI Versioning is preferred for clarity. `/v1/users`.

## 2. HTTP Status Code Guide

| Status | Name | Meaning | Use Case |
| :--- | :--- | :--- | :--- |
| **200** | OK | Success | Standard synchronous success. |
| **201** | Created | Created | Result of `POST` creating a resource. Must return `Location` header. |
| **202** | Accepted | Processing | Async task started (e.g., "Video processing started"). |
| **204** | No Content | Success (Empty) | `DELETE` success or `PUT` where no data is returned. |
| **400** | Bad Request | Client Error | Validation failed (e.g., missing field). |
| **401** | Unauthorized | Authentication | No token or invalid token. |
| **403** | Forbidden | Authorization | Valid token, but not allowed (Scopes/RBAC). |
| **404** | Not Found | Not Found | Resource doesn't exist. |
| **409** | Conflict | Conflict | Duplicate entry (Unique constraint). |
| **429** | Too Many Requests | Rate Limited | Slow down. |
| **500** | Internal Error | Server Bug | Unhandled exception. Log immediately. |

## 3. Security & Safety

### Authentication & Authorization
*   **Stateless:** Use JWT (JSON Web Tokens) for auth state.
*   **Headers:** `Authorization: Bearer <token>`.
*   **Scopes:** Granular permissions (`read:users`, `write:billing`).

### Input Validation
Never trust the client.
*   **Sanitization:** Strip HTML tags to prevent XSS.
*   **Typing:** Ensure IDs are integers/UUIDs.
*   **Libraries:** Use Pydantic (Python), Zod (TS), or Go Validator.

## 4. Idempotency
Critical for distributed systems (network retries).

*   `GET`, `PUT`, `DELETE`: Must be idempotent by definition.
*   `POST`: Not idempotent.
    *   **Pattern:** Client generates a UUID `Idempotency-Key` header. Server caches the key + response. If retried, return cached response without re-processing.

## 5. Documentation (OpenAPI/Swagger)
Documentation must be:
1.  **Machine Readable:** OpenAPI 3.0+ JSON/YAML.
2.  **Complete:** Examples for Request Body and ALL Response codes (200, 400, 404, etc.).
3.  **Up-to-Date:** Generated from code (FastAPI/NestJS) is safer than manually written.

## 6. Error Responses
Standardize error bodies. Don't return plain text.

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid email format",
    "details": [
      {
        "field": "email",
        "issue": "must contain @"
      }
    ],
    "request_id": "req_12345"
  }
}
```
