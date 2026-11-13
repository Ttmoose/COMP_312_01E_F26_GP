"""
letter_state.py
Inspired by ShhRey/Wordle-In-Python (and Pixegami).
Tracks whether an individual character in a guess is in the secret word
and whether it is in the exact position.
"""

from __future__ import annotations


class LetterState:
    """Represents the status of an individual letter within a guessed word."""

    def __init__(self, character: str):
        self.character: str = character.upper()
        self.is_in_word: bool = False
        self.is_in_position: bool = False

    @property
    def status(self) -> str:
        """Returns the color status string: 'green', 'orange', or 'grey'."""
        if self.is_in_position:
            return "green"
        if self.is_in_word:
            return "orange"
        return "grey"

    def __repr__(self) -> str:
        return f"[{self.character} in_word={self.is_in_word} in_pos={self.is_in_position}]"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LetterState):
            return False
        return (
            self.character == other.character
            and self.is_in_word == other.is_in_word
            and self.is_in_position == other.is_in_position
        )
