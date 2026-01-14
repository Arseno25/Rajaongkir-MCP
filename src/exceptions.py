"""
Custom Exceptions Module
========================
Application-specific exceptions for structured error handling.
"""

from typing import Any


class RajaOngkirError(Exception):
    """Base exception for RajaOngkir API errors."""

    def __init__(
        self,
        message: str,
        detail: str | None = None,
        code: str | None = None,
    ) -> None:
        self.message = message
        self.detail = detail
        self.code = code or "UNKNOWN_ERROR"
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for API response."""
        return {
            "success": False,
            "error": {
                "code": self.code,
                "message": self.message,
                "detail": self.detail,
            },
        }


class ConfigurationError(RajaOngkirError):
    """Raised when configuration is missing or invalid."""

    def __init__(self, message: str, detail: str | None = None) -> None:
        super().__init__(message, detail, code="CONFIG_ERROR")


class ValidationError(RajaOngkirError):
    """Raised when input validation fails."""

    def __init__(self, message: str, detail: str | None = None) -> None:
        super().__init__(message, detail, code="VALIDATION_ERROR")


class APIError(RajaOngkirError):
    """Raised when API request fails."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        detail: str | None = None,
    ) -> None:
        self.status_code = status_code
        code = f"API_ERROR_{status_code}" if status_code else "API_ERROR"
        super().__init__(message, detail, code=code)


class NetworkError(RajaOngkirError):
    """Raised when network request fails."""

    def __init__(self, message: str, detail: str | None = None) -> None:
        super().__init__(message, detail, code="NETWORK_ERROR")


class DataNotFoundError(RajaOngkirError):
    """Raised when requested data is not found."""

    def __init__(self, message: str, detail: str | None = None) -> None:
        super().__init__(message, detail, code="NOT_FOUND")
