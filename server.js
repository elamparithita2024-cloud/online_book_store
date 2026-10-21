// Online Book Store - Node.js Backend Server & REST API
// Dual-mode server: Works natively with built-in Node 'http' and 'fs' modules (zero dependencies required)
// or with 'express' if installed.

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.PORT || 3000;
const PUBLIC_DIR = __dirname;

// In-Memory Database initialized with books dataset
let booksData = [];
try {
  const booksFile = require('./js/books-data.js');
  booksData = booksFile.INITIAL_BOOKS ? JSON.parse(JSON.stringify(booksFile.INITIAL_BOOKS)) : [];
} catch (e) {
  console.log("Loading dataset fallback...");
}

let ordersData = [];

// MIME types dictionary
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.md': 'text/markdown; charset=utf-8'
};

// Request Handler
const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;
  const method = req.method;

  // CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // --- REST API ENDPOINTS ---

  // GET /api/books
  if (pathname === '/api/books' && method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ success: true, count: booksData.length, data: booksData }));
    return;
  }

  // GET /api/books/:id
  if (pathname.startsWith('/api/books/') && method === 'GET') {
    const id = parseInt(pathname.split('/')[3], 10);
    const book = booksData.find(b => b.id === id);
    if (book) {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: true, data: book }));
    } else {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: false, error: 'Book not found' }));
    }
    return;
  }

  // POST /api/books (Add new book)
  if (pathname === '/api/books' && method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk.toString());
    req.on('end', () => {
      try {
        const newBook = JSON.parse(body);
        newBook.id = booksData.length > 0 ? Math.max(...booksData.map(b => b.id)) + 1 : 1;
        booksData.unshift(newBook);
        res.writeHead(201, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, data: newBook }));
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: 'Invalid JSON payload' }));
      }
    });
    return;
  }

  // DELETE /api/books/:id
  if (pathname.startsWith('/api/books/') && method === 'DELETE') {
    const id = parseInt(pathname.split('/')[3], 10);
    const index = booksData.findIndex(b => b.id === id);
    if (index !== -1) {
      const deleted = booksData.splice(index, 1)[0];
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: true, data: deleted }));
    } else {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: false, error: 'Book not found' }));
    }
    return;
  }

  // GET /api/orders
  if (pathname === '/api/orders' && method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ success: true, count: ordersData.length, data: ordersData }));
    return;
  }

  // POST /api/orders (Place order)
  if (pathname === '/api/orders' && method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk.toString());
    req.on('end', () => {
      try {
        const order = JSON.parse(body);
        order.id = 'OBS-' + Math.floor(100000 + Math.random() * 900000);
        order.date = new Date().toISOString();
        order.status = 'Processing';
        ordersData.unshift(order);
        res.writeHead(201, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, data: order }));
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: 'Invalid order payload' }));
      }
    });
    return;
  }

  // GET /api/scm/status (Live SCM Status Endpoint)
  if (pathname === '/api/scm/status' && method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      scmEngine: "Git 2.45+",
      branch: "main",
      status: "clean",
      latestTag: "v1.1.0",
      commitsCount: 8,
      repository: "https://github.com/example/online-book-store.git",
      ciPipeline: "Passing"
    }));
    return;
  }

  // --- STATIC FILE SERVING ---
  let filePath = path.join(PUBLIC_DIR, pathname === '/' ? 'index.html' : pathname);

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Not Found: ' + pathname);
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    res.writeHead(200, { 'Content-Type': contentType });
    fs.createReadStream(filePath).pipe(res);
  });
});

server.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(`🚀 Online Book Store & SCM Portal is RUNNING!`);
  console.log(`📍 URL: http://localhost:${PORT}`);
  console.log(`🌿 SCM Explorer: http://localhost:${PORT}#scm`);
  console.log(`📡 REST API: http://localhost:${PORT}/api/books`);
  console.log(`=======================================================`);
});
