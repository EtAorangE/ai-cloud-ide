#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云端 IDE 内置 API 服务
让 AI 可以通过 HTTP API 直接操作 IDE

运行方式：python api_server.py
端口：8080（Gitpod 会自动转发）
"""

import os
import json
import subprocess
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import traceback

# 工作目录
WORKSPACE = os.path.expanduser('~/workspace')

class IDEAPIHandler(BaseHTTPRequestHandler):
    """IDE API 请求处理器"""
    
    def _send_json(self, data, status=200):
        """发送 JSON 响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self._send_json({'status': 'ok'})
    
    def do_GET(self):
        """处理 GET 请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        try:
            if path == '/':
                self._handle_root()
            elif path == '/api/status':
                self._handle_status()
            elif path == '/api/files':
                self._handle_list_files()
            elif path.startswith('/api/file/'):
                filename = path[10:]  # 去掉 /api/file/
                self._handle_read_file(filename)
            else:
                self._send_json({'error': 'Not found'}, 404)
        except Exception as e:
            self._send_json({'error': str(e), 'traceback': traceback.format_exc()}, 500)
    
    def do_POST(self):
        """处理 POST 请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        # 读取请求体
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            data = {}
        
        try:
            if path == '/api/execute':
                self._handle_execute(data)
            elif path == '/api/file':
                self._handle_write_file(data)
            elif path == '/api/delete':
                self._handle_delete_file(data)
            elif path == '/api/mkdir':
                self._handle_mkdir(data)
            else:
                self._send_json({'error': 'Not found'}, 404)
        except Exception as e:
            self._send_json({'error': str(e), 'traceback': traceback.format_exc()}, 500)
    
    def _handle_root(self):
        """根路径 - API 文档"""
        docs = {
            'name': 'AI Cloud IDE API',
            'version': '1.0.0',
            'endpoints': {
                'GET /api/status': '获取 IDE 状态',
                'GET /api/files': '列出文件',
                'GET /api/file/{filename}': '读取文件内容',
                'POST /api/execute': '执行 Shell 命令',
                'POST /api/file': '创建/写入文件',
                'POST /api/delete': '删除文件',
                'POST /api/mkdir': '创建目录'
            },
            'examples': {
                'execute_command': {
                    'method': 'POST',
                    'url': '/api/execute',
                    'body': {'command': 'ls -la'}
                },
                'write_file': {
                    'method': 'POST',
                    'url': '/api/file',
                    'body': {'filename': 'test.py', 'content': 'print("Hello")'}
                }
            }
        }
        self._send_json(docs)
    
    def _handle_status(self):
        """获取 IDE 状态"""
        import platform
        import sys
        
        status = {
            'status': 'running',
            'workspace': WORKSPACE,
            'python_version': sys.version,
            'platform': platform.platform(),
            'cwd': os.getcwd()
        }
        self._send_json(status)
    
    def _handle_list_files(self):
        """列出文件"""
        path = WORKSPACE
        files = []
        
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            files.append({
                'name': item,
                'type': 'directory' if os.path.isdir(full_path) else 'file',
                'size': os.path.getsize(full_path) if os.path.isfile(full_path) else 0
            })
        
        self._send_json({'files': files, 'path': path})
    
    def _handle_read_file(self, filename):
        """读取文件内容"""
        filepath = os.path.join(WORKSPACE, filename)
        
        if not os.path.exists(filepath):
            self._send_json({'error': 'File not found'}, 404)
            return
        
        if os.path.isdir(filepath):
            self._send_json({'error': 'Is a directory'}, 400)
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self._send_json({'filename': filename, 'content': content})
        except Exception as e:
            self._send_json({'error': str(e)}, 500)
    
    def _handle_write_file(self, data):
        """写入文件"""
        filename = data.get('filename')
        content = data.get('content', '')
        
        if not filename:
            self._send_json({'error': 'filename is required'}, 400)
            return
        
        filepath = os.path.join(WORKSPACE, filename)
        
        # 确保目录存在
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else WORKSPACE, exist_ok=True)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self._send_json({'status': 'success', 'filename': filename, 'size': len(content)})
        except Exception as e:
            self._send_json({'error': str(e)}, 500)
    
    def _handle_delete_file(self, data):
        """删除文件"""
        filename = data.get('filename')
        
        if not filename:
            self._send_json({'error': 'filename is required'}, 400)
            return
        
        filepath = os.path.join(WORKSPACE, filename)
        
        if not os.path.exists(filepath):
            self._send_json({'error': 'File not found'}, 404)
            return
        
        try:
            if os.path.isdir(filepath):
                import shutil
                shutil.rmtree(filepath)
            else:
                os.remove(filepath)
            self._send_json({'status': 'success', 'deleted': filename})
        except Exception as e:
            self._send_json({'error': str(e)}, 500)
    
    def _handle_mkdir(self, data):
        """创建目录"""
        dirname = data.get('dirname')
        
        if not dirname:
            self._send_json({'error': 'dirname is required'}, 400)
            return
        
        filepath = os.path.join(WORKSPACE, dirname)
        
        try:
            os.makedirs(filepath, exist_ok=True)
            self._send_json({'status': 'success', 'created': dirname})
        except Exception as e:
            self._send_json({'error': str(e)}, 500)
    
    def _handle_execute(self, data):
        """执行 Shell 命令"""
        command = data.get('command')
        timeout = data.get('timeout', 30)
        
        if not command:
            self._send_json({'error': 'command is required'}, 400)
            return
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=WORKSPACE
            )
            
            self._send_json({
                'status': 'success',
                'command': command,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            })
        except subprocess.TimeoutExpired:
            self._send_json({'error': f'Command timed out after {timeout}s'}, 500)
        except Exception as e:
            self._send_json({'error': str(e)}, 500)
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[API] {args[0]}")


def run_server(port=8080):
    """启动 API 服务器"""
    # 确保工作目录存在
    os.makedirs(WORKSPACE, exist_ok=True)
    
    server = HTTPServer(('0.0.0.0', port), IDEAPIHandler)
    
    print("=" * 60)
    print("🚀 AI Cloud IDE API Server")
    print("=" * 60)
    print(f"🌐 服务地址: http://localhost:{port}")
    print(f"📁 工作目录: {WORKSPACE}")
    print(f"📖 API 文档: http://localhost:{port}/")
    print("=" * 60)
    print("\n按 Ctrl+C 停止服务\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
        server.shutdown()


if __name__ == '__main__':
    run_server()
