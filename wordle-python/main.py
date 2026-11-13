#!/usr/bin/env python3
"""
main.py
CLI Game Runner inspired by ShhRey/Wordle-In-Python.
Runs an interactive terminal Wordle game powered by the Wordle and LetterState classes.
"""

from __future__ import annotations

import argparse
import random
import sys
from typing import List, Optional, Set

from letter_state import LetterState
from wordle import Wordle
from wordle_logic import load_words_from_csv

# ANSI Escape Codes for Terminal Colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN_BG = "\033[42m\033[30m"    # Green background, black text
ORANGE_BG = "\033[43m\033[30m"   # Orange/Yellow background, black text
BLUE_BG = "\033[44m\033[37m"     # Blue background, white text
GREY_BG = "\033[100m\033[37m"    # Grey background, white text
WHITE_KEY = "\033[47m\033[30m"   # Unused key: light grey/white


def format_letter(letter_state: LetterState) -> str:
    char = letter_state.character
    status = letter_state.status
    if status == "green":
        return f"{GREEN_BG} {char} {RESET}"
    elif status == "orange":
        return f"{ORANGE_BG} {char} {RESET}"
    elif status == "blue":
        return f"{BLUE_BG} {char} {RESET}"
    else:
        return f"{GREY_BG} {char} {RESET}"


def display_board(wordle: Wordle) -> None:
    print("\n--- GAME BOARD ---")
    for r in range(Wordle.MAX_ATTEMPTS):
        row_str = "| "
        for c in range(Wordle.WORD_LENGTH):
            if r < len(wordle.results):
                letter_state = wordle.results[r][c]
                row_str += format_letter(letter_state) + " | "
            else:
                row_str += "   | "
        print(row_str)


def display_keyboard(wordle: Wordle) -> None:
    print("\nVirtual Keyboard (Grey < Orange < Blue < Green):")
    rows = [
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm']
    ]
    for row in rows:
        row_str = ""
        for key in row:
            status = wordle.keyboard_status.get(key)
            formatted = f" {key.upper()} "
            if status == "green":
                row_str += f"{GREEN_BG}{formatted}{RESET} "
            elif status == "blue":
                row_str += f"{BLUE_BG}{formatted}{RESET} "
            elif status == "orange":
                row_str += f"{ORANGE_BG}{formatted}{RESET} "
            elif status == "grey":
                row_str += f"{GREY_BG}{formatted}{RESET} "
            else:
                row_str += f"{WHITE_KEY}{formatted}{RESET} "
        print(row_str)


def play(words: Set[str]) -> None:
    word_list = sorted(list(words))
    print("==================================")
    print("       WELCOME TO WORDLE (PYTHON) ")
    print("==================================")
    print(f"Loaded dictionary with {len(words)} five-letter words.")
    print("Commands: Enter a 5-letter word, or type 'HINT' or 'RESET'.")

    play_again = True
    while play_again:
        secret = random.choice(word_list)
        game = Wordle(secret)

        while game.can_attempt:
            display_board(game)
            display_keyboard(game)

            attempt_num = len(game.attempts) + 1
            try:
                user_input = input(f"\nGuess #{attempt_num} (or HINT/RESET): ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting. Thanks for playing!")
                return

            if user_input == "reset":
                print("🔄 Resetting game...")
                break

            if user_input == "hint":
                hint_info = game.use_hint()
                if hint_info is None:
                    if game.hints_left <= 0:
                        print("❌ No hints remaining!")
                    else:
                        print("✨ All secret letters have already been revealed or hinted!")
                    continue

                target_letter, played_wrong = hint_info
                print(f"💡 Hint used! {game.hints_left} hints remaining.")
                print(f"🔵 Letter '{target_letter.upper()}' highlighted in BLUE on keyboard.")
                if played_wrong:
                    print(f"👉 Since '{target_letter.upper()}' was played in the wrong location before, it is suggested for your next guess!")
                continue

            if len(user_input) != Wordle.WORD_LENGTH:
                print(f"❌ Error: Guess must be exactly {Wordle.WORD_LENGTH} letters.")
                continue

            if not user_input.isalpha():
                print("❌ Error: Guess must contain only alphabetic characters.")
                continue

            if user_input not in words:
                print("❌ Error: Not in official word list.")
                continue

            game.attempt(user_input)

        display_board(game)
        if game.is_solved:
            print("🎉 GENIUS! You guessed the word correctly!")
        elif game.remaining_attempts <= 0:
            print(f"😢 Game Over! The secret word was: {game.secret.upper()}")

        try:
            resp = input("\nWould you like to play a New Game? (y/n): ").strip().lower()
            if not resp.startswith("y"):
                play_again = False
                print("Thanks for playing!")
        except (EOFError, KeyboardInterrupt):
            print("\nThanks for playing!")
            play_again = False


def main() -> None:
    parser = argparse.ArgumentParser(description="Wordle in Python (ShhRey style)")
    parser.add_argument("--csv", type=str, default=None, help="Custom CSV dictionary path")
    args = parser.parse_args()
    words = load_words_from_csv(args.csv)
    play(words)


if __name__ == "__main__":
    main()
