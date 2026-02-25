// AI Cloud IDE - Node.js 示例
// 运行: node index.js

const http = require('http');

const PORT = 3000;

const server = http.createServer((req, res) => {
  if (req.url === '/api/hello') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      message: 'Hello from AI Cloud IDE!',
      runtime: 'Node.js',
      version: process.version,
      timestamp: new Date().toISOString()
    }));
  } else {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`
      <html>
        <head><title>AI Cloud IDE</title></head>
        <body>
          <h1>🚀 AI Cloud IDE</h1>
          <p>Welcome to your AI-accessible development environment!</p>
          <p>API: <a href="/api/hello">/api/hello</a></p>
        </body>
      </html>
    `);
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`🌐 Server running at http://localhost:${PORT}`);
  console.log(`📡 API endpoint: http://localhost:${PORT}/api/hello`);
});
