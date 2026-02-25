#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 调用云端 IDE 的完整示例
支持多种方式访问 Gitpod 云端开发环境
"""

import os
import time
import json
import subprocess
from typing import Optional

# ============================================
# 方式一：Playwright 浏览器自动化（推荐）
# ============================================

def access_gitpod_via_playwright():
    """
    使用 Playwright 浏览器自动化访问 Gitpod
    需要安装：pip install playwright && playwright install chromium
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
        
        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=True)  # headless=True 适合 AI 运行
            context = browser.new_context()
            page = context.new_page()
            
            # 访问 Gitpod
            print("🚀 正在打开 Gitpod...")
            page.goto('https://gitpod.io/#https://github.com/EtAorangE/ai-cloud-ide')
            
            # 等待页面加载
            time.sleep(5)
            
            # 检查是否需要登录
            if 'login' in page.url or 'authorize' in page.url:
                print("⚠️ 需要登录 GitHub，请手动完成登录...")
                # AI 可以在这里等待用户登录，或者使用预存的 cookies
                page.wait_for_url('**/gitpod.io/workspaces*', timeout=120000)
            
            # 等待工作区启动
            print("⏳ 等待工作区启动...")
            time.sleep(30)  # Gitpod 启动需要时间
            
            # 获取工作区 URL
            workspace_url = page.url
            print(f"✅ 工作区已启动: {workspace_url}")
            
            # 现在可以操作 IDE
            # 例如：在终端输入命令
            # page.keyboard.press('Control+`')  # 打开终端
            # page.keyboard.type('python main.py')
            # page.keyboard.press('Enter')
            
            return {
                'status': 'success',
                'workspace_url': workspace_url,
                'browser': 'playwright'
            }
            
    except ImportError:
        return {'status': 'error', 'message': '请安装 playwright: pip install playwright && playwright install chromium'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


# ============================================
# 方式二：Gitpod API（需要 API Token）
# ============================================

def access_gitpod_via_api(api_token: str):
    """
    使用 Gitpod API 创建和管理工作区
    需要 Gitpod API Token（从 https://gitpod.io/tokens 获取）
    """
    import requests
    
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    # 创建工作区
    create_url = 'https://api.gitpod.io/workspaces'
    payload = {
        'contextUrl': 'https://github.com/EtAorangE/ai-cloud-ide',
        'organizationId': None  # 个人账号
    }
    
    try:
        response = requests.post(create_url, headers=headers, json=payload)
        response.raise_for_status()
        
        workspace = response.json()
        workspace_id = workspace['workspaceId']
        workspace_url = workspace['ideUrl']
        
        print(f"✅ 工作区已创建: {workspace_id}")
        print(f"🌐 访问地址: {workspace_url}")
        
        return {
            'status': 'success',
            'workspace_id': workspace_id,
            'workspace_url': workspace_url,
            'method': 'api'
        }
        
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': f'API 调用失败: {e}'}


# ============================================
# 方式三：SSH 访问（需要配置）
# ============================================

def access_via_ssh(host: str, username: str, key_path: str, command: str):
    """
    通过 SSH 访问云端 IDE 终端
    需要：pip install paramiko
    """
    try:
        import paramiko
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 连接
        client.connect(
            hostname=host,
            username=username,
            key_filename=key_path
        )
        
        # 执行命令
        stdin, stdout, stderr = client.exec_command(command)
        
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        client.close()
        
        return {
            'status': 'success',
            'output': output,
            'error': error,
            'method': 'ssh'
        }
        
    except ImportError:
        return {'status': 'error', 'message': '请安装 paramiko: pip install paramiko'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


# ============================================
# 方式四：直接 HTTP 请求（如果 IDE 暴露了 API）
# ============================================

def execute_code_via_http(workspace_url: str, code: str):
    """
    如果云端 IDE 运行了 Web 服务，可以直接通过 HTTP 调用
    """
    import requests
    
    # 假设我们在 server.py 中暴露了一个执行代码的 API
    api_url = f"{workspace_url}/api/execute"
    
    try:
        response = requests.post(api_url, json={'code': code})
        return {
            'status': 'success',
            'result': response.json(),
            'method': 'http'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


# ============================================
# 方式五：使用 Gitpod CLI
# ============================================

def access_via_gitpod_cli():
    """
    使用 Gitpod CLI 工具
    需要先安装：npm install -g gitpod-cli
    """
    try:
        # 创建工作区
        result = subprocess.run(
            ['gitpod', 'workspace', 'create', 'https://github.com/EtAorangE/ai-cloud-ide'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return {
                'status': 'success',
                'output': result.stdout,
                'method': 'cli'
            }
        else:
            return {'status': 'error', 'message': result.stderr}
            
    except FileNotFoundError:
        return {'status': 'error', 'message': '请安装 gitpod-cli: npm install -g gitpod-cli'}


# ============================================
# 完整的 AI Agent 示例
# ============================================

class CloudIDEAgent:
    """
    AI 云端 IDE 代理类
    封装了所有访问方式
    """
    
    def __init__(self, method: str = 'playwright', **kwargs):
        self.method = method
        self.config = kwargs
        self.workspace_url = None
        self.browser = None
        self.page = None
        
    def connect(self) -> dict:
        """连接到云端 IDE"""
        if self.method == 'playwright':
            return self._connect_playwright()
        elif self.method == 'api':
            return self._connect_api()
        else:
            return {'status': 'error', 'message': f'不支持的方法: {self.method}'}
    
    def _connect_playwright(self) -> dict:
        """使用 Playwright 连接"""
        try:
            from playwright.sync_api import sync_playwright
            
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            
            # 访问 Gitpod
            self.page.goto('https://gitpod.io/#https://github.com/EtAorangE/ai-cloud-ide')
            
            return {'status': 'success', 'message': '正在启动工作区...'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _connect_api(self) -> dict:
        """使用 API 连接"""
        api_token = self.config.get('api_token')
        if not api_token:
            return {'status': 'error', 'message': '需要提供 api_token'}
        
        return access_gitpod_via_api(api_token)
    
    def run_command(self, command: str) -> dict:
        """在终端执行命令"""
        if not self.page:
            return {'status': 'error', 'message': '未连接到工作区'}
        
        try:
            # 打开终端
            self.page.keyboard.press('Control+`')
            time.sleep(1)
            
            # 输入命令
            self.page.keyboard.type(command)
            self.page.keyboard.press('Enter')
            
            return {'status': 'success', 'message': f'命令已执行: {command}'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def create_file(self, filename: str, content: str) -> dict:
        """创建文件"""
        if not self.page:
            return {'status': 'error', 'message': '未连接到工作区'}
        
        try:
            # 使用快捷键创建新文件
            self.page.keyboard.press('Control+N')
            time.sleep(0.5)
            
            # 保存文件
            self.page.keyboard.press('Control+S')
            time.sleep(0.5)
            
            # 输入文件名
            self.page.keyboard.type(filename)
            self.page.keyboard.press('Enter')
            
            return {'status': 'success', 'message': f'文件已创建: {filename}'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def disconnect(self):
        """断开连接"""
        if self.browser:
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()


# ============================================
# 使用示例
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("🤖 AI 云端 IDE 访问示例")
    print("=" * 60)
    
    # 示例 1：使用 Playwright
    print("\n方式一：Playwright 浏览器自动化")
    print("-" * 40)
    result = access_gitpod_via_playwright()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 示例 2：使用 Agent 类
    print("\n方式二：使用 CloudIDEAgent 类")
    print("-" * 40)
    agent = CloudIDEAgent(method='playwright')
    connect_result = agent.connect()
    print(f"连接结果: {connect_result}")
    
    # 执行命令
    if connect_result['status'] == 'success':
        time.sleep(30)  # 等待工作区启动
        cmd_result = agent.run_command('python main.py')
        print(f"命令执行: {cmd_result}")
    
    # 断开连接
    agent.disconnect()
    print("✅ 已断开连接")
    
    print("\n" + "=" * 60)
    print("📖 更多用法请参考代码注释")
    print("=" * 60)
