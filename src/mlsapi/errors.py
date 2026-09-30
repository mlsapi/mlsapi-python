from __future__ import annotations

from typing import Any, Optional


class MlsApiError(Exception):
    """Base exception for all mlsapi.dev SDK errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        code: Optional[str] = None,
        raw_response: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code or "UNKNOWN_ERROR"
        self.raw_response = raw_response

    def __str__(self) -> str:
        parts = []
        if self.status_code:
            parts.append(f"HTTP {self.status_code}")
        if self.code and self.code != "UNKNOWN_ERROR":
            parts.append(f"[{self.code}]")
        parts.append(self.message)
        return " - ".join(parts)


class AuthenticationError(MlsApiError):
    """Raised on HTTP 401 when the provided API key is invalid, missing, or revoked."""


class PermissionDeniedError(MlsApiError):
    """Raised on HTTP 403 when the API key lacks necessary permissions or plan tier."""


class NotFoundError(MlsApiError):
    """Raised on HTTP 404 when the requested MLS listing, job, or resource is not found."""


class InvalidRequestError(MlsApiError):
    """Raised on HTTP 400 when request parameters are malformed or missing."""


class InsufficientCreditsError(MlsApiError):
    """Raised on HTTP 402 when workspace credit balance is insufficient for the requested action."""


class RateLimitError(MlsApiError):
    """Raised on HTTP 429 when concurrency or rate limits have been exceeded."""

    def __init__(
        self,
        message: str,
        status_code: int = 429,
        code: str = "RATE_LIMIT_EXCEEDED",
        retry_after_seconds: Optional[float] = None,
        raw_response: Optional[Any] = None,
    ) -> None:
        super().__init__(message, status_code, code, raw_response)
        self.retry_after_seconds = retry_after_seconds


class StudioJobFailedError(MlsApiError):
    """Raised when an asynchronous Studio AI job completes with a failed status."""

    def __init__(
        self,
        job_id: str,
        message: str,
        error_details: Optional[Any] = None,
    ) -> None:
        super().__init__(
            f"Studio job '{job_id}' failed: {message}",
            status_code=500,
            code="JOB_FAILED",
            raw_response=error_details,
        )
        self.job_id = job_id


class JobTimeoutError(MlsApiError):
    """Raised when polling for an asynchronous job exceeds the configured timeout."""

    def __init__(self, job_id: str, timeout_seconds: float) -> None:
        super().__init__(
            f"Job '{job_id}' did not complete within {timeout_seconds:.1f} seconds",
            status_code=408,
            code="JOB_TIMEOUT",
        )
        self.job_id = job_id
        self.timeout_seconds = timeout_seconds
