"""Arcade cabinet. Loopback only. pythonw + no extra windows."""
from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent
PORT = 8933
DIGNITY = Path(r"C:\Users\zizox\Desktop\CODE\dignity-coin-rush\app\src\main\assets\index.html")
CYBER = Path(r"C:\Users\zizox\Desktop\CYBER TOWN\game\little-mind-layered-town-v6.html")
PID = ROOT / "app.pid"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        path = unquote(self.path.split("?", 1)[0])
        if path in ("/", "/index.html"):
            return self._send_file(ROOT / "index.html", "text/html; charset=utf-8")
        if path == "/carts.json":
            return self._send_file(ROOT / "carts.json", "application/json")
        if path == "/play/dignity":
            return self._send_file(DIGNITY, "text/html; charset=utf-8")
        if path == "/play/cyber":
            return self._send_file(CYBER, "text/html; charset=utf-8")
        return super().do_GET()

    def _send_file(self, p: Path, ctype: str):
        if not p.is_file():
            self.send_error(404, f"missing {p.name}")
            return
        data = p.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


def main():
    PID.write_text(str(PORT), encoding="utf-8")
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
