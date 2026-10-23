# FoodCalorie MCP Server

> 中国食品营养数据MCP服务器 - 扫码查热量，健康饮食更轻松

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![MCP SDK](https://img.shields.io/badge/MCP-v2.x-green.svg)](https://github.com/modelcontextprotocol/python-sdk)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

## 🚀 快速开始

### 安装

```bash
pip install -e .
```

### 运行

```bash
foodcalorie-mcp
```

### 配置 Claude/Cursor

在 `.claude/settings.json` 或 `cursorrules` 中添加：

```json
{
  "mcpServers": {
    "foodcalorie": {
      "command": "python",
      "args": ["-m", "foodcalorie_mcp.server"]
    }
  }
}
```

## 📖 可用工具

| 工具 | 描述 | 参数 |
|------|------|------|
| `search_food_by_barcode` | 通过条形码查询食品营养数据 | `barcode: string` |
| `search_food_by_name` | 通过名称关键词搜索食品 | `keyword: string`, `limit: int` |
| `get_daily_nutrition_summary` | 计算每日营养摄入汇总 | `items: list[dict]` |
| `get_health_tip` | 获取健康饮食建议 | `food_name: string` |

## 💡 使用示例

### 查询特定食品
```
用户: 查询条形码6901234567890的营养信息
AI: 调用 search_food_by_barcode(barcode="6901234567890")
```

### 计算每日摄入
```
用户: 我今天吃了可乐、牛奶和鸡胸肉，帮我计算总热量
AI: 调用 get_daily_nutrition_summary(items=[...])
```

## 🎯 商业化路线

### Free Tier
- 基础食品数据库（500+ 商品）
- 条形码查询
- 名称搜索

### Pro Tier (¥29/月)
- 实时价格数据（美团/京东）
- 饮食计划生成
- 健康报告导出

### Enterprise (定制报价)
- API 访问
- 私有数据集
- 定制化服务

## 🏗️ 架构

```
FoodCalorie MCP Server
├── 核心工具层 (server.py)
├── 数据层 (SQLite/PostgreSQL)
├── 外部API (条形码查询、价格追踪)
└── 认证层 (License Key验证)
```

## 📦 发布到MCP Marketplace

1. 注册 [MCP Marketplace](https://mcpmarketplace.io)
2. 上传包（支持Python SDK）
3. 配置定价和许可密钥
4. 发布并同步到 mcp.so、PulseMCP

## 🔧 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 代码格式化
ruff format src/
```

## 📄 许可证

Apache-2.0

## 🤝 贡献

欢迎 PR！请先 Fork 并创建特性分支。

## 📞 联系与支持

### 技术支持
- **付费咨询服务**: ¥500-2000/小时（企业客户专享）
- **定制开发**: ¥10,000-50,000/项目
- **企业培训**: ¥1,000-2,000/人/天
- 联系邮箱: jihaochang1@github.com

### 赞助项目
如果这个项目对你有帮助，欢迎赞助支持：
- [GitHub Sponsors](https://github.com/sponsors/Jihaochang1) 💝
- 或一次性捐赠: [Buy Me a Coffee](https://buymeacoffee.com/jihaochang) ☕

### 商业合作
- 企业定制部署: ¥20,000起
- 私有化部署: ¥50,000起
- 数据定制服务: 面议

---

*让AI帮你吃得健康！* 🥗

**⭐ 如果觉得有用，请给个 Star！你的支持是我持续维护的动力**
