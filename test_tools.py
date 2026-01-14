"""
Test Script for RajaOngkir MCP Server
=====================================
Run this script to test all tools with proper validation.

Usage:
    python test_tools.py
"""

import asyncio
import json

from src.tools import (
    calculate_district_cost,
    calculate_domestic_cost,
    get_cities,
    get_districts,
    get_provinces,
    get_subdistricts,
    search_domestic_destination,
    search_international_destination,
    track_package,
)


def print_result(name: str, result: dict) -> None:
    """Pretty print a test result."""
    print(f"\n{'=' * 60}")
    print(f"📌 {name}")
    print("=" * 60)

    if result.get("success"):
        print("✅ Status: SUCCESS")
        if "message" in result:
            print(f"📝 Message: {result['message']}")
        if "meta" in result:
            print(f"📊 Meta: {result['meta']}")
        # Print first 2 items of data for brevity
        data = result.get("data", [])
        if isinstance(data, list) and len(data) > 0:
            print(f"📦 Data (showing first 2 of {len(data)}):")
            for item in data[:2]:
                print(f"   {json.dumps(item, indent=2)[:200]}...")
        else:
            print(f"📦 Data: {json.dumps(data, indent=2)[:300]}...")
    else:
        print("❌ Status: ERROR")
        error = result.get("error", {})
        print(f"🔴 Code: {error.get('code', 'N/A')}")
        print(f"🔴 Message: {error.get('message', 'N/A')}")
        if error.get("detail"):
            print(f"🔴 Detail: {error['detail']}")


async def test_search_method():
    """Test Search Method tools."""
    print("\n" + "🔍 " * 20)
    print("TESTING SEARCH METHOD")
    print("🔍 " * 20)

    # Test domestic search
    result = await search_domestic_destination("Jakarta")
    print_result("search_domestic_destination('Jakarta')", result)

    # Test international search
    result = await search_international_destination("Singapore")
    print_result("search_international_destination('Singapore')", result)


async def test_step_by_step_method():
    """Test Step-by-Step Method tools."""
    print("\n" + "🗂️ " * 20)
    print("TESTING STEP-BY-STEP METHOD")
    print("🗂️ " * 20)

    # Step 1: Get provinces
    result = await get_provinces()
    print_result("Step 1: get_provinces()", result)

    province_id = None
    if result.get("success") and result.get("data"):
        # Find DKI Jakarta or use first province
        for prov in result["data"]:
            if "jakarta" in prov.get("province", "").lower():
                province_id = str(prov.get("province_id", prov.get("id", "")))
                break
        if not province_id and result["data"]:
            province_id = str(result["data"][0].get("province_id", result["data"][0].get("id", "")))

    if province_id:
        # Step 2: Get cities
        result = await get_cities(province_id)
        print_result(f"Step 2: get_cities('{province_id}')", result)

        city_id = None
        if result.get("success") and result.get("data"):
            city_id = str(result["data"][0].get("city_id", result["data"][0].get("id", "")))

        if city_id:
            # Step 3: Get districts
            result = await get_districts(city_id)
            print_result(f"Step 3: get_districts('{city_id}')", result)

            district_id = None
            if result.get("success") and result.get("data"):
                district_id = str(result["data"][0].get("district_id", result["data"][0].get("id", "")))

            if district_id:
                # Step 4: Get subdistricts (optional)
                result = await get_subdistricts(district_id)
                print_result(f"Step 4: get_subdistricts('{district_id}')", result)


async def test_cost_calculation():
    """Test cost calculation tools."""
    print("\n" + "💰 " * 20)
    print("TESTING COST CALCULATION")
    print("💰 " * 20)

    # Test with sample district IDs
    result = await calculate_district_cost(
        origin="1391",
        destination="1376",
        weight=1000,
        courier="jne",
    )
    print_result("calculate_district_cost('1391', '1376', 1000, 'jne')", result)


async def test_validation_errors():
    """Test that validation works correctly."""
    print("\n" + "🛡️ " * 20)
    print("TESTING VALIDATION (Expected Errors)")
    print("🛡️ " * 20)

    # Test empty query
    result = await search_domestic_destination("")
    print_result("search_domestic_destination('') - Empty query", result)

    # Test invalid weight
    result = await calculate_district_cost("1391", "1376", -100, "jne")
    print_result("calculate_district_cost with negative weight", result)

    # Test invalid courier
    result = await calculate_district_cost("1391", "1376", 1000, "invalid_courier")
    print_result("calculate_district_cost with invalid courier", result)


async def main():
    """Run all tests."""
    print("🚀 " * 20)
    print("RAJAONGKIR MCP SERVER - TOOL TESTS")
    print("🚀 " * 20)

    await test_search_method()
    await test_step_by_step_method()
    await test_cost_calculation()
    await test_validation_errors()

    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
