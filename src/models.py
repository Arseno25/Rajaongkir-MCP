"""
Data Models Module
==================
Pydantic models for request/response data structures.
Based on the official Postman Collection specifications.
"""

from pydantic import BaseModel, Field


# ============================================================================
# Request Models
# ============================================================================

class DomesticCostRequest(BaseModel):
    """Request payload for domestic shipping cost calculation."""

    origin: str = Field(..., description="Origin location ID")
    destination: str = Field(..., description="Destination location ID")
    weight: int = Field(..., gt=0, description="Weight in grams")
    courier: str = Field(..., description="Courier code (e.g., 'jne', 'sicepat')")
    price: str = Field(default="lowest", description="Price preference")


class InternationalCostRequest(BaseModel):
    """Request payload for international shipping cost calculation."""

    origin: str = Field(..., description="Origin location ID (Indonesia)")
    destination: str = Field(..., description="Destination country ID")
    weight: int = Field(..., gt=0, description="Weight in grams")
    courier: str = Field(..., description="Courier code")
    price: str = Field(default="lowest", description="Price preference")


class TrackingRequest(BaseModel):
    """Request payload for package tracking."""

    awb: str = Field(..., description="Tracking/waybill number")
    courier: str = Field(..., description="Courier code")


# ============================================================================
# Error Models
# ============================================================================

class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str
    detail: str | None = None
