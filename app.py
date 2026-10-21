#!/usr/bin/env python3
"""
Online Book Store - Python Standalone Backend & REST API
Zero external dependencies required (uses standard library http.server).
Can be run with: python app.py
"""

import http.server
import socketserver
import json
import os
import sys
import mimetypes

PORT = int(os.environ.get("PORT", 8000))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load initial books dataset from json or fallback
BOOKS_DATA = [
    {
        "id": 1,
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "author": "Robert C. Martin",
        "category": "Computer Science",
        "price": 38.99,
        "originalPrice": 49.99,
        "rating": 4.8,
        "reviewsCount": 342,
        "stock": 24,
        "isbn": "978-0132350884",
        "publisher": "Prentice Hall",
        "year": 2008,
        "pages": 464,
        "featured": True,
        "cover": "https://images.unsplash.com/photo-1532012164546-f432f2e3777a?w=600",
        "description": "Even bad code can function. But if code isn't clean, it can bring a development organization to its knees.",
        "tags": ["Best Seller", "Agile", "Programming"]
    },
    {
        "id": 2,
        "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
        "author": "Erich Gamma et al.",
        "category": "Computer Science",
        "price": 44.50,
        "originalPrice": 54.99,
        "rating": 4.9,
        "reviewsCount": 512,
        "stock": 18,
        "isbn": "978-0201633610",
        "publisher": "Addison-Wesley",
        "year": 1994,
        "pages": 395,
        "featured": True,
        "cover": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600",
        "description": "Capturing a wealth of experience about the design of object-oriented software.",
        "tags": ["Classic", "OOP", "Architecture"]
    },
    {
        "id": 3,
        "title": "Atomic Habits",
        "author": "James Clear",
        "category": "Self-Help",
        "price": 19.99,
        "originalPrice": 27.00,
        "rating": 4.9,
        "reviewsCount": 1450,
        "stock": 50,
        "isbn": "978-0735211292",
        "publisher": "Avery",
        "year": 2018,
        "pages": 320,
        "featured": True,
        "cover": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=600",
        "description": "An easy and proven way to build good habits and break bad ones.",
        "tags": ["Best Seller", "Productivity"]
    }
]

ORDERS_DATA = []

class BookStoreHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/books":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "count": len(BOOKS_DATA), "data": BOOKS_DATA}).encode('utf-8'))
            return

        elif self.path == "/api/orders":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "count": len(ORDERS_DATA), "data": ORDERS_DATA}).encode('utf-8'))
            return

        elif self.path == "/api/scm/status":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            scm_info = {
                "scmEngine": "Git 2.45+ (Integrated) & PySCM Engine",
                "branch": "main",
                "status": "clean",
                "latestTag": "v1.1.0",
                "commitsCount": 8,
                "ciStatus": "Passed"
            }
            self.wfile.write(json.dumps(scm_info).encode('utf-8'))
            return

        # Default static file handling
        return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        if self.path == "/api/orders":
            try:
                order = json.loads(post_data.decode('utf-8'))
                order["id"] = "OBS-" + str(os.urandom(3).hex().upper())
                order["status"] = "Processing"
                ORDERS_DATA.append(order)

                self.send_response(201)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "data": order}).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

def run_server():
    os.chdir(BASE_DIR)
    with socketserver.TCPServer(("", PORT), BookStoreHandler) as httpd:
        print("=" * 60)
        print("🚀 Online Book Store & SCM Portal is RUNNING (Python Engine)")
        print(f"📍 URL: http://localhost:{PORT}")
        print(f"🌿 SCM Explorer: http://localhost:{PORT}#scm")
        print("=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")

if __name__ == "__main__":
    run_server()
