#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Cloud IDE - 示例程序
"""

import os
import sys
from datetime import datetime

def main():
    print("=" * 50)
    print("🚀 AI Cloud IDE - 欢迎使用!")
    print("=" * 50)
    print(f"\n📅 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python 版本: {sys.version}")
    print(f"📁 当前目录: {os.getcwd()}")
    print("\n✅ 环境配置完成，可以开始编码了！")
    print("\n可用命令:")
    print("  - python main.py     # 运行此程序")
    print("  - pip install <包名>  # 安装 Python 包")
    print("  - npm install <包名>  # 安装 Node.js 包")
    print("  - pnpm add <包名>     # 使用 pnpm 安装")
    print("\n祝您编码愉快! 🎉")

if __name__ == "__main__":
    main()
