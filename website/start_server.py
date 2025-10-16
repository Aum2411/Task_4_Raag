#!/usr/bin/env python3
"""
Simple HTTP Server for RAG Agent Website
Serves the website on localhost:8000
"""
import http.server
import socketserver
import os
import sys

# Change to website directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = 8000
HOST = "127.0.0.1"  # Bind to IPv4 localhost

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add headers to prevent caching during development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

try:
    with socketserver.TCPServer((HOST, PORT), MyHTTPRequestHandler) as httpd:
        print("=" * 60)
        print("🚀 RAG Agent Website Server Started!")
        print("=" * 60)
        print(f"📡 Server running at: http://{HOST}:{PORT}")
        print(f"📡 Also accessible at: http://localhost:{PORT}")
        print("=" * 60)
        print("📝 Available pages:")
        print(f"   - Home:          http://localhost:{PORT}/#home")
        print(f"   - Features:      http://localhost:{PORT}/#features")
        print(f"   - APIs:          http://localhost:{PORT}/#apis")
        print(f"   - Demo:          http://localhost:{PORT}/#demo")
        print(f"   - Documentation: http://localhost:{PORT}/#docs")
        print("=" * 60)
        print("⏹️  Press Ctrl+C to stop the server")
        print("=" * 60)
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\n🛑 Server stopped by user")
    sys.exit(0)
except OSError as e:
    if "address already in use" in str(e).lower():
        print(f"\n❌ Error: Port {PORT} is already in use!")
        print("Please close the other application or choose a different port.")
    else:
        print(f"\n❌ Error: {e}")
    sys.exit(1)
