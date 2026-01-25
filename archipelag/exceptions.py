"""
Archipelag SDK Exceptions

Custom exception classes for error handling.
"""

from typing import Any, Optional


class ArchipelagError(Exception):
    """Base exception for all Archipelag SDK errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[Any] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(ArchipelagError):
    """Raised when authentication fails (invalid or missing API key)."""

    pass


class RateLimitError(ArchipelagError):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        **kwargs: Any,
    ):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class InsufficientCreditsError(ArchipelagError):
    """Raised when the account has insufficient credits."""

    def __init__(
        self,
        message: str = "Insufficient credits",
        required: Optional[float] = None,
        available: Optional[float] = None,
        **kwargs: Any,
    ):
        super().__init__(message, **kwargs)
        self.required = required
        self.available = available


class JobFailedError(ArchipelagError):
    """Raised when a job fails during execution."""

    def __init__(
        self,
        message: str,
        job_id: Optional[str] = None,
        error_code: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(message, **kwargs)
        self.job_id = job_id
        self.error_code = error_code


class NotFoundError(ArchipelagError):
    """Raised when a resource is not found."""

    pass


class ValidationError(ArchipelagError):
    """Raised when request validation fails."""

    def __init__(
        self,
        message: str,
        errors: Optional[dict[str, list[str]]] = None,
        **kwargs: Any,
    ):
        super().__init__(message, **kwargs)
        self.errors = errors or {}


class TimeoutError(ArchipelagError):
    """Raised when a request or job times out."""

    pass


class ConnectionError(ArchipelagError):
    """Raised when connection to the API fails."""

    pass
