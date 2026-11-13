"""
Core Wordle game logic and session management in Python.
Matches all rules, two-pass guess evaluation, hint handling, and keyboard priorities
from the Java Wordle application.
"""

from __future__ import annotations

import csv
import os
import random
import threading
import time
import uuid
from typing import Any, Dict, List, Optional, Set

FALLBACK_DICTIONARY: Set[str] = {
    "apple", "beach", "chair", "dance", "eagle", "faith", "grape", "happy", "image", "juice",
    "knife", "lemon", "mouse", "night", "ocean", "peace", "queen", "river", "smile", "train",
    "urban", "voice", "water", "youth", "zebra", "blend", "crane", "drift", "ember", "frost",
    "glory", "hound", "input", "jolly", "kneel", "lurch", "maple", "noble", "orbit", "pearl",
    "quake", "rider", "scope", "twist", "ultra", "vigor", "waltz", "xenon", "yield", "about",
    "above", "actor", "admit", "adopt", "adult", "after", "again", "agent", "agree", "ahead",
    "alarm", "album", "alert", "alike", "alive", "allow", "alone", "along", "alter", "among",
    "anger", "angle", "angry", "apart", "apply", "arena", "argue", "arise", "armor", "array",
    "arrow", "aside", "asset", "audio", "audit", "avoid", "award", "aware", "badly", "baker",
    "bases", "basic", "basis", "began", "begin", "begun", "being", "below", "bench", "billy",
    "birth", "black", "blame", "blind", "block", "blood", "board", "boost", "booth", "bound",
    "brain", "brand", "bread", "break", "breed", "brief", "bring", "broad", "broke", "brown",
    "brush", "build", "built", "buyer", "cable", "canal", "candy", "canon", "cargo", "carry",
    "catch", "cause", "chain", "chart", "chase", "cheap", "check", "chest", "chief", "child",
    "china", "chose", "civil", "claim", "class", "clean", "clear", "click", "clock", "close",
    "coach", "coast", "could", "count", "court", "cover", "crack", "craft", "crash", "cream",
    "crime", "cross", "crowd", "crown", "curve", "cycle", "daily", "dated", "dealt", "death",
    "debut", "delay", "depth", "dirty", "doing", "doubt", "dozen", "draft", "drama", "drawn",
    "dream", "dress", "drill", "drink", "drive", "drove", "dying", "eager", "early", "earth",
    "eaten", "eight", "elite", "empty", "enemy", "enjoy", "enter", "entry", "equal", "error",
    "event", "every", "exact", "exist", "extra", "faint", "false", "fault", "favor", "feast",
    "fence", "fetch", "fiber", "field", "fifth", "fifty", "fight", "final", "first", "fixed",
    "flash", "fleet", "floor", "fluid", "focus", "force", "forth", "forty", "forum", "found",
    "frame", "frank", "fraud", "fresh", "front", "fruit", "fully", "funny", "giant", "given",
    "glass", "globe", "glove", "going", "grace", "grade", "grand", "grant", "grass", "grave",
    "great", "green", "gross", "group", "grown", "guard", "guess", "guest", "guide", "harry",
    "heart", "heavy", "hence", "henry", "horse", "hotel", "house", "human", "ideal", "index",
    "inner", "irony", "issue", "japan", "jimmy", "joint", "jones", "judge", "known", "label",
    "large", "laser", "later", "laugh", "layer", "learn", "lease", "least", "leave", "legal",
    "level", "lewis", "light", "limit", "links", "liver", "lives", "local", "lodge", "logic",
    "loose", "lower", "lucky", "lunch", "lying", "magic", "major", "maker", "march", "maria",
    "match", "maybe", "mayor", "meant", "media", "metal", "might", "minor", "minus", "mixed",
    "model", "money", "month", "moral", "motor", "mount", "mouth", "movie", "music", "naked",
    "nasty", "naval", "needs", "never", "newly", "noise", "north", "noted", "novel", "nurse",
    "occur", "offer", "often", "order", "other", "ought", "paint", "panel", "paper", "party",
    "pasta", "patch", "pause", "phase", "phone", "photo", "piece", "pilot", "pitch", "place",
    "plain", "plane", "plant", "plate", "point", "poker", "pound", "power", "press", "price",
    "pride", "prime", "print", "prior", "prize", "proof", "proud", "prove", "quick", "quiet",
    "quite", "radio", "raise", "range", "rapid", "ratio", "reach", "react", "ready", "realm",
    "rebel", "refer", "reign", "relax", "relay", "renal", "renew", "reply", "reset", "resin",
    "ridge", "right", "rigid", "ripen", "risen", "rival", "roast", "robin", "robot", "rocky",
    "roman", "rough", "round", "route", "royal", "ruler", "rural", "scale", "scene", "score",
    "sense", "serve", "seven", "shall", "shape", "share", "sharp", "sheet", "shelf", "shell",
    "shift", "shirt", "shock", "shoot", "short", "shown", "sight", "since", "sixth", "sixty",
    "sized", "skill", "sleep", "slide", "small", "smart", "smell", "smoke", "snake", "solid",
    "solve", "sorry", "sound", "south", "space", "spare", "speak", "speed", "spend", "spent",
    "split", "spoke", "sport", "staff", "stage", "stake", "stand", "start", "state", "steam",
    "steel", "steep", "steer", "stick", "stiff", "still", "stock", "stone", "stood", "store",
    "storm", "story", "strip", "stuck", "study", "stuff", "style", "sugar", "suite", "super",
    "sweet", "swift", "swing", "sword", "table", "taken", "taste", "taxes", "teach", "teeth",
    "teddy", "tears", "tempo", "tends", "tenth", "terms", "testy", "thank", "theft", "their",
    "theme", "there", "these", "thick", "thief", "third", "those", "three", "threw", "throw",
    "thumb", "tiger", "tight", "times", "tired", "title", "today", "token", "tooth", "topic",
    "total", "touch", "tough", "tower", "track", "trade", "treat", "trend", "trial", "tribe",
    "trick", "tried", "tries", "truck", "truly", "trunk", "trust", "truth", "twice", "under",
    "union", "unity", "until", "upper", "upset", "usage", "usual", "valid", "value", "vault",
    "video", "viral", "virus", "visit", "vital", "vivid", "vocal", "wagon", "waist", "waste",
    "watch", "weary", "weigh", "weird", "welsh", "whale", "wheat", "wheel", "where", "which",
    "while", "white", "whole", "whose", "widow", "width", "woman", "women", "world", "worry",
    "worse", "worst", "worth", "would", "wound", "woven", "wrist", "write", "wrong", "yacht",
    "yards", "years", "yeast", "young", "yours", "youth", "zones",
}

COLOR_PRIORITY: Dict[str, int] = {
    "grey": 1,
    "orange": 2,
    "blue": 3,
    "green": 4,
}


def load_words_from_csv(file_path: Optional[str] = None) -> Set[str]:
    """
    Loads 5-letter words from a CSV file. If no file path is specified,
    checks standard project locations before falling back to built-in dictionary.
    """
    candidate_paths: List[str] = []
    if file_path:
        candidate_paths.append(file_path)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidate_paths.extend([
        os.path.join(base_dir, "words.csv"),
        os.path.join(base_dir, "..", "wordle-web", "words.csv"),
        os.path.join(base_dir, "..", "words.csv"),
        "words.csv",
        "wordle-web/words.csv",
        "wordle-python/words.csv",
    ])

    for path in candidate_paths:
        if os.path.isfile(path):
            try:
                words: Set[str] = set()
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        for token in row:
                            cleaned = "".join(ch for ch in token if ch.isalpha()).lower().strip()
                            if len(cleaned) == 5 and cleaned not in ("words", "word"):
                                words.add(cleaned)
                if len(words) >= 100:
                    return words
            except Exception:
                continue

    return set(FALLBACK_DICTIONARY)


class GameSession:
    """Represents an active Wordle game session for a single player/tab."""

    def __init__(self, game_id: str, secret_word: str):
        self.game_id: str = game_id
        self.secret_word: str = secret_word.lower()
        self.guesses: List[Dict[str, Any]] = []
        self.keyboard_status: Dict[str, str] = {}
        self.hints_left: int = 5
        self.won: bool = False
        self.game_over: bool = False
        self.message: str = "Start guessing! You have 6 attempts and 5 hints."
        self.last_accessed: float = time.time()
        self._lock = threading.Lock()

    def touch(self) -> None:
        self.last_accessed = time.time()

    def to_dict(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "gameId": self.game_id,
                "guesses": [dict(g) for g in self.guesses],
                "keyboardStatus": dict(self.keyboard_status),
                "attemptsRemaining": max(0, 6 - len(self.guesses)),
                "hintsLeft": self.hints_left,
                "won": self.won,
                "gameOver": self.game_over,
                "message": self.message,
            }


class GameService:
    """Manages game sessions, guess evaluation, hints, and word dictionary."""

    def __init__(self, words_file: Optional[str] = None):
        self.dictionary: Set[str] = load_words_from_csv(words_file)
        self.word_list: List[str] = sorted(list(self.dictionary))
        self.games: Dict[str, GameSession] = {}
        self._global_lock = threading.Lock()

    def _evict_old_sessions_if_needed(self) -> None:
        if len(self.games) > 500:
            two_hours_ago = time.time() - (2 * 3600)
            with self._global_lock:
                self.games = {
                    gid: game for gid, game in self.games.items()
                    if game.last_accessed >= two_hours_ago
                }

    def _find_game(self, game_id: str) -> GameSession:
        game = self.games.get(game_id)
        if game is None:
            raise KeyError("Game not found. Start a new game.")
        game.touch()
        return game

    def new_game(self) -> Dict[str, Any]:
        self._evict_old_sessions_if_needed()
        game_id = str(uuid.uuid4())
        secret = random.choice(self.word_list)
        session = GameSession(game_id, secret)
        with self._global_lock:
            self.games[game_id] = session
        return session.to_dict()

    def create_game_with_secret(self, secret: str) -> Dict[str, Any]:
        """Helper primarily for testing and deterministic setups."""
        self._evict_old_sessions_if_needed()
        game_id = str(uuid.uuid4())
        session = GameSession(game_id, secret.lower())
        with self._global_lock:
            self.games[game_id] = session
        return session.to_dict()

    def get_game(self, game_id: str) -> Dict[str, Any]:
        session = self._find_game(game_id)
        return session.to_dict()

    def reset_game(self, game_id: str) -> Dict[str, Any]:
        session = self._find_game(game_id)
        with session._lock:
            session.secret_word = random.choice(self.word_list)
            session.guesses.clear()
            session.keyboard_status.clear()
            session.hints_left = 5
            session.won = False
            session.game_over = False
            session.message = "Game reset. Guess the new five-letter word."
            session.touch()
        return session.to_dict()

    def submit_guess(self, game_id: str, raw_guess: Optional[str]) -> Dict[str, Any]:
        session = self._find_game(game_id)
        with session._lock:
            session.touch()
            if session.game_over:
                session.message = "This game is finished. Start a new game to play again."
                return {
                    "gameId": session.game_id,
                    "guesses": [dict(g) for g in session.guesses],
                    "keyboardStatus": dict(session.keyboard_status),
                    "attemptsRemaining": max(0, 6 - len(session.guesses)),
                    "hintsLeft": session.hints_left,
                    "won": session.won,
                    "gameOver": session.game_over,
                    "message": session.message,
                }

            guess = (raw_guess or "").strip().lower()

            if len(guess) != 5 or not guess.isalpha():
                session.message = "Your guess must be exactly five letters."
                return {
                    "gameId": session.game_id,
                    "guesses": [dict(g) for g in session.guesses],
                    "keyboardStatus": dict(session.keyboard_status),
                    "attemptsRemaining": max(0, 6 - len(session.guesses)),
                    "hintsLeft": session.hints_left,
                    "won": session.won,
                    "gameOver": session.game_over,
                    "message": session.message,
                }

            if guess not in self.dictionary:
                session.message = "That word is not in the game's dictionary."
                return {
                    "gameId": session.game_id,
                    "guesses": [dict(g) for g in session.guesses],
                    "keyboardStatus": dict(session.keyboard_status),
                    "attemptsRemaining": max(0, 6 - len(session.guesses)),
                    "hintsLeft": session.hints_left,
                    "won": session.won,
                    "gameOver": session.game_over,
                    "message": session.message,
                }

            statuses = self.evaluate_guess(guess, session.secret_word)
            session.guesses.append({"guess": guess, "statuses": statuses})

            for i in range(5):
                self._update_keyboard_status(session, guess[i], statuses[i])

            if guess == session.secret_word:
                session.won = True
                session.game_over = True
                session.message = "Genius! You guessed the word!"
            elif len(session.guesses) >= 6:
                session.game_over = True
                session.message = f"Game over! The word was {session.secret_word.upper()}."
            else:
                session.message = "Good guess. Keep going!"

        return session.to_dict()

    def use_hint(self, game_id: str) -> Dict[str, Any]:
        session = self._find_game(game_id)
        with session._lock:
            session.touch()
            if session.game_over:
                session.message = "This game is finished. Start a new game to play again."
                return {
                    "gameId": session.game_id,
                    "guesses": [dict(g) for g in session.guesses],
                    "keyboardStatus": dict(session.keyboard_status),
                    "attemptsRemaining": max(0, 6 - len(session.guesses)),
                    "hintsLeft": session.hints_left,
                    "won": session.won,
                    "gameOver": session.game_over,
                    "message": session.message,
                }

            if session.hints_left <= 0:
                session.message = "You have no hints remaining."
                return {
                    "gameId": session.game_id,
                    "guesses": [dict(g) for g in session.guesses],
                    "keyboardStatus": dict(session.keyboard_status),
                    "attemptsRemaining": max(0, 6 - len(session.guesses)),
                    "hintsLeft": session.hints_left,
                    "won": session.won,
                    "gameOver": session.game_over,
                    "message": session.message,
                }

            target_letter: Optional[str] = None
            for i in range(5):
                letter = session.secret_word[i]
                already_solved = False
                for g in session.guesses:
                    if g["guess"][i] == letter and g["statuses"][i] == "green":
                        already_solved = True
                        break

                kbd = session.keyboard_status.get(letter)
                already_hinted = (kbd in ("blue", "green"))
                if not already_solved and not already_hinted:
                    target_letter = letter
                    break

            if target_letter is None:
                session.message = "All letters in the secret word have already been revealed or hinted!"
                return {
                    "gameId": session.game_id,
                    "guesses": [dict(g) for g in session.guesses],
                    "keyboardStatus": dict(session.keyboard_status),
                    "attemptsRemaining": max(0, 6 - len(session.guesses)),
                    "hintsLeft": session.hints_left,
                    "won": session.won,
                    "gameOver": session.game_over,
                    "message": session.message,
                }

            session.hints_left -= 1
            self._update_keyboard_status(session, target_letter, "blue")

            played_wrong_location = any(target_letter in g["guess"] for g in session.guesses)
            letter_str = target_letter.upper()
            extra = " Consider trying it in a different position." if played_wrong_location else ""
            session.message = f"Hint used: {letter_str} is highlighted blue on the keyboard.{extra}"

        return session.to_dict()

    @staticmethod
    def evaluate_guess(guess: str, target: str) -> List[str]:
        """
        Two-pass evaluation matching Wordle rules:
        Pass 1: Exact letter & position matches -> green
        Pass 2: Letter in word but different position -> orange
        Remaining -> grey
        """
        statuses = ["grey"] * 5
        target_chars: List[Optional[str]] = list(target)

        # 1st Pass: Greens
        for i in range(5):
            if guess[i] == target_chars[i]:
                statuses[i] = "green"
                target_chars[i] = None

        # 2nd Pass: Oranges
        for i in range(5):
            if statuses[i] == "green":
                continue
            char = guess[i]
            for j in range(5):
                if target_chars[j] == char:
                    statuses[i] = "orange"
                    target_chars[j] = None
                    break

        return statuses

    @staticmethod
    def _update_keyboard_status(session: GameSession, letter: str, new_status: str) -> None:
        """
        Updates keyboard status following priority:
        grey (1) < orange (2) < blue (3) < green (4)
        """
        current = session.keyboard_status.get(letter)
        new_priority = COLOR_PRIORITY.get(new_status, 0)
        current_priority = COLOR_PRIORITY.get(current, 0) if current else 0
        if current is None or new_priority > current_priority:
            session.keyboard_status[letter] = new_status
