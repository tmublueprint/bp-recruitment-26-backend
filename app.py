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


VALID_STATUSES = {"pending", "shipped", "cancelled"}


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


db = get_db()


class OrderHandler(BaseHTTPRequestHandler):

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def _send_json(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/orders":
            self._send_json(404, {"error": "not found"})
            return
        try:
            body = self._read_body()
        except Exception:
            self._send_json(400, {"error": "invalid json"})
            return

        email = body.get("customer_email")
        amount = body.get("amount")
        status = body.get("status", "pending")

        if not email or not isinstance(email, str):
            self._send_json(400, {"error": "customer_email is required"})
            return
        if not isinstance(amount, (int, float)) or amount <= 0:
            self._send_json(400, {"error": "amount must be a positive number"})
            return
        if status not in VALID_STATUSES:
            self._send_json(400, {"error": "invalid status"})
            return

        created_at = datetime.now(timezone.utc).isoformat()
        cur = db.execute(
            "INSERT INTO orders (customer_email, amount, status, created_at) VALUES (?, ?, ?, ?)",
            (email, amount, status, created_at),
        )
        db.commit()
        row = db.execute("SELECT * FROM orders WHERE id = ?", (cur.lastrowid,)).fetchone()
        self._send_json(201, dict(row))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/orders":
            params = parse_qs(parsed.query)
            status_filter = params.get("status", [None])[0]
            if status_filter:
                rows = db.execute("SELECT * FROM orders WHERE status = ?", (status_filter,)).fetchall()
            else:
                rows = db.execute("SELECT * FROM orders").fetchall()
            self._send_json(200, [dict(r) for r in rows])
            return

        parts = path.split("/")
        if len(parts) == 3 and parts[0] == "" and parts[1] == "orders" and parts[2].isdigit():
            order_id = int(parts[2])
            row = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
            if row is None:
                self._send_json(404, {"error": "not found"})
            else:
                self._send_json(200, dict(row))
            return

        self._send_json(404, {"error": "not found"})

    def do_PATCH(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        parts = path.split("/")
        if not (len(parts) == 3 and parts[0] == "" and parts[1] == "orders" and parts[2].isdigit()):
            self._send_json(404, {"error": "not found"})
            return

        order_id = int(parts[2])
        try:
            body = self._read_body()
        except Exception:
            self._send_json(400, {"error": "invalid json"})
            return

        status = body.get("status")
        if not status or status not in VALID_STATUSES:
            self._send_json(400, {"error": "invalid status"})
            return

        row = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if row is None:
            self._send_json(404, {"error": "not found"})
            return

        db.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
        db.commit()
        row = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        self._send_json(200, dict(row))

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 3000), OrderHandler)
    print("Listening on port 3000")
    server.serve_forever()
