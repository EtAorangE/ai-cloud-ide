# AI Cloud IDE 🚀

一个为 AI 访问优化的云端开发环境，基于 Gitpod。

## 🎯 一键启动

**点击下方按钮即可启动免费的云端 IDE：**

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/EtAorangE/ai-cloud-ide)

**或者直接在浏览器地址栏输入：**
```
https://gitpod.io/#https://github.com/EtAorangE/ai-cloud-ide
```

## ✨ 功能特点

| 功能 | 说明 |
|------|------|
| 🆓 **完全免费** | 每月 50 小时免费使用 |
| 💻 **VS Code 体验** | 完整的 VS Code 编辑器 |
| ⌨️ **内置终端** | 完整的 Shell 环境 |
| 🐍 **Python 3.11** | 后端开发、数据分析 |
| 📦 **Node.js 18+** | 前端开发、全栈应用 |
| 🔧 **预装工具** | pnpm, bun, Jupyter 等 |

## 📦 包含工具

- **Python 3.11** - 后端开发、数据分析
- **Node.js 18+** - 前端开发
- **pnpm** - 快速的包管理器
- **bun** - JavaScript 运行时
- **Jupyter** - 数据科学 Notebook
- **Git** - 版本控制

## 🚀 快速开始

启动后，您可以直接在终端运行：

```bash
# Python 示例
python main.py

# 启动 Web 服务器
python server.py

# Node.js 示例
node index.js
```

## 🤖 AI 访问方式

AI 可以通过浏览器自动化工具访问此 IDE：

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://gitpod.io/#https://github.com/EtAorangE/ai-cloud-ide')
    # 登录并操作...
```

## 📝 项目结构

```
ai-cloud-ide/
├── .gitpod.yml    # Gitpod 配置
├── main.py        # Python 示例
├── server.py      # Web 服务器示例
├── index.js       # Node.js 示例
└── README.md      # 说明文档
```

## ⚠️ 注意事项

- Gitpod 免费套餐每月 50 小时
- 工作区会在不活跃 30 分钟后自动关闭
- 数据保存在云端，建议定期推送到 GitHub

## 📄 License

MIT
