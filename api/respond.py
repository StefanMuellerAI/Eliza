"""Vercel Python entrypoint for the ELIZA demo.

Vercel's Python runtime loads the `handler` class below (configured via
`pyproject.toml` -> `[tool.vercel] entrypoint = "api.respond:handler"`).

This single handler serves everything:
  * GET/POST /api/respond  -> the ELIZA chat JSON API
  * any other GET path      -> the static frontend from public/

ELIZA keeps state across a conversation (it cycles through reassembly rules and
has a small "memory"). Serverless functions are stateless, so the client keeps
the conversation and sends all previous user messages with each request; we
*replay* them through a fresh ELIZA instance and answer the most recent one.

    GET  /api/respond[?lang=en]   -> {"reply": "<greeting>", "quit": false}
    POST /api/respond             -> {"reply": "<answer>", "quit": <bool>}
        body: {"messages": ["...", "..."], "language": "de"}
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler

# Make the `eliza` package importable regardless of the runtime CWD.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from eliza.engine import load_doctor  # noqa: E402

PUBLIC_DIR = os.path.join(REPO_ROOT, "public")
API_PATH = "/api/respond"

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".json": "application/json; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
}


def build_reply(messages, language):
    """Replay `messages` (user turns) and return the response to the last one."""
    eliza = load_doctor(language)
    if not messages:
        return {"reply": eliza.initial(), "quit": False}

    reply = None
    quit_flag = False
    for message in messages:
        reply = eliza.respond(message or "")
        if reply is None:
            reply = eliza.final()
            quit_flag = True
            break
    return {"reply": reply, "quit": quit_flag}


class handler(BaseHTTPRequestHandler):
    # ----------------------------------------------------------------- helpers
    def _send_bytes(self, status, body, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _path(self):
        return self.path.split("?", 1)[0]

    def _is_api(self):
        return self._path().rstrip("/") == API_PATH

    def _serve_static(self):
        path = self._path()
        if path in ("", "/"):
            path = "/index.html"
        full = os.path.normpath(os.path.join(PUBLIC_DIR, path.lstrip("/")))
        if not full.startswith(PUBLIC_DIR) or not os.path.isfile(full):
            self._send_bytes(404, b"Not found", "text/plain; charset=utf-8")
            return
        ext = os.path.splitext(full)[1].lower()
        with open(full, "rb") as f:
            data = f.read()
        self._send_bytes(200, data, CONTENT_TYPES.get(ext, "application/octet-stream"))

    # ------------------------------------------------------------------ routes
    def do_GET(self):
        if self._is_api():
            language = "en" if "lang=en" in self.path else "de"
            self._send_json(200, build_reply([], language))
        else:
            self._serve_static()

    def do_POST(self):
        if not self._is_api():
            self._send_bytes(404, b"Not found", "text/plain; charset=utf-8")
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length) or "{}")
        except (ValueError, TypeError):
            self._send_json(400, {"error": "invalid JSON body"})
            return

        messages = data.get("messages", [])
        language = "en" if data.get("language") == "en" else "de"
        if not isinstance(messages, list):
            self._send_json(400, {"error": "'messages' must be a list"})
            return
        # Keep replay cost bounded for a public demo.
        messages = [str(m) for m in messages][-200:]
        self._send_json(200, build_reply(messages, language))

    def log_message(self, *args):  # quieter logs
        pass
