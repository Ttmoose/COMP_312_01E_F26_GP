"""
wordle.py
Core game engine class Wordle inspired by ShhRey/Wordle-In-Python.
Manages attempts, evaluations using LetterState, remaining guesses, win/loss states,
plus support for hints and keyboard tracking.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from letter_state import LetterState

COLOR_PRIORITY: Dict[str, int] = {
    "grey": 1,
    "orange": 2,
    "blue": 3,
    "green": 4,
}


class Wordle:
    MAX_ATTEMPTS: int = 6
    WORD_LENGTH: int = 5
    MAX_HINTS: int = 5

    def __init__(self, secret: str):
        self.secret: str = secret.upper()
        self.attempts: List[str] = []
        self.results: List[List[LetterState]] = []
        self.keyboard_status: Dict[str, str] = {}
        self.hints_left: int = self.MAX_HINTS

    @property
    def is_solved(self) -> bool:
        return len(self.attempts) > 0 and self.attempts[-1] == self.secret

    @property
    def remaining_attempts(self) -> int:
        return max(0, self.MAX_ATTEMPTS - len(self.attempts))

    @property
    def can_attempt(self) -> bool:
        return self.remaining_attempts > 0 and not self.is_solved

    @property
    def is_game_over(self) -> bool:
        return self.is_solved or self.remaining_attempts <= 0

    def guess(self, word: str) -> List[LetterState]:
        """
        Evaluates a word against the secret word using a two-pass algorithm
        to correctly handle duplicate letters (e.g. AGREE against CRANE).
        Returns a list of LetterState objects.
        """
        word = word.upper()
        result: List[LetterState] = [LetterState(c) for c in word]
        secret_letters: List[Optional[str]] = list(self.secret)

        # 1st Pass: Exact position matches (Green)
        for i in range(min(len(word), self.WORD_LENGTH)):
            if word[i] == secret_letters[i]:
                result[i].is_in_position = True
                result[i].is_in_word = True
                secret_letters[i] = None

        # 2nd Pass: Letters present in wrong positions (Orange/Yellow)
        for i in range(min(len(word), self.WORD_LENGTH)):
            if result[i].is_in_position:
                continue
            char = word[i]
            if char in secret_letters:
                result[i].is_in_word = True
                # Consume the letter instance to prevent duplicate markings
                secret_letters[secret_letters.index(char)] = None

        return result

    def attempt(self, word: str) -> List[LetterState]:
        """Submits an attempt, updates history and keyboard state."""
        word = word.upper()
        letter_states = self.guess(word)
        self.attempts.append(word)
        self.results.append(letter_states)

        # Update keyboard statuses according to priority hierarchy
        for state in letter_states:
            self.update_keyboard_status(state.character.lower(), state.status)

        return letter_states

    def update_keyboard_status(self, letter: str, new_status: str) -> None:
        """Updates keyboard status following: grey (1) < orange (2) < blue (3) < green (4)."""
        letter = letter.lower()
        current = self.keyboard_status.get(letter)
        new_pri = COLOR_PRIORITY.get(new_status, 0)
        curr_pri = COLOR_PRIORITY.get(current, 0) if current else 0
        if current is None or new_pri > curr_pri:
            self.keyboard_status[letter] = new_status

    def use_hint(self) -> Optional[tuple[str, bool]]:
        """
        Uses a hint if available. Returns (target_letter, played_wrong_location) or None.
        """
        if self.hints_left <= 0 or self.is_game_over:
            return None

        target_letter: Optional[str] = None
        for i in range(self.WORD_LENGTH):
            letter = self.secret[i].lower()
            already_solved = any(
                len(r) > i and r[i].character.lower() == letter and r[i].is_in_position
                for r in self.results
            )
            kbd = self.keyboard_status.get(letter)
            already_hinted = (kbd in ("blue", "green"))
            if not already_solved and not already_hinted:
                target_letter = letter
                break

        if target_letter is None:
            return None

        self.hints_left -= 1
        self.update_keyboard_status(target_letter, "blue")
        played_wrong_location = any(target_letter.upper() in a for a in self.attempts)
        return (target_letter, played_wrong_location)
