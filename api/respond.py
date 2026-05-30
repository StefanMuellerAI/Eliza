"""Vercel Python serverless function backing the ELIZA chat UI.

Serverless functions are stateless, but ELIZA keeps state across a conversation
(it cycles through reassembly rules instead of repeating them and has a small
"memory"). To preserve that behaviour we keep the conversation on the client and
*replay* all previous user messages through a fresh ELIZA instance on every
request, then return the response to the most recent message.

Endpoints (same file, method-dispatched):
    GET  /api/respond            -> {"reply": "<greeting>"}
    POST /api/respond            -> {"reply": "<answer>", "quit": false}
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
    def _send(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        language = "en" if self.path.endswith("lang=en") else "de"
        self._send(200, build_reply([], language))

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length) or "{}")
        except (ValueError, TypeError):
            self._send(400, {"error": "invalid JSON body"})
            return

        messages = data.get("messages", [])
        language = "en" if data.get("language") == "en" else "de"

        if not isinstance(messages, list):
            self._send(400, {"error": "'messages' must be a list"})
            return
        # Keep replay cost bounded for a public demo.
        messages = [str(m) for m in messages][-200:]

        self._send(200, build_reply(messages, language))
