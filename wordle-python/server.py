"""
Zero-dependency Python HTTP Server for the Wordle Web Application.
Runs out-of-the-box on standard Python 3 with NO third-party packages required!
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from typing import Optional
from urllib.parse import urlparse

from wordle_logic import GameService


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class WordleHandler(SimpleHTTPRequestHandler):
    game_service: GameService = GameService()
    static_dir: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

    def log_message(self, format: str, *args) -> None:
        # Standard clean log output
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

    def _send_json(self, status_code: int, data: dict) -> None:
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(payload)

    def _read_json_body(self) -> dict:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length <= 0:
            return {}
        raw_body = self.rfile.read(content_length)
        try:
            return json.loads(raw_body.decode("utf-8"))
        except Exception:
            return {}

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path.rstrip("/")

        # API: GET /api/games/{id}
        if path.startswith("/api/games/"):
            game_id = path[len("/api/games/"):]
            try:
                view = self.game_service.get_game(game_id)
                self._send_json(200, view)
            except KeyError:
                self._send_json(404, {"message": "Game not found. Start a new game."})
            return

        # Serve static UI files
        self._serve_static_file(parsed_url.path)

    def do_POST(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path.rstrip("/")

        # API: POST /api/games
        if path == "/api/games":
            view = self.game_service.new_game()
            self._send_json(200, view)
            return

        # API: POST /api/games/{id}/guesses
        if path.startswith("/api/games/") and path.endswith("/guesses"):
            game_id = path[len("/api/games/"):-len("/guesses")].strip("/")
            body = self._read_json_body()
            guess = body.get("guess", "")
            try:
                view = self.game_service.submit_guess(game_id, guess)
                self._send_json(200, view)
            except KeyError:
                self._send_json(404, {"message": "Game not found. Start a new game."})
            return

        # API: POST /api/games/{id}/hint
        if path.startswith("/api/games/") and path.endswith("/hint"):
            game_id = path[len("/api/games/"):-len("/hint")].strip("/")
            try:
                view = self.game_service.use_hint(game_id)
                self._send_json(200, view)
            except KeyError:
                self._send_json(404, {"message": "Game not found. Start a new game."})
            return

        # API: POST /api/games/{id}/reset
        if path.startswith("/api/games/") and path.endswith("/reset"):
            game_id = path[len("/api/games/"):-len("/reset")].strip("/")
            try:
                view = self.game_service.reset_game(game_id)
                self._send_json(200, view)
            except KeyError:
                self._send_json(404, {"message": "Game not found. Start a new game."})
            return

        self._send_json(404, {"message": "Endpoint not found"})

    def _serve_static_file(self, req_path: str) -> None:
        clean_path = req_path.lstrip("/")
        if clean_path in ("", "index.html"):
            target_file = os.path.join(self.static_dir, "index.html")
        else:
            target_file = os.path.join(self.static_dir, clean_path)

        target_file = os.path.normpath(target_file)
        if not target_file.startswith(self.static_dir) or not os.path.isfile(target_file):
            self.send_error(404, "File Not Found")
            return

        content_type, _ = mimetypes.guess_type(target_file)
        if not content_type:
            content_type = "application/octet-stream"
        if content_type.startswith("text/") or content_type == "application/javascript":
            content_type += "; charset=utf-8"

        try:
            with open(target_file, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {e}")


def run_server(host: str = "0.0.0.0", port: int = 8080, auto_fallback: bool = True) -> None:
    current_port = port
    max_attempts = 10 if auto_fallback else 1
    httpd = None

    for attempt in range(max_attempts):
        try:
            server_address = (host, current_port)
            httpd = ThreadedHTTPServer(server_address, WordleHandler)
            break
        except OSError as e:
            if getattr(e, "errno", None) in (48, 98) and auto_fallback and attempt < max_attempts - 1:
                print(f"⚠️  Port {current_port} is already in use (e.g. by another server or Java).")
                current_port += 1
                print(f"🔄 Automatically trying port {current_port}...")
            else:
                print(f"❌ Error binding to {host}:{current_port} - {e}")
                print("\nTip: If another process (like Java Spring Boot) is using port 8080, you can:")
                print("  1. Free port 8080:  kill -9 $(lsof -t -i :8080)")
                print(f"  2. Or specify another port:  python3 server.py --port {current_port + 1}\n")
                sys.exit(1)

    display_host = "localhost" if host in ("0.0.0.0", "127.0.0.1") else host
    print("=" * 60)
    print(" Python Wordle Web Application Server")
    print(f" Web UI available at: http://{display_host}:{current_port}")
    if current_port != port:
        print(f" (Note: automatically switched from busy port {port} to {current_port})")
    print(f" Loaded {len(WordleHandler.game_service.dictionary)} words from dictionary")
    print(" Press Ctrl+C to stop the server")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        if httpd:
            httpd.server_close()
        print("Server stopped cleanly.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Wordle Web Server")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on (default: 8080)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host interface (default: 0.0.0.0)")
    args = parser.parse_args()
    run_server(args.host, args.port)
