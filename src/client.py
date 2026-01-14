"""
HTTP Client Module
==================
Async HTTP client for RajaOngkir Komerce API V2.
Based on the official Postman Collection specifications.
"""

from typing import Any

import httpx

from .config import settings
from .exceptions import APIError, ConfigurationError, NetworkError


class RajaOngkirClient:
    """
    Async HTTP client for RajaOngkir Komerce API V2.

    This client handles all HTTP communication with the RajaOngkir API,
    including authentication, request formatting, and error handling.
    """

    def __init__(self) -> None:
        """Initialize the client with settings."""
        self.api_key = settings.API_KEY
        self.timeout = settings.REQUEST_TIMEOUT

    def _get_headers(self, include_content_type: bool = False) -> dict[str, str]:
        """Generate headers for API requests."""
        headers = {"key": self.api_key or ""}
        if include_content_type:
            headers["content-type"] = "application/x-www-form-urlencoded"
        return headers

    def _ensure_configured(self) -> None:
        """Ensure API key is configured."""
        if not settings.is_configured:
            raise ConfigurationError(
                message="API key not configured",
                detail="Please set RAJAONGKIR_API_KEY in .env file.",
            )

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """
        Handle API response and raise errors if needed.

        Args:
            response: The HTTP response object.

        Returns:
            Parsed JSON response.

        Raises:
            APIError: If response status code is not 2xx.
        """
        # Handle different error codes with specific messages
        if response.status_code == 400:
            raise APIError(
                message="Bad request - invalid parameters",
                status_code=400,
                detail=response.text,
            )
        elif response.status_code == 401:
            raise APIError(
                message="Unauthorized - invalid API key",
                status_code=401,
                detail="Please check your RAJAONGKIR_API_KEY in .env file.",
            )
        elif response.status_code == 403:
            raise APIError(
                message="Forbidden - API key does not have access",
                status_code=403,
                detail=response.text,
            )
        elif response.status_code == 404:
            raise APIError(
                message="Resource not found",
                status_code=404,
                detail=response.text,
            )
        elif response.status_code == 429:
            raise APIError(
                message="Rate limit exceeded",
                status_code=429,
                detail="Too many requests. Please wait and try again.",
            )
        elif response.status_code >= 500:
            raise APIError(
                message="RajaOngkir server error",
                status_code=response.status_code,
                detail="The API server is experiencing issues. Please try again later.",
            )
        elif response.status_code != 200:
            raise APIError(
                message=f"API returned status {response.status_code}",
                status_code=response.status_code,
                detail=response.text,
            )

        try:
            return response.json()
        except Exception:
            raise APIError(
                message="Failed to parse API response",
                status_code=response.status_code,
                detail="The API returned an invalid JSON response.",
            )

    async def _get(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Make a GET request.

        Args:
            url: The URL to request.
            params: Optional query parameters.

        Returns:
            Parsed JSON response.
        """
        self._ensure_configured()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    url,
                    headers=self._get_headers(),
                    params=params,
                )
                return self._handle_response(response)

            except httpx.TimeoutException:
                raise NetworkError(
                    message="Request timeout",
                    detail="The request took too long. Please try again.",
                )
            except httpx.RequestError as e:
                raise NetworkError(
                    message="Network request failed",
                    detail=str(e),
                )

    async def _post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Make a POST request.

        Args:
            url: The URL to request.
            data: Form data to send in body.
            params: Optional query parameters.

        Returns:
            Parsed JSON response.
        """
        self._ensure_configured()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    url,
                    headers=self._get_headers(include_content_type=True if data else False),
                    data=data,
                    params=params,
                )
                return self._handle_response(response)

            except httpx.TimeoutException:
                raise NetworkError(
                    message="Request timeout",
                    detail="The request took too long. Please try again.",
                )
            except httpx.RequestError as e:
                raise NetworkError(
                    message="Network request failed",
                    detail=str(e),
                )

    # ========================================================================
    # Search Method Endpoints
    # ========================================================================

    async def search_domestic_destination(
        self,
        query: str,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Search domestic destinations (cities/districts)."""
        return await self._get(
            settings.domestic_destination_url,
            params={"search": query, "limit": limit, "offset": offset},
        )

    async def search_international_destination(
        self,
        query: str,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Search international destinations (countries)."""
        return await self._get(
            settings.international_destination_url,
            params={"search": query, "limit": limit, "offset": offset},
        )

    # ========================================================================
    # Step-by-Step Method Endpoints
    # ========================================================================

    async def get_provinces(self) -> dict[str, Any]:
        """Get all Indonesian provinces."""
        return await self._get(settings.province_url)

    async def get_cities(self, province_id: str) -> dict[str, Any]:
        """Get all cities within a province."""
        return await self._get(settings.city_url(province_id))

    async def get_districts(self, city_id: str) -> dict[str, Any]:
        """Get all districts within a city."""
        return await self._get(settings.district_url(city_id))

    async def get_subdistricts(self, district_id: str) -> dict[str, Any]:
        """Get all subdistricts within a district."""
        return await self._get(settings.subdistrict_url(district_id))

    # ========================================================================
    # Cost Calculation Endpoints
    # ========================================================================

    async def calculate_domestic_cost(
        self,
        origin: str,
        destination: str,
        weight: int,
        courier: str,
        price: str = "lowest",
    ) -> dict[str, Any]:
        """Calculate domestic shipping cost (Search Method)."""
        return await self._post(
            settings.domestic_cost_url,
            data={
                "origin": origin,
                "destination": destination,
                "weight": weight,
                "courier": courier,
                "price": price,
            },
        )

    async def calculate_district_domestic_cost(
        self,
        origin: str,
        destination: str,
        weight: int,
        courier: str,
        price: str = "lowest",
    ) -> dict[str, Any]:
        """Calculate domestic shipping cost using District IDs (Step-by-Step)."""
        return await self._post(
            settings.district_domestic_cost_url,
            data={
                "origin": origin,
                "destination": destination,
                "weight": weight,
                "courier": courier,
                "price": price,
            },
        )

    async def calculate_international_cost(
        self,
        origin: str,
        destination: str,
        weight: int,
        courier: str,
        price: str = "lowest",
    ) -> dict[str, Any]:
        """Calculate international shipping cost."""
        return await self._post(
            settings.international_cost_url,
            data={
                "origin": origin,
                "destination": destination,
                "weight": weight,
                "courier": courier,
                "price": price,
            },
        )

    # ========================================================================
    # Tracking Endpoint
    # ========================================================================

    async def track_waybill(self, awb: str, courier: str) -> dict[str, Any]:
        """
        Track a package by AWB number.
        NOTE: Uses query params even though it's a POST request (per Postman spec).
        """
        return await self._post(
            settings.track_waybill_url,
            params={"awb": awb, "courier": courier},
        )


# Global client instance
api_client = RajaOngkirClient()
