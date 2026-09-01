from typing import Any


class SoroushException(Exception):
    """Base exception class for all errors in aiosplus."""


class NetworkError(SoroushException):
    """Raised when a network-level error occurs (e.g. connection refused, timeout)."""

    def __init__(self, message: str, original_exception: Exception | None = None) -> None:
        super().__init__(message)
        self.original_exception = original_exception


class SoroushAPIError(SoroushException):
    """Base exception for errors returned by Soroush Plus Bot API."""

    def __init__(
        self,
        message: str,
        error_code: int = 400,
        description: str | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> None:
        self.error_code = error_code
        self.description = description or message
        self.parameters = parameters or {}
        super().__init__(f"[{error_code}] {self.description}")


class SoroushBadRequest(SoroushAPIError):
    """Raised when Soroush API returns 400 Bad Request."""


class SoroushUnauthorized(SoroushAPIError):
    """Raised when Soroush API returns 401 Unauthorized (invalid bot token)."""


class SoroushForbidden(SoroushAPIError):
    """Raised when Soroush API returns 403 Forbidden (e.g. bot blocked by user)."""


class SoroushNotFound(SoroushAPIError):
    """Raised when Soroush API returns 404 Not Found (chat/message not found)."""


class SoroushConflictError(SoroushAPIError):
    """Raised when Soroush API returns 409 Conflict (e.g. another instance is running)."""


class SoroushFloodError(SoroushAPIError):
    """Raised when Soroush API returns 429 Too Many Requests (rate limit exceeded)."""

    def __init__(
        self,
        message: str,
        error_code: int = 429,
        description: str | None = None,
        parameters: dict[str, Any] | None = None,
        retry_after: int | None = None,
    ) -> None:
        super().__init__(message, error_code, description, parameters)
        self.retry_after = retry_after or (parameters.get("retry_after") if parameters else None)


class SoroushServerError(SoroushAPIError):
    """Raised when Soroush API returns 5xx Internal Server Error."""


class RestartingUpdateError(SoroushAPIError):
    """Raised when updates cannot be retrieved because of server-side restarts."""


def create_api_error(
    status_code: int,
    description: str,
    parameters: dict[str, Any] | None = None,
) -> SoroushAPIError:
    """Factory to instantiate the appropriate SoroushAPIError subclass based on status code and description."""
    params = parameters or {}
    retry_after = params.get("retry_after")

    if status_code == 400:
        return SoroushBadRequest(
            description, error_code=status_code, description=description, parameters=params
        )
    if status_code == 401:
        return SoroushUnauthorized(
            description, error_code=status_code, description=description, parameters=params
        )
    if status_code == 403:
        return SoroushForbidden(
            description, error_code=status_code, description=description, parameters=params
        )
    if status_code == 404:
        return SoroushNotFound(
            description, error_code=status_code, description=description, parameters=params
        )
    if status_code == 409:
        return SoroushConflictError(
            description, error_code=status_code, description=description, parameters=params
        )
    if status_code == 429 or retry_after is not None:
        return SoroushFloodError(
            description,
            error_code=status_code,
            description=description,
            parameters=params,
            retry_after=retry_after,
        )
    if status_code >= 500:
        return SoroushServerError(
            description, error_code=status_code, description=description, parameters=params
        )

    return SoroushAPIError(
        description, error_code=status_code, description=description, parameters=params
    )
