"""
Configuration Module
====================
Handles all configuration and environment variable loading.
"""

import os
import sys
from dataclasses import dataclass

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    # API Configuration
    BASE_URL: str = "https://rajaongkir.komerce.id/api/v1"
    API_KEY: str | None = None

    # HTTP Client Configuration
    REQUEST_TIMEOUT: float = 30.0

    # Server Configuration
    SERVER_NAME: str = "RajaOngkir Komerce"

    def __post_init__(self) -> None:
        """Validate settings after initialization."""
        if not self.API_KEY:
            print(
                "⚠️  WARNING: RAJAONGKIR_API_KEY is not set in .env file!",
                file=sys.stderr,
            )
            print(
                "   Please create a .env file with your API key.",
                file=sys.stderr,
            )
            print(
                "   See .env.example for reference.",
                file=sys.stderr,
            )

    @property
    def is_configured(self) -> bool:
        """Check if the API key is configured."""
        return bool(self.API_KEY)

    # ========================================================================
    # Search Method Endpoints
    # ========================================================================

    @property
    def domestic_destination_url(self) -> str:
        return f"{self.BASE_URL}/destination/domestic-destination"

    @property
    def international_destination_url(self) -> str:
        return f"{self.BASE_URL}/destination/international-destination"

    # ========================================================================
    # Step-by-Step Method Endpoints (Hierarchical Location)
    # ========================================================================

    @property
    def province_url(self) -> str:
        """Get all provinces."""
        return f"{self.BASE_URL}/destination/province"

    def city_url(self, province_id: str | int) -> str:
        """Get cities by province ID."""
        return f"{self.BASE_URL}/destination/city/{province_id}"

    def district_url(self, city_id: str | int) -> str:
        """Get districts by city ID."""
        return f"{self.BASE_URL}/destination/district/{city_id}"

    def subdistrict_url(self, district_id: str | int) -> str:
        """Get subdistricts by district ID."""
        return f"{self.BASE_URL}/destination/sub-district/{district_id}"

    # ========================================================================
    # Cost Calculation Endpoints
    # ========================================================================

    @property
    def domestic_cost_url(self) -> str:
        return f"{self.BASE_URL}/calculate/domestic-cost"

    @property
    def international_cost_url(self) -> str:
        return f"{self.BASE_URL}/calculate/international-cost"

    @property
    def district_domestic_cost_url(self) -> str:
        """Calculate cost using district IDs (Step-by-Step Method)."""
        return f"{self.BASE_URL}/calculate/district/domestic-cost"

    # ========================================================================
    # Tracking Endpoint
    # ========================================================================

    @property
    def track_waybill_url(self) -> str:
        return f"{self.BASE_URL}/track/waybill"


def get_settings() -> Settings:
    """
    Factory function to create Settings instance.

    Returns:
        Settings: Application settings loaded from environment.
    """
    return Settings(
        BASE_URL=os.getenv("RAJAONGKIR_BASE_URL", "https://rajaongkir.komerce.id/api/v1"),
        API_KEY=os.getenv("RAJAONGKIR_API_KEY"),
    )


# Global settings instance
settings = get_settings()
