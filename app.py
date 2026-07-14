"""
Orders API

Implement the four endpoints below using Python's built-in http.server module.
Your server must listen on port 3000.

Docs: https://docs.python.org/3/library/http.server.html
"""

import json
import sqlite3
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


def get_db():
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_email TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL
        )
    """)
    return db


class OrderHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # POST /orders — create a new orde
        pass

    def do_GET(self):
        # GET /orders        — list all orders (optional ?status= filter)
        # GET /orders/<id>   — get a single order
        pass

    def do_PATCH(self):
        # PATCH /orders/<id> — update an order's stat
        pass

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 3000), OrderHandler)
    print("Listening on port 3000")
    server.serve_forever()
