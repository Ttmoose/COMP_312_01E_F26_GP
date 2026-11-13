"""
wordle_logic.py
Connects the ShhRey-inspired Wordle and LetterState engine to the web server
and multi-session REST API.
"""

from __future__ import annotations

import csv
import os
import random
import threading
import time
import uuid
from typing import Any, Dict, List, Optional, Set

from letter_state import LetterState
from wordle import COLOR_PRIORITY, Wordle

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


def load_words_from_csv(file_path: Optional[str] = None) -> Set[str]:
    """Loads 5-letter words from words.csv or fallback locations."""
    candidate_paths: List[str] = []
    if file_path:
        candidate_paths.append(file_path)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidate_paths.extend([
        os.path.join(base_dir, "words.csv"),
        os.path.join(base_dir, "..", "wordle-web", "words.csv"),
        os.path.join(base_dir, "..", "words.csv"),
        "words.csv",
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
    """Wraps a Wordle game instance with thread-safety and timestamping for web sessions."""

    def __init__(self, game_id: str, secret_word: str):
        self.game_id: str = game_id
        self.wordle: Wordle = Wordle(secret_word)
        self.message: str = "Start guessing! You have 6 attempts and 5 hints."
        self.last_accessed: float = time.time()
        self._lock = threading.RLock()

    def touch(self) -> None:
        self.last_accessed = time.time()

    def to_dict(self) -> Dict[str, Any]:
        with self._lock:
            formatted_guesses = [
                {
                    "guess": word.lower(),
                    "statuses": [state.status for state in states]
                }
                for word, states in zip(self.wordle.attempts, self.wordle.results)
            ]
            return {
                "gameId": self.game_id,
                "guesses": formatted_guesses,
                "keyboardStatus": dict(self.wordle.keyboard_status),
                "attemptsRemaining": self.wordle.remaining_attempts,
                "hintsLeft": self.wordle.hints_left,
                "won": self.wordle.is_solved,
                "gameOver": self.wordle.is_game_over,
                "message": self.message,
            }


class GameService:
    """Multi-session service managing player sessions on top of the Wordle engine."""

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
        """Testing helper to start a deterministic game."""
        self._evict_old_sessions_if_needed()
        game_id = str(uuid.uuid4())
        session = GameSession(game_id, secret.lower())
        with self._global_lock:
            self.games[game_id] = session
        return session.to_dict()

    def get_game(self, game_id: str) -> Dict[str, Any]:
        return self._find_game(game_id).to_dict()

    def reset_game(self, game_id: str) -> Dict[str, Any]:
        session = self._find_game(game_id)
        with session._lock:
            new_secret = random.choice(self.word_list)
            session.wordle = Wordle(new_secret)
            session.message = "Game reset. Guess the new five-letter word."
            session.touch()
        return session.to_dict()

    def submit_guess(self, game_id: str, raw_guess: Optional[str]) -> Dict[str, Any]:
        session = self._find_game(game_id)
        with session._lock:
            session.touch()
            if session.wordle.is_game_over:
                session.message = "This game is finished. Start a new game to play again."
                return session.to_dict()

            guess = (raw_guess or "").strip().lower()

            if len(guess) != Wordle.WORD_LENGTH or not guess.isalpha():
                session.message = "Your guess must be exactly five letters."
                return session.to_dict()

            if guess not in self.dictionary:
                session.message = "That word is not in the game's dictionary."
                return session.to_dict()

            session.wordle.attempt(guess)

            if session.wordle.is_solved:
                session.message = "Genius! You guessed the word!"
            elif session.wordle.remaining_attempts <= 0:
                session.message = f"Game over! The word was {session.wordle.secret.upper()}."
            else:
                session.message = "Good guess. Keep going!"

        return session.to_dict()

    def use_hint(self, game_id: str) -> Dict[str, Any]:
        session = self._find_game(game_id)
        with session._lock:
            session.touch()
            if session.wordle.is_game_over:
                session.message = "This game is finished. Start a new game to play again."
                return session.to_dict()

            if session.wordle.hints_left <= 0:
                session.message = "You have no hints remaining."
                return session.to_dict()

            hint_result = session.wordle.use_hint()
            if hint_result is None:
                session.message = "All letters in the secret word have already been revealed or hinted!"
                return session.to_dict()

            target_letter, played_wrong = hint_result
            letter_str = target_letter.upper()
            extra = " Consider trying it in a different position." if played_wrong else ""
            session.message = f"Hint used: {letter_str} is highlighted blue on the keyboard.{extra}"

        return session.to_dict()

    @staticmethod
    def evaluate_guess(guess: str, target: str) -> List[str]:
        """Static helper returning string statuses using Wordle's evaluation."""
        dummy = Wordle(target)
        states = dummy.guess(guess)
        return [st.status for st in states]
