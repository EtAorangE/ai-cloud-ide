# AI Cloud IDE

一个为 AI 访问优化的云端开发环境，基于 Gitpod。

## 快速使用

**在浏览器地址栏输入：**
```
gitpod.io/#https://github.com/你的用户名/ai-cloud-ide
```

或者直接点击下方按钮（需要先 Fork 到你的账号）：

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/你的用户名/ai-cloud-ide)

## 功能特点

- ✅ **完全免费** - 每月 50 小时免费使用
- ✅ **VS Code 体验** - 完整的 VS Code 编辑器
- ✅ **内置终端** - 完整的 Shell 环境
- ✅ **预装工具** - Python, Node.js, pnpm, bun
- ✅ **AI 友好** - 浏览器自动化可访问

## 包含工具

| 工具 | 版本 | 用途 |
|------|------|------|
| Python | 3.11 | 后端开发、数据分析 |
| Node.js | 18+ | 前端开发、全栈应用 |
| pnpm | latest | 包管理器 |
| bun | latest | JavaScript 运行时 |
| Jupyter | latest | 数据科学、Notebook |

## 示例代码

### Python 示例
```python
# main.py
import requests

def hello():
    print("Hello from AI Cloud IDE!")
    
if __name__ == "__main__":
    hello()
```

### 运行方式
```bash
python main.py
```

## AI 访问方式

AI 可以通过浏览器自动化工具访问此 IDE：

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://gitpod.io/#https://github.com/你的用户名/ai-cloud-ide')
    # 登录并操作...
```

## 注意事项

- Gitpod 免费套餐每月 50 小时
- 工作区会在不活跃 30 分钟后自动关闭
- 数据保存在云端，建议定期推送到 GitHub

## License

MIT
