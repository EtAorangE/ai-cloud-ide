# AI 调用云端 IDE 完整指南

## 🎯 两种调用方式

### 方式一：HTTP API（推荐）✨

最简单的方式！启动后 AI 可以直接通过 HTTP 请求操作 IDE。

#### 步骤：

**1. 启动 Gitpod 工作区**
```
https://gitpod.io/#https://github.com/EtAorangE/ai-cloud-ide
```

**2. 在 Gitpod 终端运行 API 服务**
```bash
python api_server.py
```

**3. 获取 API 地址**
- 查看 Gitpod 底部的「Ports」标签
- 复制 8080 端口的公开 URL（格式：`https://8080-xxx.gitpod.io`）

**4. AI 调用示例**

```python
import requests

# 替换为你的 Gitpod 端口 URL
API_URL = "https://8080-xxx.gitpod.io"

# 执行命令
response = requests.post(f"{API_URL}/api/execute", json={
    "command": "python -c 'print(\"Hello AI!\")'"
})
print(response.json())

# 创建文件
response = requests.post(f"{API_URL}/api/file", json={
    "filename": "test.py",
    "content": "print('Created by AI!')"
})
print(response.json())

# 运行 Python
response = requests.post(f"{API_URL}/api/execute", json={
    "command": "python test.py"
})
print(response.json())
```

---

### 方式二：浏览器自动化

使用 Playwright 控制 Gitpod。

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 打开 Gitpod
    page.goto('https://gitpod.io/#https://github.com/EtAorangE/ai-cloud-ide')
    
    # 等待启动（需要登录 GitHub）
    page.wait_for_timeout(60000)
    
    # 打开终端
    page.keyboard.press('Control+`')
    
    # 输入命令
    page.keyboard.type('python main.py')
    page.keyboard.press('Enter')
```

---

## 📡 API 接口文档

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | API 文档 |
| `/api/status` | GET | 获取 IDE 状态 |
| `/api/files` | GET | 列出文件 |
| `/api/file/{name}` | GET | 读取文件 |
| `/api/file` | POST | 写入文件 |
| `/api/delete` | POST | 删除文件 |
| `/api/mkdir` | POST | 创建目录 |
| `/api/execute` | POST | 执行命令 |

### 示例请求

**执行命令**
```json
POST /api/execute
{
    "command": "ls -la",
    "timeout": 30
}
```

**创建文件**
```json
POST /api/file
{
    "filename": "hello.py",
    "content": "print('Hello World!')"
}
```

---

## 🚀 快速测试

1. 打开 Gitpod
2. 运行 `python api_server.py`
3. 在另一个终端运行 `python ai_client.py`（修改 BASE_URL）

---

## ⚠️ 注意事项

- Gitpod 免费套餐每月 50 小时
- API 服务需要手动启动
- 端口 URL 每次启动会变化
- 建议保存重要代码到 GitHub
