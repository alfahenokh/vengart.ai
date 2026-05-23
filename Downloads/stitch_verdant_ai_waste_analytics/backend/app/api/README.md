# Verdant AI Integrated Dashboard - API Structure

## Overview

This directory contains the FastAPI application structure with versioned API endpoints, middleware, and routing configuration.

## Directory Structure

```
app/api/
├── __init__.py
├── README.md
└── v1/
    ├── __init__.py
    ├── api.py              # Main API router aggregator
    └── endpoints/
        ├── __init__.py
        ├── health.py       # Health and status endpoints
        ├── auth.py         # Authentication endpoints (to be created)
        ├── dashboard.py    # Dashboard data endpoints (to be created)
        ├── analytics.py    # Analytics endpoints (to be created)
        ├── simulation.py   # Simulation endpoints (to be created)
        └── resources.py    # Resource management endpoints (to be created)
```

## API Versioning

All API endpoints are versioned under `/api/v1/` prefix. This allows for future API versions without breaking existing clients.

### Available Endpoints

#### Health & Status
- `GET /api/v1/health` - API health check
- `GET /api/v1/status` - Detailed API status information

#### Future Endpoints (to be implemented)
- `/api/v1/auth/*` - Authentication and authorization
- `/api/v1/dashboard/*` - Master dashboard data
- `/api/v1/analytics/*` - Analytics and reporting
- `/api/v1/simulation/*` - Operational simulator
- `/api/v1/resources/*` - Resource management

## Middleware Stack

The application uses the following middleware (executed in order):

1. **RequestIDMiddleware** - Adds unique request ID to each request
2. **LoggingMiddleware** - Logs all requests and responses
3. **ErrorHandlerMiddleware** - Global exception handling
4. **CORSMiddleware** - Cross-Origin Resource Sharing configuration

### Request Flow

```
Client Request
    ↓
CORS Middleware (allow origins, credentials, methods, headers)
    ↓
RequestID Middleware (generate UUID, add to request state)
    ↓
Logging Middleware (log incoming request)
    ↓
Error Handler Middleware (catch exceptions)
    ↓
Route Handler (process request)
    ↓
Response (with X-Request-ID and X-Process-Time headers)
    ↓
Client Response
```

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:3000` (React default)
- `http://127.0.0.1:3000`
- `http://localhost:5173` (Vite default)
- `http://127.0.0.1:5173`

All HTTP methods and headers are allowed for development. In production, these should be restricted to specific origins.

## Response Headers

All API responses include:
- `X-Request-ID` - Unique identifier for request tracing
- `X-Process-Time` - Request processing time in seconds

## Error Handling

The API uses standardized error responses:

```json
{
  "error": "Error Type",
  "message": "Human-readable error message",
  "details": {},  // Optional additional details
  "request_id": "uuid"
}
```

### HTTP Status Codes

- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `429` - Rate Limit Exceeded
- `500` - Internal Server Error

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`
- OpenAPI JSON: `http://localhost:8000/api/openapi.json`

## Adding New Endpoints

To add new endpoints:

1. Create a new router file in `app/api/v1/endpoints/`
2. Define your endpoints using FastAPI's `APIRouter`
3. Import and include the router in `app/api/v1/api.py`

Example:

```python
# app/api/v1/endpoints/example.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/items")
async def get_items():
    return {"items": []}
```

```python
# app/api/v1/api.py
from .endpoints import example

api_router.include_router(example.router, prefix="/example", tags=["example"])
```

## Requirements Validation

This API structure validates:
- **Requirement 3.1**: RESTful endpoints with proper HTTP methods
- **Requirement 3.4**: Proper error handling with HTTP status codes
- **Requirement 12.3**: Health check endpoints for monitoring

## Next Steps

The following routers need to be implemented in subsequent tasks:
1. Authentication router (Task 3.1)
2. Dashboard router (Task 6.2)
3. Analytics router (Task 6.3)
4. Simulation router (Task 6.3)
5. Resources router (Task 6.4)
