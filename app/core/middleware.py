import time
import uuid
from collections.abc import Callable

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.gzip import GZipMiddleware
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.config import settings
from app.core.logging import logger


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add a unique request ID to each request."""

    async def dispatch(self, request: Request, call_next: Callable):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        response = await call_next(request)

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log request and response details."""

    async def dispatch(self, request: Request, call_next: Callable):
        # Log request
        start_time = time.time()

        # Skip logging for health checks and favicon
        if request.url.path in ["/health", "/favicon.ico"]:
            return await call_next(request)

        logger.info(
            f"Request started: {request.method} {request.url.path} "
            f"Client: {request.client.host if request.client else 'Unknown'}"
        )

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Request failed: {request.method} {request.url.path} - Error: {str(e)}")
            raise

        # Calculate processing time
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = f"{process_time:.2f}ms"

        # Log response
        logger.info(
            f"Request completed: {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Duration: {formatted_process_time}"
        )

        # Add processing time to response headers
        response.headers["X-Process-Time"] = formatted_process_time

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to responses."""

    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)

        # Security headers
        security_headers = {
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
        }

        # Add CSP in production
        if settings.ENVIRONMENT == "production":
            security_headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self'; "
                "media-src 'self'; "
                "object-src 'none'; "
                "frame-src 'none'; "
                "base-uri 'self'; "
                "form-action 'self';"
            )

        # Add all security headers
        for header, value in security_headers.items():
            response.headers[header] = value

        return response


class TimeoutMiddleware(BaseHTTPMiddleware):
    """Middleware to set a timeout for requests."""

    def __init__(self, app, timeout: int = 30):
        super().__init__(app)
        self.timeout = timeout

    async def dispatch(self, request: Request, call_next: Callable):
        # You could implement timeout logic here
        # For now, we'll just pass through
        # In production, consider using asyncio.timeout()
        return await call_next(request)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Basic rate limiting middleware."""

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_counts = {}

    async def dispatch(self, request: Request, call_next: Callable):
        # Skip rate limiting for certain paths
        if request.url.path in ["/health", "/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)

        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Simple rate limiting logic (in-memory, not for production use)
        # For production, use Redis or a dedicated rate limiting service
        current_time = int(time.time())
        minute_key = current_time // 60

        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = {}

        if minute_key not in self.request_counts[client_ip]:
            self.request_counts[client_ip][minute_key] = 0

        self.request_counts[client_ip][minute_key] += 1

        if self.request_counts[client_ip][minute_key] > self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded"
            )

        # Clean up old entries (older than 2 minutes)
        old_keys = [k for k in self.request_counts[client_ip] if k < minute_key - 1]
        for old_key in old_keys:
            del self.request_counts[client_ip][old_key]

        return await call_next(request)


class CustomCORSMiddleware(CORSMiddleware):
    """Custom CORS middleware with additional configuration."""

    async def dispatch(self, request: Request, call_next: Callable):
        # Add CORS headers for preflight requests
        if request.method == "OPTIONS":
            response = Response()
        else:
            response = await call_next(request)

        # Ensure CORS headers are set
        origin = request.headers.get("origin")
        if origin and origin in [str(o) for o in settings.BACKEND_CORS_ORIGINS]:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"

        return response


class RequestSizeMiddleware(BaseHTTPMiddleware):
    """Middleware to limit request body size."""

    def __init__(self, app, max_body_size: int = 10 * 1024 * 1024):  # 10MB default
        super().__init__(app)
        self.max_body_size = max_body_size

    async def dispatch(self, request: Request, call_next: Callable):
        # Check content-length header if present
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_body_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Request body too large. Max size is {self.max_body_size} bytes",
            )

        # For streaming requests, we could implement chunked reading
        # but that's more complex. For now, we rely on content-length.

        return await call_next(request)


class CacheControlMiddleware(BaseHTTPMiddleware):
    """Middleware to add cache control headers."""

    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)

        # Don't cache API responses by default
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

        return response


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to catch and format unhandled exceptions."""

    async def dispatch(self, request: Request, call_next: Callable):
        try:
            return await call_next(request)
        except Exception as exc:
            # Log the error
            logger.error(
                f"Unhandled exception: {exc}",
                exc_info=True,
                extra={
                    "path": request.url.path,
                    "method": request.method,
                    "client": request.client.host if request.client else "unknown",
                },
            )

            # Re-raise the exception (FastAPI will handle it)
            raise


def setup_middleware(app: FastAPI):
    """we configure all middleware for the application."""

    # Add security headers middleware
    app.add_middleware(SecurityHeadersMiddleware)

    # Add request ID middleware
    app.add_middleware(RequestIDMiddleware)

    # Add logging middleware
    app.add_middleware(LoggingMiddleware)

    # Add error handler middleware
    app.add_middleware(ErrorHandlerMiddleware)

    # Add cache control middleware
    app.add_middleware(CacheControlMiddleware)

    # Add request size limiting middleware
    app.add_middleware(RequestSizeMiddleware, max_body_size=10 * 1024 * 1024)  # 10MB

    # Add GZIP compression for responses
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Add trusted hosts middleware in production
    if settings.ENVIRONMENT == "production":
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS.split(",")
            if hasattr(settings, "ALLOWED_HOSTS")
            else ["*"],
        )

    # Note: CORS middleware is already added in main.py
    # Note: Rate limiting is commented out by default - enable if needed
    # app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

    logger.info("Middleware setup complete")
