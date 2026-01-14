"""
Response Helper Module
======================
Standardized response formatting for all tools.
"""

from typing import Any


def success_response(
    data: Any,
    message: str | None = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create a standardized success response.

    Args:
        data: The response data.
        message: Optional success message.
        meta: Optional metadata (count, pagination, etc).

    Returns:
        Formatted success response dictionary.
    """
    response: dict[str, Any] = {
        "success": True,
        "data": data,
    }

    if message:
        response["message"] = message

    if meta:
        response["meta"] = meta

    return response


def error_response(
    code: str,
    message: str,
    detail: str | None = None,
) -> dict[str, Any]:
    """
    Create a standardized error response.

    Args:
        code: Error code (e.g., 'VALIDATION_ERROR', 'API_ERROR').
        message: Human-readable error message.
        detail: Optional detailed error description.

    Returns:
        Formatted error response dictionary.
    """
    error_data: dict[str, Any] = {
        "code": code,
        "message": message,
    }

    if detail:
        error_data["detail"] = detail

    return {
        "success": False,
        "error": error_data,
    }


def list_response(
    items: list[Any],
    item_name: str = "items",
) -> dict[str, Any]:
    """
    Create a standardized list response with count.

    Args:
        items: List of items.
        item_name: Name of the items for the message.

    Returns:
        Formatted list response with count metadata.
    """
    count = len(items)
    return success_response(
        data=items,
        message=f"Found {count} {item_name}",
        meta={"count": count},
    )


def extract_api_data(
    api_response: dict[str, Any],
    keys: list[str] | None = None,
) -> list[Any] | dict[str, Any]:
    """
    Extract data from API response, handling various response formats.

    Args:
        api_response: Raw API response dictionary.
        keys: List of possible keys to look for data (in priority order).

    Returns:
        Extracted data (list or dict).
    """
    if keys is None:
        keys = ["data", "results", "result"]

    # Try each key in priority order
    for key in keys:
        if key in api_response and api_response[key] is not None:
            return api_response[key]

    # If no known key found, return the whole response
    return api_response
