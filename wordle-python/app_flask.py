"""
Optional Flask implementation for users who prefer Flask / WSGI.
Run with:
    pip install flask
    python3 app_flask.py
"""

from __future__ import annotations

import os
import sys

try:
    from flask import Flask, jsonify, request, send_from_directory
except ImportError:
    print("Flask is not installed. To use the Flask server, run: pip install flask")
    print("Alternatively, you can run the zero-dependency server: python3 server.py")
    sys.exit(1)
from wordle_logic import GameService

app = Flask(__name__, static_folder="static")
service = GameService()


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/<path:path>")
def static_proxy(path: str):
    return send_from_directory("static", path)


@app.route("/api/games", methods=["POST"])
def new_game():
    return jsonify(service.new_game())


@app.route("/api/games/<game_id>", methods=["GET"])
def get_game(game_id: str):
    try:
        return jsonify(service.get_game(game_id))
    except KeyError:
        return jsonify({"message": "Game not found. Start a new game."}), 404


@app.route("/api/games/<game_id>/guesses", methods=["POST"])
def submit_guess(game_id: str):
    data = request.get_json(silent=True) or {}
    guess = data.get("guess", "")
    try:
        return jsonify(service.submit_guess(game_id, guess))
    except KeyError:
        return jsonify({"message": "Game not found. Start a new game."}), 404


@app.route("/api/games/<game_id>/hint", methods=["POST"])
def use_hint(game_id: str):
    try:
        return jsonify(service.use_hint(game_id))
    except KeyError:
        return jsonify({"message": "Game not found. Start a new game."}), 404


@app.route("/api/games/<game_id>/reset", methods=["POST"])
def reset_game(game_id: str):
    try:
        return jsonify(service.reset_game(game_id))
    except KeyError:
        return jsonify({"message": "Game not found. Start a new game."}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
