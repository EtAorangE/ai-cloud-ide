#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 调用云端 IDE 的简单客户端
演示如何通过 HTTP API 操作云端 IDE

使用前：
1. 先在 Gitpod 中启动 API 服务：python api_server.py
2. 获取 Gitpod 转发的端口 URL
3. 运行此脚本
"""

import requests
import json
from typing import Optional

class CloudIDEClient:
    """云端 IDE 客户端"""
    
    def __init__(self, base_url: str):
        """
        初始化客户端
        
        Args:
            base_url: Gitpod 转发的 API 地址，如 https://8080-xxx.gitpod.io
        """
        self.base_url = base_url.rstrip('/')
    
    def get_status(self) -> dict:
        """获取 IDE 状态"""
        response = requests.get(f'{self.base_url}/api/status')
        return response.json()
    
    def list_files(self) -> dict:
        """列出文件"""
        response = requests.get(f'{self.base_url}/api/files')
        return response.json()
    
    def read_file(self, filename: str) -> dict:
        """读取文件"""
        response = requests.get(f'{self.base_url}/api/file/{filename}')
        return response.json()
    
    def write_file(self, filename: str, content: str) -> dict:
        """写入文件"""
        response = requests.post(
            f'{self.base_url}/api/file',
            json={'filename': filename, 'content': content}
        )
        return response.json()
    
    def delete_file(self, filename: str) -> dict:
        """删除文件"""
        response = requests.post(
            f'{self.base_url}/api/delete',
            json={'filename': filename}
        )
        return response.json()
    
    def create_directory(self, dirname: str) -> dict:
        """创建目录"""
        response = requests.post(
            f'{self.base_url}/api/mkdir',
            json={'dirname': dirname}
        )
        return response.json()
    
    def execute(self, command: str, timeout: int = 30) -> dict:
        """执行命令"""
        response = requests.post(
            f'{self.base_url}/api/execute',
            json={'command': command, 'timeout': timeout}
        )
        return response.json()
    
    def run_python(self, code: str) -> dict:
        """运行 Python 代码"""
        # 先写入文件
        self.write_file('_temp.py', code)
        # 然后执行
        return self.execute('python _temp.py')


# ============================================
# 使用示例
# ============================================

def main():
    print("=" * 60)
    print("🤖 AI 云端 IDE 客户端示例")
    print("=" * 60)
    
    # 替换为你的 Gitpod 端口 URL
    # 格式：https://端口号-工作区ID.gitpod.io
    BASE_URL = "https://8080-your-workspace.gitpod.io"  # ← 修改这里
    
    print(f"\n📡 连接到: {BASE_URL}")
    print("⚠️ 请先在 Gitpod 中运行: python api_server.py")
    print()
    
    # 创建客户端
    client = CloudIDEClient(BASE_URL)
    
    try:
        # 1. 获取状态
        print("1️⃣ 获取 IDE 状态...")
        status = client.get_status()
        print(f"   状态: {status.get('status')}")
        print(f"   Python: {status.get('python_version', '').split()[0]}")
        print()
        
        # 2. 创建文件
        print("2️⃣ 创建 Python 文件...")
        code = '''#!/usr/bin/env python3
# 由 AI 创建的文件
print("Hello from AI Cloud IDE!")
print("This file was created by AI via HTTP API")
'''
        result = client.write_file('ai_created.py', code)
        print(f"   结果: {result}")
        print()
        
        # 3. 执行代码
        print("3️⃣ 执行 Python 代码...")
        result = client.execute('python ai_created.py')
        print(f"   输出: {result.get('stdout', '').strip()}")
        print()
        
        # 4. 列出文件
        print("4️⃣ 列出工作区文件...")
        files = client.list_files()
        for f in files.get('files', []):
            print(f"   - {f['name']} ({f['type']})")
        print()
        
        # 5. 运行复杂命令
        print("5️⃣ 安装包并运行...")
        result = client.execute('pip list | head -5')
        print(f"   已安装的包:\n{result.get('stdout', '')}")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败！请确保：")
        print("   1. Gitpod 工作区已启动")
        print("   2. API 服务正在运行 (python api_server.py)")
        print("   3. BASE_URL 正确")
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()
