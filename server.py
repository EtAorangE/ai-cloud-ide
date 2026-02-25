#!/usr/bin/env python3
"""
简单的 Web 服务器示例
运行: python server.py
访问: http://localhost:8080
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

class APIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/hello':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'message': 'Hello from AI Cloud IDE!',
                'status': 'success',
                'timestamp': str(__import__('datetime').datetime.now())
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            super().do_GET()

if __name__ == '__main__':
    PORT = 8080
    server = HTTPServer(('0.0.0.0', PORT), APIHandler)
    print(f"🌐 Server running at http://localhost:{PORT}")
    print(f"📡 API endpoint: http://localhost:{PORT}/api/hello")
    print("Press Ctrl+C to stop...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        server.shutdown()
