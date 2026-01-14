"""
Validators Module
=================
Input validation functions for all tools.
"""

from .exceptions import ValidationError


# Supported couriers for domestic shipping
DOMESTIC_COURIERS = [
    "jne", "sicepat", "jnt", "pos", "tiki", "anteraja", "ninja",
    "lion", "ide", "sap", "ncs", "rex", "rpx", "sentral", "star",
    "wahana", "dse", "first", "indah", "kgx", "pandu"
]

# Supported couriers for international shipping
INTERNATIONAL_COURIERS = ["pos", "jne", "tiki", "pcp", "ems"]


def validate_query(query: str, min_length: int = 1) -> str:
    """
    Validate search query string.

    Args:
        query: The search query to validate.
        min_length: Minimum required length.

    Returns:
        Cleaned query string.

    Raises:
        ValidationError: If query is invalid.
    """
    if not query or not isinstance(query, str):
        raise ValidationError(
            message="Query cannot be empty",
            detail="Please provide a valid search query string.",
        )

    cleaned = query.strip()
    if len(cleaned) < min_length:
        raise ValidationError(
            message=f"Query must be at least {min_length} character(s)",
            detail=f"Your query '{query}' is too short.",
        )

    return cleaned


def validate_id(value: str | int, field_name: str = "ID") -> str:
    """
    Validate and convert ID to string.

    Args:
        value: The ID value to validate.
        field_name: Name of the field for error messages.

    Returns:
        ID as string.

    Raises:
        ValidationError: If ID is invalid.
    """
    if value is None:
        raise ValidationError(
            message=f"{field_name} cannot be empty",
            detail=f"Please provide a valid {field_name}.",
        )

    str_value = str(value).strip()
    if not str_value:
        raise ValidationError(
            message=f"{field_name} cannot be empty",
            detail=f"Please provide a valid {field_name}.",
        )

    # Check if it's a valid numeric ID
    if not str_value.isdigit():
        raise ValidationError(
            message=f"Invalid {field_name} format",
            detail=f"{field_name} must be a numeric value. Got: '{value}'",
        )

    return str_value


def validate_weight(weight: int) -> int:
    """
    Validate package weight in grams.

    Args:
        weight: Weight in grams.

    Returns:
        Validated weight.

    Raises:
        ValidationError: If weight is invalid.
    """
    if not isinstance(weight, int):
        try:
            weight = int(weight)
        except (ValueError, TypeError):
            raise ValidationError(
                message="Weight must be a number",
                detail=f"Got invalid weight value: '{weight}'",
            )

    if weight <= 0:
        raise ValidationError(
            message="Weight must be greater than 0",
            detail="Please provide a positive weight in grams.",
        )

    if weight > 500000:  # 500 kg max
        raise ValidationError(
            message="Weight exceeds maximum limit",
            detail="Maximum weight is 500,000 grams (500 kg).",
        )

    return weight


def validate_courier(
    courier: str,
    courier_type: str = "domestic",
) -> str:
    """
    Validate and normalize courier code(s).

    Args:
        courier: Courier code(s), can be colon-separated for multiple.
        courier_type: Either 'domestic' or 'international'.

    Returns:
        Normalized courier code(s).

    Raises:
        ValidationError: If courier is invalid.
    """
    if not courier or not isinstance(courier, str):
        raise ValidationError(
            message="Courier cannot be empty",
            detail="Please provide a valid courier code.",
        )

    cleaned = courier.strip().lower()
    if not cleaned:
        raise ValidationError(
            message="Courier cannot be empty",
            detail="Please provide a valid courier code.",
        )

    # Split by colon for multiple couriers
    courier_list = [c.strip() for c in cleaned.split(":") if c.strip()]

    if not courier_list:
        raise ValidationError(
            message="No valid courier codes provided",
            detail="Please provide at least one valid courier code.",
        )

    # Validate each courier
    valid_couriers = DOMESTIC_COURIERS if courier_type == "domestic" else INTERNATIONAL_COURIERS

    invalid_couriers = [c for c in courier_list if c not in valid_couriers]
    if invalid_couriers:
        raise ValidationError(
            message=f"Invalid courier code(s): {', '.join(invalid_couriers)}",
            detail=f"Valid {courier_type} couriers: {', '.join(valid_couriers)}",
        )

    return ":".join(courier_list)


def validate_awb(awb: str) -> str:
    """
    Validate AWB (Air Waybill) / tracking number.

    Args:
        awb: The tracking number to validate.

    Returns:
        Cleaned AWB string.

    Raises:
        ValidationError: If AWB is invalid.
    """
    if not awb or not isinstance(awb, str):
        raise ValidationError(
            message="AWB/tracking number cannot be empty",
            detail="Please provide a valid tracking number.",
        )

    cleaned = awb.strip()
    if len(cleaned) < 5:
        raise ValidationError(
            message="AWB/tracking number is too short",
            detail="Tracking number must be at least 5 characters.",
        )

    if len(cleaned) > 50:
        raise ValidationError(
            message="AWB/tracking number is too long",
            detail="Tracking number must be at most 50 characters.",
        )

    return cleaned
