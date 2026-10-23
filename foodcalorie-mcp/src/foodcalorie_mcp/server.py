#!/usr/bin/env python3
"""FoodCalorie MCP Server - Query Chinese food nutrition data by barcode or name."""

import logging
import sys
from typing import Any

import httpx
import orjson
from mcp.server.mcpserver import MCPServer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = MCPServer("foodcalorie-mcp")

# Sample food database (in production, this would be a real database/API)
FOOD_DATABASE = {
    "6901234567890": {
        "name": "可口可乐（330ml）",
        "brand": "Coca-Cola",
        "category": "饮料",
        "calories": 140,
        "protein": 0,
        "fat": 0,
        "carbs": 35,
        "sodium": 15,
        "sugar": 35,
        "tip": "含糖饮料，建议适量饮用",
    },
    "6921234567891": {
        "name": "纯牛奶（250ml）",
        "brand": "伊利",
        "category": "乳制品",
        "calories": 150,
        "protein": 8,
        "fat": 4,
        "carbs": 12,
        "sodium": 100,
        "calcium": 300,
        "tip": "优质蛋白质和钙来源",
    },
    "6931234567892": {
        "name": "全麦面包（100g）",
        "brand": "克莉丝汀",
        "category": "面包",
        "calories": 260,
        "protein": 10,
        "fat": 3,
        "carbs": 48,
        "fiber": 6,
        "tip": "富含膳食纤维，适合减肥人群",
    },
    "6941234567893": {
        "name": "红富士苹果（1个）",
        "brand": "国产",
        "category": "水果",
        "calories": 52,
        "protein": 0.3,
        "fat": 0.2,
        "carbs": 14,
        "fiber": 2.4,
        "vitamin_c": 4,
        "tip": "富含抗氧化物质，建议带皮食用",
    },
    "6951234567894": {
        "name": "鸡胸肉（100g）",
        "brand": "国产",
        "category": "肉类",
        "calories": 165,
        "protein": 31,
        "fat": 3.6,
        "carbs": 0,
        "tip": "高蛋白低脂肪，健身首选",
    },
}

# Brand names for search
BRAND_NAMES = {
    "coca": "可口可乐",
    "pepsi": "百事",
    "yili": "伊利",
    "mengniu": "蒙牛",
    "whatsapp": " Whatsapp ",
}


@mcp.tool()
async def search_food_by_barcode(barcode: str) -> dict[str, Any]:
    """Search food nutrition data by barcode.

    Args:
        barcode: The barcode number of the food product (e.g., "6901234567890")

    Returns:
        Nutrition information including calories, protein, fat, carbs, etc.
    """
    item = FOOD_DATABASE.get(barcode)
    if not item:
        return {
            "success": False,
            "error": f"Barcode {barcode} not found in database",
            "suggestion": "Try searching by name instead",
        }
    return {"success": True, "data": item}


@mcp.tool()
async def search_food_by_name(keyword: str, limit: int = 10) -> dict[str, Any]:
    """Search food by name keyword.

    Args:
        keyword: Search keyword (Chinese or English)
        limit: Maximum number of results (default: 10)

    Returns:
        List of matching foods with basic nutrition info
    """
    results = []
    keyword_lower = keyword.lower()

    for barcode, item in FOOD_DATABASE.items():
        if (
            keyword_lower in item["name"].lower()
            or keyword_lower in item.get("brand", "").lower()
            or keyword_lower in item.get("category", "").lower()
        ):
            results.append(
                {
                    "barcode": barcode,
                    "name": item["name"],
                    "brand": item.get("brand"),
                    "category": item.get("category"),
                    "calories": item["calories"],
                    "protein": item.get("protein"),
                    "fat": item.get("fat"),
                    "carbs": item.get("carbs"),
                }
            )
        if len(results) >= limit:
            break

    return {
        "success": True,
        "keyword": keyword,
        "count": len(results),
        "results": results,
    }


@mcp.tool()
async def get_daily_nutrition_summary(
    items: list[dict[str, str]],
) -> dict[str, Any]:
    """Get daily nutrition summary for a list of food items.

    Args:
        items: List of items, each with 'barcode' or 'name' key

    Returns:
        Total nutrition summary with daily value percentages
    """
    total_calories = 0
    total_protein = 0
    total_fat = 0
    total_carbs = 0
    details = []

    for item in items:
        barcode = item.get("barcode")
        name = item.get("name")

        food = None
        if barcode and barcode in FOOD_DATABASE:
            food = FOOD_DATABASE[barcode]
        elif name:
            # Search by name
            for fb_barcode, fb_item in FOOD_DATABASE.items():
                if name.lower() in fb_item["name"].lower():
                    food = fb_item
                    break

        if food:
            total_calories += food.get("calories", 0)
            total_protein += food.get("protein", 0)
            total_fat += food.get("fat", 0)
            total_carbs += food.get("carbs", 0)
            details.append(
                {
                    "name": food["name"],
                    "calories": food.get("calories", 0),
                    "protein": food.get("protein", 0),
                    "fat": food.get("fat", 0),
                    "carbs": food.get("carbs", 0),
                }
            )

    # Calculate daily value percentages (based on 2000 calorie diet)
    dv_calories = (total_calories / 2000) * 100
    dv_protein = (total_protein / 50) * 100
    dv_fat = (total_fat / 65) * 100
    dv_carbs = (total_carbs / 300) * 100

    return {
        "success": True,
        "summary": {
            "total_calories": total_calories,
            "total_protein": round(total_protein, 1),
            "total_fat": round(total_fat, 1),
            "total_carbs": round(total_carbs, 1),
            "daily_values": {
                "calories": f"{dv_calories:.1f}%",
                "protein": f"{dv_protein:.1f}%",
                "fat": f"{dv_fat:.1f}%",
                "carbs": f"{dv_carbs:.1f}%",
            },
        },
        "details": details,
    }


@mcp.tool()
async def get_health_tip(food_name: str) -> dict[str, Any]:
    """Get health tips for a specific food.

    Args:
        food_name: Name of the food

    Returns:
        Health tips and dietary recommendations
    """
    food_name_lower = food_name.lower()

    tips = []
    for barcode, item in FOOD_DATABASE.items():
        if food_name_lower in item["name"].lower():
            tips.append(
                {
                    "food": item["name"],
                    "tip": item.get("tip", "无特别建议"),
                    "category": item.get("category", "其他"),
                    "calories_per_serving": item["calories"],
                }
            )

    # General tips based on keywords
    general_tips = {
        "高糖": "建议控制糖分摄入，选择低糖或无糖替代品",
        "高脂": "注意脂肪摄入量，选择低脂食品",
        "高蛋白": "优质蛋白质来源，适合运动后补充",
        "高纤维": "有助于消化，建议增加摄入量",
    }

    for keyword, tip in general_tips.items():
        if keyword in food_name:
            tips.append({"food": "通用建议", "tip": tip})

    return {
        "success": True,
        "query": food_name,
        "tips": tips if tips else [{"food": food_name, "tip": "暂无数据，建议咨询营养师"}],
    }


def main() -> None:
    """Main server entry point."""
    logger.info("Starting FoodCalorie MCP Server...")
    mcp.run(stdio=True)


if __name__ == "__main__":
    main()
