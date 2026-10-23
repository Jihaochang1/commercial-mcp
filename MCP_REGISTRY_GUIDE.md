# MCP Registry 注册指南

## 官方 Registry
- URL: https://github.com/modelcontextprotocol/registry
- 提交方式: Pull Request

## 提交步骤

### 1. Fork 官方 Registry
访问: https://github.com/modelcontextprotocol/registry
点击 Fork 按钮

### 2. 添加你的 Server
在 `servers/` 目录下创建新文件:
```json
{
  "name": "foodcalorie-mcp",
  "description": "MCP Server for Chinese food calorie and nutrition data",
  "repository": "https://github.com/Jihaochang1/foodcalorie-mcp",
  "image": "https://raw.githubusercontent.com/Jihaochang1/foodcalorie-mcp/main/logo.png",
  "schemaVersion": 1
}
```

### 3. 提交 PR
- Commit message: "Add foodcalorie-mcp server"
- 等待审核

## 其他目录

### mcp.so
- URL: https://mcp.so
- 提交方式: 网站提交表单

### PulseMCP
- URL: https://pulsemcp.com
- GitHub: https://github.com/pulsemcp/mcp-servers

## 注意事项
- Registry 审核需要时间（通常1-3天）
- 确保 README 清晰完整
- 提供测试示例
