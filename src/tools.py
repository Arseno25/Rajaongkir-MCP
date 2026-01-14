"""
MCP Tools Module
================
MCP tool definitions for RajaOngkir Komerce API V2.

Tools are organized into 3 categories:
1. Search Method - Quick search for locations
2. Step-by-Step Method - Hierarchical location selection
3. Tracking - Package tracking
"""

from typing import Any

from .client import api_client
from .exceptions import RajaOngkirError
from .response import error_response, extract_api_data, list_response, success_response
from .validators import (
    validate_awb,
    validate_courier,
    validate_id,
    validate_query,
    validate_weight,
)


def _handle_error(e: Exception) -> dict[str, Any]:
    """Convert exception to error response."""
    if isinstance(e, RajaOngkirError):
        return e.to_dict()
    return error_response(
        code="UNEXPECTED_ERROR",
        message="An unexpected error occurred",
        detail=str(e),
    )


# ============================================================================
# SEARCH METHOD TOOLS
# ============================================================================

async def search_domestic_destination(query: str) -> dict[str, Any]:
    """
    Search for domestic destinations (cities/districts) in Indonesia.

    Args:
        query: Location name to search (minimum 1 character).

    Returns:
        List of matching locations with id, name, province, and postal code.

    Example:
        >>> await search_domestic_destination("Jakarta")
    """
    try:
        # Validate input
        validated_query = validate_query(query, min_length=1)

        # Make API request
        api_response = await api_client.search_domestic_destination(
            query=validated_query,
            limit=20,
            offset=0,
        )

        # Extract and format response
        data = extract_api_data(api_response)
        if isinstance(data, list):
            return list_response(data, "domestic destinations")
        return success_response(data)

    except Exception as e:
        return _handle_error(e)


async def search_international_destination(query: str) -> dict[str, Any]:
    """
    Search for international destinations (countries).

    Args:
        query: Country name to search (minimum 1 character).

    Returns:
        List of matching countries with id and country name.

    Example:
        >>> await search_international_destination("Singapore")
    """
    try:
        # Validate input
        validated_query = validate_query(query, min_length=1)

        # Make API request
        api_response = await api_client.search_international_destination(
            query=validated_query,
            limit=20,
            offset=0,
        )

        # Extract and format response
        data = extract_api_data(api_response)
        if isinstance(data, list):
            return list_response(data, "international destinations")
        return success_response(data)

    except Exception as e:
        return _handle_error(e)


# ============================================================================
# STEP-BY-STEP METHOD TOOLS (Hierarchical Location Selection)
# Flow: Province → City → District → Subdistrict → Calculate Cost
# ============================================================================

async def get_provinces() -> dict[str, Any]:
    """
    Get all Indonesian provinces.

    This is Step 1 in the hierarchical location selection.
    Use the province_id from results to call get_cities().

    Returns:
        List of all provinces with province_id and province name.

    Example:
        >>> provinces = await get_provinces()
        >>> # Use province_id to get cities:
        >>> cities = await get_cities("6")  # DKI Jakarta
    """
    try:
        api_response = await api_client.get_provinces()
        data = extract_api_data(api_response)
        if isinstance(data, list):
            return list_response(data, "provinces")
        return success_response(data)

    except Exception as e:
        return _handle_error(e)


async def get_cities(province_id: str) -> dict[str, Any]:
    """
    Get all cities/regencies within a province.

    This is Step 2 in the hierarchical location selection.
    Requires province_id from get_provinces().
    Use the city_id from results to call get_districts().

    Args:
        province_id: Province ID from get_provinces().

    Returns:
        List of cities within the province.

    Example:
        >>> cities = await get_cities("6")  # DKI Jakarta
        >>> # Use city_id to get districts:
        >>> districts = await get_districts("152")
    """
    try:
        # Validate input
        validated_id = validate_id(province_id, "Province ID")

        api_response = await api_client.get_cities(validated_id)
        data = extract_api_data(api_response)
        if isinstance(data, list):
            return list_response(data, "cities")
        return success_response(data)

    except Exception as e:
        return _handle_error(e)


async def get_districts(city_id: str) -> dict[str, Any]:
    """
    Get all districts within a city.

    This is Step 3 in the hierarchical location selection.
    Requires city_id from get_cities().
    Use the district_id either:
    - To call get_subdistricts() for more precision, OR
    - To call calculate_district_cost() directly

    Args:
        city_id: City ID from get_cities().

    Returns:
        List of districts within the city.

    Example:
        >>> districts = await get_districts("152")  # Jakarta Pusat
        >>> # Option A: Get subdistricts for more precision
        >>> subdistricts = await get_subdistricts("2096")
        >>> # Option B: Calculate cost directly with district_id
        >>> cost = await calculate_district_cost("1391", "1376", 1000, "jne")
    """
    try:
        # Validate input
        validated_id = validate_id(city_id, "City ID")

        api_response = await api_client.get_districts(validated_id)
        data = extract_api_data(api_response)
        if isinstance(data, list):
            return list_response(data, "districts")
        return success_response(data)

    except Exception as e:
        return _handle_error(e)


async def get_subdistricts(district_id: str) -> dict[str, Any]:
    """
    Get all subdistricts (kelurahan) within a district.

    This is Step 4 (optional) in the hierarchical location selection.
    Requires district_id from get_districts().
    Use this for maximum precision in shipping calculations.

    Args:
        district_id: District ID from get_districts().

    Returns:
        List of subdistricts within the district.

    Example:
        >>> subdistricts = await get_subdistricts("2096")
    """
    try:
        # Validate input
        validated_id = validate_id(district_id, "District ID")

        api_response = await api_client.get_subdistricts(validated_id)
        data = extract_api_data(api_response)
        if isinstance(data, list):
            return list_response(data, "subdistricts")
        return success_response(data)

    except Exception as e:
        return _handle_error(e)


# ============================================================================
# COST CALCULATION TOOLS
# ============================================================================

async def calculate_domestic_cost(
    origin: str,
    destination: str,
    weight: int,
    courier: str,
) -> dict[str, Any]:
    """
    Calculate domestic shipping cost (Search Method).

    Use this with IDs from search_domestic_destination().

    Args:
        origin: Origin location ID (from search_domestic_destination).
        destination: Destination location ID (from search_domestic_destination).
        weight: Package weight in grams (1-500000).
        courier: Courier code: jne, sicepat, jnt, pos, tiki, anteraja, etc.

    Returns:
        Shipping cost options from the specified courier.

    Example:
        >>> # First, search for locations
        >>> origin = await search_domestic_destination("Jakarta")
        >>> dest = await search_domestic_destination("Surabaya")
        >>> # Then calculate cost
        >>> cost = await calculate_domestic_cost("12345", "67890", 1000, "jne")
    """
    try:
        # Validate all inputs
        validated_origin = validate_id(origin, "Origin ID")
        validated_dest = validate_id(destination, "Destination ID")
        validated_weight = validate_weight(weight)
        validated_courier = validate_courier(courier, "domestic")

        api_response = await api_client.calculate_domestic_cost(
            origin=validated_origin,
            destination=validated_dest,
            weight=validated_weight,
            courier=validated_courier,
            price="lowest",
        )

        data = extract_api_data(api_response)
        return success_response(data, message="Shipping cost calculated successfully")

    except Exception as e:
        return _handle_error(e)


async def calculate_district_cost(
    origin: str,
    destination: str,
    weight: int,
    courier: str,
) -> dict[str, Any]:
    """
    Calculate domestic shipping cost using District IDs (Step-by-Step Method).

    Use this with district_id from get_districts().
    Supports multiple couriers separated by colon (:).

    Args:
        origin: Origin district ID (from get_districts).
        destination: Destination district ID (from get_districts).
        weight: Package weight in grams (1-500000).
        courier: Courier code(s). Single: 'jne'. Multiple: 'jne:sicepat:jnt'.

    Returns:
        Shipping cost options from all specified couriers.

    Example:
        >>> # Step-by-step flow:
        >>> provinces = await get_provinces()
        >>> cities = await get_cities("6")  # DKI Jakarta
        >>> districts = await get_districts("152")  # Jakarta Pusat
        >>> # Calculate with multiple couriers
        >>> cost = await calculate_district_cost(
        ...     origin="1391",
        ...     destination="1376",
        ...     weight=1000,
        ...     courier="jne:sicepat:jnt"
        ... )
    """
    try:
        # Validate all inputs
        validated_origin = validate_id(origin, "Origin District ID")
        validated_dest = validate_id(destination, "Destination District ID")
        validated_weight = validate_weight(weight)
        validated_courier = validate_courier(courier, "domestic")

        api_response = await api_client.calculate_district_domestic_cost(
            origin=validated_origin,
            destination=validated_dest,
            weight=validated_weight,
            courier=validated_courier,
            price="lowest",
        )

        data = extract_api_data(api_response)
        return success_response(data, message="District shipping cost calculated successfully")

    except Exception as e:
        return _handle_error(e)


async def calculate_international_cost(
    origin: str,
    destination: str,
    weight: int,
    courier: str,
) -> dict[str, Any]:
    """
    Calculate international shipping cost.

    Args:
        origin: Origin location ID (Indonesia, from search_domestic_destination).
        destination: Destination country ID (from search_international_destination).
        weight: Package weight in grams (1-500000).
        courier: Courier code: pos, jne, tiki, pcp, ems.

    Returns:
        International shipping cost options.

    Example:
        >>> # Search for origin (Indonesia) and destination (country)
        >>> origin = await search_domestic_destination("Jakarta")
        >>> dest = await search_international_destination("Singapore")
        >>> # Calculate cost
        >>> cost = await calculate_international_cost("12345", "108", 1000, "pos")
    """
    try:
        # Validate all inputs
        validated_origin = validate_id(origin, "Origin ID")
        validated_dest = validate_id(destination, "Destination Country ID")
        validated_weight = validate_weight(weight)
        validated_courier = validate_courier(courier, "international")

        api_response = await api_client.calculate_international_cost(
            origin=validated_origin,
            destination=validated_dest,
            weight=validated_weight,
            courier=validated_courier,
            price="lowest",
        )

        data = extract_api_data(api_response)
        return success_response(data, message="International shipping cost calculated successfully")

    except Exception as e:
        return _handle_error(e)


# ============================================================================
# TRACKING TOOL
# ============================================================================

async def track_package(awb: str, courier: str) -> dict[str, Any]:
    """
    Track a package by AWB (Air Waybill) / tracking number.

    Args:
        awb: Tracking/waybill number (5-50 characters).
        courier: Courier code: jne, sicepat, jnt, pos, tiki, anteraja, etc.

    Returns:
        Tracking status and shipment history.

    Example:
        >>> result = await track_package("JNE1234567890", "jne")
    """
    try:
        # Validate inputs
        validated_awb = validate_awb(awb)
        validated_courier = validate_courier(courier, "domestic")

        api_response = await api_client.track_waybill(
            awb=validated_awb,
            courier=validated_courier,
        )

        data = extract_api_data(api_response, keys=["result", "data", "results"])
        return success_response(data, message="Package tracking retrieved successfully")

    except Exception as e:
        return _handle_error(e)
