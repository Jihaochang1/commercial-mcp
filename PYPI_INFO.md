# PyPI 账号信息

## 邮箱
358550956@qq.com

## 用户名
jihaochang1

## 密码
(需要创建账号时设置)

## 操作步骤
1. 访问 https://pypi.org/account/register/
2. 使用邮箱 358550956@qq.com 注册
3. 验证邮箱
4. 使用以下命令上传包：
   ```
   python -m twine upload dist/*
   ```
5. 输入用户名: jihaochang1
6. 输入密码或 API Token

## 注意事项
- 建议使用 API Token 而不是密码
- Token 可在 https://pypi.org/manage/account/token/ 创建
- 权限选择: Upload releases to foodcalorie-mcp
