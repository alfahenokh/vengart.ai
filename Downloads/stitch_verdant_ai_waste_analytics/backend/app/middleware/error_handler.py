"""
Error Handler Middleware
Catches and handles exceptions globally
"""
import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle exceptions globally"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except ValidationError as exc:
            # Handle Pydantic validation errors
            request_id = getattr(request.state, "request_id", "unknown")
            logger.error(
                f"Validation error: {exc}",
                extra={"request_id": request_id, "error": str(exc)}
            )
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "error": "Validation Error",
                    "details": exc.errors(),
                    "request_id": request_id,
                }
            )
        except SQLAlchemyError as exc:
            # Handle database errors
            request_id = getattr(request.state, "request_id", "unknown")
            logger.error(
                f"Database error: {exc}",
                extra={"request_id": request_id, "error": str(exc)}
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Database Error",
                    "message": "An internal database error occurred",
                    "request_id": request_id,
                }
            )
        except Exception as exc:
            # Handle all other exceptions
            request_id = getattr(request.state, "request_id", "unknown")
            logger.exception(
                f"Unhandled exception: {exc}",
                extra={"request_id": request_id, "error": str(exc)}
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred",
                    "request_id": request_id,
                }
            )
