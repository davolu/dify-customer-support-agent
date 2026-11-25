"""Tiny mock order-status API for the Nimbus Coffee Co. tutorial.

GET /orders/<ORDER_ID>  -> 200 + order JSON, or 404 {"error": "not_found"}
GET /health             -> 200 {"ok": true}

Standard library only. All data is fictional.
"""
import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ORDERS_DIR = Path(__file__).parent / "orders"
ORDER_RE = re.compile(r"^/orders/(NMB-\d{4})/?$", re.IGNORECASE)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.rstrip("/") == "/health":
            return self._send(200, {"ok": True})
        m = ORDER_RE.match(self.path.split("?")[0])
        if not m:
            return self._send(404, {"error": "not_found"})
        f = ORDERS_DIR / f"{m.group(1).upper()}.json"
        if not f.exists():
            return self._send(404, {"error": "not_found", "order_id": m.group(1).upper()})
        return self._send(200, json.loads(f.read_text()))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Nimbus mock API on :{port}")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
