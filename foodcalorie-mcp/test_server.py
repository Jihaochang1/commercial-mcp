#!/usr/bin/env python3
"""Test script for FoodCalorie MCP Server tools."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from foodcalorie_mcp.server import (
    FOOD_DATABASE,
    get_health_tip,
    get_daily_nutrition_summary,
    search_food_by_barcode,
    search_food_by_name,
)


async def test_all_tools():
    """Test all MCP server tools."""
    print("=" * 60)
    print("FoodCalorie MCP Server - Test Suite")
    print("=" * 60)

    # Test 1: Search by barcode
    print("\n📋 Test 1: Search by barcode")
    result = await search_food_by_barcode("6901234567890")
    print(f"  Input: barcode='6901234567890'")
    print(f"  Result: {json.dumps(result, indent=2, ensure_ascii=False)}")

    # Test 2: Search by name
    print("\n📋 Test 2: Search by name")
    result = await search_food_by_name("可乐")
    print(f"  Input: keyword='可乐'")
    print(f"  Results found: {result['count']}")
    for item in result["results"]:
        print(f"    - {item['name']}: {item['calories']} kcal")

    # Test 3: Daily nutrition summary
    print("\n📋 Test 3: Daily nutrition summary")
    items = [
        {"barcode": "6901234567890"},  # Coca-Cola
        {"barcode": "6921234567891"},  # Milk
        {"name": "鸡胸肉"},  # Chicken breast
    ]
    result = await get_daily_nutrition_summary(items)
    print(f"  Items: {len(items)}")
    print(f"  Total calories: {result['summary']['total_calories']} kcal")
    print(f"  Daily values: {result['summary']['daily_values']}")

    # Test 4: Health tips
    print("\n📋 Test 4: Health tips")
    result = await get_health_tip("高糖饮料")
    print(f"  Query: '高糖饮料'")
    for tip in result["tips"]:
        print(f"    - {tip['food']}: {tip['tip']}")

    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_all_tools())
