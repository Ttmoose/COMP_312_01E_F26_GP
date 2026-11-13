"""
Unit and Integration Tests for Python Wordle.
Tests LetterState, Wordle, GameService, and the HTTP server endpoints.
"""

from __future__ import annotations

import io
import json
import unittest
from unittest.mock import MagicMock

from letter_state import LetterState
from server import WordleHandler
from wordle import Wordle
from wordle_logic import GameService


class TestLetterState(unittest.TestCase):
    """Tests the LetterState class (from ShhRey / Pixegami design)."""

    def test_letter_state_defaults(self) -> None:
        state = LetterState("a")
        self.assertEqual("A", state.character)
        self.assertFalse(state.is_in_word)
        self.assertFalse(state.is_in_position)
        self.assertEqual("grey", state.status)

    def test_letter_state_in_word(self) -> None:
        state = LetterState("e")
        state.is_in_word = True
        self.assertEqual("orange", state.status)

    def test_letter_state_in_position(self) -> None:
        state = LetterState("c")
        state.is_in_word = True
        state.is_in_position = True
        self.assertEqual("green", state.status)


class TestWordleEngine(unittest.TestCase):
    """Tests the Wordle engine class (from ShhRey / Pixegami design)."""

    def test_wordle_initialization(self) -> None:
        w = Wordle("apple")
        self.assertEqual("APPLE", w.secret)
        self.assertEqual([], w.attempts)
        self.assertEqual([], w.results)
        self.assertEqual(6, w.remaining_attempts)
        self.assertTrue(w.can_attempt)
        self.assertFalse(w.is_solved)
        self.assertFalse(w.is_game_over)

    def test_wordle_guess_and_attempt(self) -> None:
        w = Wordle("crane")
        states = w.attempt("beach")

        self.assertEqual(1, len(w.attempts))
        self.assertEqual("BEACH", w.attempts[0])
        self.assertEqual(5, w.remaining_attempts)
        self.assertEqual(["grey", "orange", "green", "orange", "grey"], [s.status for s in states])

    def test_wordle_solved(self) -> None:
        w = Wordle("apple")
        w.attempt("apple")
        self.assertTrue(w.is_solved)
        self.assertTrue(w.is_game_over)
        self.assertFalse(w.can_attempt)

    def test_wordle_hints(self) -> None:
        w = Wordle("orbit")
        hint1 = w.use_hint()
        self.assertIsNotNone(hint1)
        self.assertEqual(4, w.hints_left)
        target_char, _ = hint1
        self.assertEqual("blue", w.keyboard_status.get(target_char))


class TestWordleService(unittest.TestCase):

    def setUp(self) -> None:
        self.service = GameService()

    def test_game_initialization(self) -> None:
        game = self.service.new_game()
        self.assertIsNotNone(game["gameId"])
        self.assertEqual(6, game["attemptsRemaining"])
        self.assertEqual(5, game["hintsLeft"])
        self.assertEqual([], game["guesses"])
        self.assertEqual({}, game["keyboardStatus"])
        self.assertFalse(game["won"])
        self.assertFalse(game["gameOver"])

    def test_exact_guess_wins_game(self) -> None:
        game = self.service.create_game_with_secret("apple")
        result = self.service.submit_guess(game["gameId"], "apple")

        self.assertTrue(result["won"])
        self.assertTrue(result["gameOver"])
        self.assertEqual(5, result["attemptsRemaining"])
        self.assertEqual(1, len(result["guesses"]))

        guess_result = result["guesses"][0]
        self.assertEqual("apple", guess_result["guess"])
        self.assertEqual(["green", "green", "green", "green", "green"], guess_result["statuses"])

        self.assertEqual("green", result["keyboardStatus"].get("a"))
        self.assertEqual("green", result["keyboardStatus"].get("p"))
        self.assertEqual("green", result["keyboardStatus"].get("l"))
        self.assertEqual("green", result["keyboardStatus"].get("e"))

    def test_partial_matches_evaluation(self) -> None:
        game = self.service.create_game_with_secret("crane")
        result = self.service.submit_guess(game["gameId"], "beach")

        self.assertFalse(result["won"])
        self.assertFalse(result["gameOver"])
        self.assertEqual(5, result["attemptsRemaining"])

        statuses = result["guesses"][0]["statuses"]
        self.assertEqual(["grey", "orange", "green", "orange", "grey"], statuses)

        self.assertEqual("grey", result["keyboardStatus"].get("b"))
        self.assertEqual("orange", result["keyboardStatus"].get("e"))
        self.assertEqual("green", result["keyboardStatus"].get("a"))
        self.assertEqual("orange", result["keyboardStatus"].get("c"))
        self.assertEqual("grey", result["keyboardStatus"].get("h"))

    def test_duplicate_letter_evaluation(self) -> None:
        game = self.service.create_game_with_secret("crane")
        result = self.service.submit_guess(game["gameId"], "agree")

        self.assertEqual(1, len(result["guesses"]))
        statuses = result["guesses"][0]["statuses"]
        self.assertEqual("orange", statuses[0], "A should be orange")
        self.assertEqual("grey", statuses[1], "G should be grey")
        self.assertEqual("orange", statuses[2], "R should be orange")
        self.assertEqual("grey", statuses[3], "First E should be grey")
        self.assertEqual("green", statuses[4], "Second E should be green")

    def test_color_priority_on_keyboard(self) -> None:
        game = self.service.create_game_with_secret("crane")

        self.service.submit_guess(game["gameId"], "solid")
        current_game = self.service.get_game(game["gameId"])
        self.assertEqual("grey", current_game["keyboardStatus"].get("s"))

        after_hint = self.service.use_hint(game["gameId"])
        self.assertEqual(4, after_hint["hintsLeft"])

        blue_letters = [k for k, v in after_hint["keyboardStatus"].items() if v == "blue"]
        self.assertTrue(len(blue_letters) >= 1)
        blue_letter = blue_letters[0]

        after_win = self.service.submit_guess(game["gameId"], "crane")
        self.assertEqual("green", after_win["keyboardStatus"].get(blue_letter))

    def test_invalid_guess_length_rejected(self) -> None:
        game = self.service.new_game()

        r1 = self.service.submit_guess(game["gameId"], "cat")
        self.assertEqual(6, r1["attemptsRemaining"])
        self.assertEqual([], r1["guesses"])

        r2 = self.service.submit_guess(game["gameId"], "banana")
        self.assertEqual(6, r2["attemptsRemaining"])
        self.assertEqual([], r2["guesses"])

    def test_word_not_in_dictionary_rejected(self) -> None:
        game = self.service.new_game()
        result = self.service.submit_guess(game["gameId"], "zzzzz")

        self.assertEqual(6, result["attemptsRemaining"])
        self.assertEqual([], result["guesses"])
        self.assertIn("not in", result["message"].lower())

    def test_consecutive_hints_reveal_different_letters(self) -> None:
        game = self.service.create_game_with_secret("orbit")

        h1 = self.service.use_hint(game["gameId"])
        self.assertEqual(4, h1["hintsLeft"])
        blue1 = sum(1 for v in h1["keyboardStatus"].values() if v == "blue")
        self.assertEqual(1, blue1)

        h2 = self.service.use_hint(game["gameId"])
        self.assertEqual(3, h2["hintsLeft"])
        blue2 = sum(1 for v in h2["keyboardStatus"].values() if v == "blue")
        self.assertEqual(2, blue2)

        h3 = self.service.use_hint(game["gameId"])
        self.assertEqual(2, h3["hintsLeft"])
        blue3 = sum(1 for v in h3["keyboardStatus"].values() if v == "blue")
        self.assertEqual(3, blue3)

    def test_no_hints_remaining(self) -> None:
        game = self.service.create_game_with_secret("orbit")
        for _ in range(5):
            self.service.use_hint(game["gameId"])

        exhausted = self.service.get_game(game["gameId"])
        self.assertEqual(0, exhausted["hintsLeft"])

        extra = self.service.use_hint(game["gameId"])
        self.assertEqual(0, extra["hintsLeft"])
        self.assertIn("no hints remaining", extra["message"].lower())

    def test_game_over_after_six_failed_guesses(self) -> None:
        game = self.service.create_game_with_secret("apple")
        guesses = ["beach", "chair", "dance", "eagle", "faith", "grape"]
        curr = game
        for g in guesses:
            curr = self.service.submit_guess(game["gameId"], g)

        self.assertEqual(0, curr["attemptsRemaining"])
        self.assertEqual(6, len(curr["guesses"]))
        self.assertTrue(curr["gameOver"])
        self.assertFalse(curr["won"])
        self.assertIn("game over", curr["message"].lower())
        self.assertIn("APPLE", curr["message"])

    def test_guess_after_game_over_rejected(self) -> None:
        game = self.service.create_game_with_secret("apple")
        self.service.submit_guess(game["gameId"], "apple")

        extra = self.service.submit_guess(game["gameId"], "beach")
        self.assertEqual(1, len(extra["guesses"]))
        self.assertIn("finished", extra["message"].lower())

    def test_reset_game_preserves_session_id(self) -> None:
        original = self.service.create_game_with_secret("apple")
        original_id = original["gameId"]

        self.service.submit_guess(original_id, "beach")
        self.service.use_hint(original_id)

        reset = self.service.reset_game(original_id)
        self.assertEqual(original_id, reset["gameId"])
        self.assertEqual(6, reset["attemptsRemaining"])
        self.assertEqual(5, reset["hintsLeft"])
        self.assertEqual([], reset["guesses"])
        self.assertEqual({}, reset["keyboardStatus"])
        self.assertFalse(reset["won"])
        self.assertFalse(reset["gameOver"])

    def test_dictionary_loaded(self) -> None:
        d = self.service.dictionary
        self.assertGreaterEqual(len(d), 600)
        for w in d:
            self.assertEqual(5, len(w))
            self.assertTrue(w.isalpha())
            self.assertTrue(w.islower())


class FakeSocket:
    def __init__(self, raw_input: bytes):
        self.rfile = io.BytesIO(raw_input)
        self.wfile = io.BytesIO()

    def makefile(self, mode: str, *args, **kwargs):
        if "r" in mode:
            return self.rfile
        return self.wfile

    def sendall(self, data: bytes) -> None:
        self.wfile.write(data)


class TestHttpServerHandler(unittest.TestCase):

    def _execute_request(self, method: str, path: str, body: dict = None) -> tuple[int, dict]:
        body_bytes = json.dumps(body).encode("utf-8") if body else b""
        raw_http = (
            f"{method} {path} HTTP/1.1\r\n"
            f"Host: localhost\r\n"
            f"Content-Type: application/json\r\n"
            f"Content-Length: {len(body_bytes)}\r\n\r\n"
        ).encode("utf-8") + body_bytes

        sock = FakeSocket(raw_http)
        server = MagicMock()

        handler = WordleHandler(sock, ("127.0.0.1", 12345), server)
        output = sock.wfile.getvalue().decode("utf-8")

        lines = output.split("\r\n")
        status_line = lines[0]
        status_code = int(status_line.split(" ")[1])

        empty_index = output.find("\r\n\r\n")
        json_body = json.loads(output[empty_index + 4:]) if empty_index != -1 else {}
        return status_code, json_body

    def test_api_flow(self) -> None:
        code, game = self._execute_request("POST", "/api/games")
        self.assertEqual(200, code)
        self.assertIn("gameId", game)
        game_id = game["gameId"]

        code, fetched = self._execute_request("GET", f"/api/games/{game_id}")
        self.assertEqual(200, code)
        self.assertEqual(game_id, fetched["gameId"])

        code, guessed = self._execute_request("POST", f"/api/games/{game_id}/guesses", {"guess": "beach"})
        self.assertEqual(200, code)
        self.assertEqual(1, len(guessed["guesses"]))
        self.assertEqual(5, guessed["attemptsRemaining"])

        code, hinted = self._execute_request("POST", f"/api/games/{game_id}/hint")
        self.assertEqual(200, code)
        self.assertEqual(4, hinted["hintsLeft"])

        code, reset = self._execute_request("POST", f"/api/games/{game_id}/reset")
        self.assertEqual(200, code)
        self.assertEqual(game_id, reset["gameId"])
        self.assertEqual(6, reset["attemptsRemaining"])
        self.assertEqual(5, reset["hintsLeft"])

        code, error = self._execute_request("GET", "/api/games/unknown-id")
        self.assertEqual(404, code)
        self.assertIn("message", error)

    def test_static_files_served(self) -> None:
        raw_http = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        sock = FakeSocket(raw_http)
        WordleHandler(sock, ("127.0.0.1", 12345), MagicMock())
        output = sock.wfile.getvalue().decode("utf-8")
        self.assertIn("200 OK", output)
        self.assertIn("<!DOCTYPE html>", output)

        raw_http_css = b"GET /style.css HTTP/1.1\r\nHost: localhost\r\n\r\n"
        sock_css = FakeSocket(raw_http_css)
        WordleHandler(sock_css, ("127.0.0.1", 12345), MagicMock())
        output_css = sock_css.wfile.getvalue().decode("utf-8")
        self.assertIn("200 OK", output_css)
        self.assertIn("text/css", output_css)


if __name__ == "__main__":
    unittest.main()
