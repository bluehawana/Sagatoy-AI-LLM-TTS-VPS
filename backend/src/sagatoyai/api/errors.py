"""Error handling and response models."""

import logging
from typing import Optional

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ErrorResponse(BaseModel):
    """Standard error response format."""

    error: bool = True
    error_code: str
    error_message: str
    fallback_audio_url: Optional[str] = None
    retry_after: Optional[int] = None


def setup_error_handlers(app: FastAPI) -> None:
    """Configure global error handlers for the application."""

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle unexpected exceptions."""
        logger.error(
            "Unhandled exception",
            extra={
                "error_type": type(exc).__name__,
                "error_message": str(exc),
                "path": request.url.path,
                "method": request.method,
            },
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                error_code="INTERNAL_ERROR",
                error_message="Oops! Something went wrong. Please try again.",
            ).model_dump(),
        )
