"""
MCP Server Module
=================
FastMCP server initialization and tool registration.
"""

from mcp.server.fastmcp import FastMCP

from .config import settings
from .tools import (
    # Search Method
    calculate_domestic_cost,
    calculate_international_cost,
    search_domestic_destination,
    search_international_destination,
    # Step-by-Step Method
    get_provinces,
    get_cities,
    get_districts,
    get_subdistricts,
    calculate_district_cost,
    # Tracking
    track_package,
)

# Initialize FastMCP server
mcp = FastMCP(settings.SERVER_NAME)

# ============================================================================
# Register Search Method Tools
# ============================================================================
mcp.tool()(search_domestic_destination)
mcp.tool()(search_international_destination)
mcp.tool()(calculate_domestic_cost)
mcp.tool()(calculate_international_cost)

# ============================================================================
# Register Step-by-Step Method Tools (Hierarchical Location)
# ============================================================================
mcp.tool()(get_provinces)
mcp.tool()(get_cities)
mcp.tool()(get_districts)
mcp.tool()(get_subdistricts)
mcp.tool()(calculate_district_cost)

# ============================================================================
# Register Tracking Tool
# ============================================================================
mcp.tool()(track_package)


def run_server() -> None:
    """Run the MCP server."""
    mcp.run()
