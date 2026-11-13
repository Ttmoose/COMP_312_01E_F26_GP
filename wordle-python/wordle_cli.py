#!/usr/bin/env python3
"""
Python Terminal / CLI version of WordleGame.
Direct port of the original Java WordleGame.java console game with ANSI colors,
colored game board, interactive virtual keyboard, hint system, and CSV dictionary loading.
"""

from __future__ import annotations

import argparse
import random
import sys
from typing import List, Optional

from wordle_logic import COLOR_PRIORITY, GameService, load_words_from_csv

# ANSI Escape Codes for Terminal Colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN_BG = "\033[42m\033[30m"    # Green background, black text
ORANGE_BG = "\033[43m\033[30m"   # Yellow/Orange background, black text
BLUE_BG = "\033[44m\033[37m"     # Blue background, white text
GREY_BG = "\033[100m\033[37m"    # Grey background, white text
WHITE_KEY = "\033[47m\033[30m"   # Unused key: light grey/white bg, black text


def format_colored_char(char: str, status: str) -> str:
    upper = char.upper()
    if status == "green":
        return f"{GREEN_BG} {upper} {RESET}"
    elif status == "orange":
        return f"{ORANGE_BG} {upper} {RESET}"
    elif status == "blue":
        return f"{BLUE_BG} {upper} {RESET}"
    else:
        return f"{GREY_BG} {upper} {RESET}"


def print_board(guesses: List[str], guess_statuses: List[List[str]]) -> None:
    print("\n--- GAME BOARD ---")
    for r in range(6):
        row_str = "| "
        for c in range(5):
            if r < len(guesses):
                letter = guesses[r][c]
                status = guess_statuses[r][c]
                row_str += format_colored_char(letter, status) + " | "
            else:
                row_str += "   | "
        print(row_str)


def print_keyboard(keyboard_status: dict) -> None:
    print("\nVirtual Keyboard (Grey < Orange < Blue < Green):")
    rows = [
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm']
    ]

    for row in rows:
        row_str = ""
        for key in row:
            status = keyboard_status.get(key)
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


def run_cli(csv_path: Optional[str] = None) -> None:
    words = load_words_from_csv(csv_path)
    word_list = sorted(list(words))
    service = GameService()
    service.dictionary = words
    service.word_list = word_list

    print("==================================")
    print("       WELCOME TO PYTHON WORDLE   ")
    print("==================================")
    print(f"Word Dictionary: Loaded {len(words)} five-letter words.")
    print("Commands during your turn: Type a 5-letter word, type 'HINT', or 'RESET'.")

    play_again = True
    while play_again:
        secret_word = random.choice(word_list)
        guesses: List[str] = []
        guess_statuses: List[List[str]] = []
        keyboard_status: dict = {}
        hints_left = 5
        won = False

        while len(guesses) < 6 and not won:
            print_board(guesses, guess_statuses)
            print_keyboard(keyboard_status)

            try:
                user_input = input(f"\nGuess #{len(guesses) + 1} (or type HINT/RESET): ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting game. Thanks for playing!")
                return

            if user_input == "reset":
                print("🔄 Resetting game...")
                break

            if user_input == "hint":
                if hints_left <= 0:
                    print("❌ No hints remaining!")
                    continue

                target_letter: Optional[str] = None
                for i in range(5):
                    letter = secret_word[i]
                    already_solved = False
                    for r, g in enumerate(guesses):
                        if g[i] == letter and guess_statuses[r][i] == "green":
                            already_solved = True
                            break
                    kbd = keyboard_status.get(letter)
                    already_hinted = (kbd in ("blue", "green"))
                    if not already_solved and not already_hinted:
                        target_letter = letter
                        break

                if target_letter is None:
                    print("✨ All letters in the secret word have already been revealed or hinted!")
                    continue

                hints_left -= 1
                curr = keyboard_status.get(target_letter)
                if curr is None or COLOR_PRIORITY["blue"] > COLOR_PRIORITY.get(curr, 0):
                    keyboard_status[target_letter] = "blue"

                print(f"💡 Hint used! {hints_left} hints remaining.")
                print(f"🔵 Letter '{target_letter.upper()}' highlighted in BLUE on keyboard.")

                if any(target_letter in g for g in guesses):
                    print(f"👉 Since '{target_letter.upper()}' was played in the wrong location before, it is suggested for your next guess!")
                continue

            if len(user_input) != 5:
                print("❌ Error: Guess must be exactly 5 letters.")
                continue

            if not user_input.isalpha():
                print("❌ Error: Guess must contain only alphabetic characters.")
                continue

            if user_input not in words:
                print("❌ Error: Not in official word list.")
                continue

            statuses = GameService.evaluate_guess(user_input, secret_word)
            guesses.append(user_input)
            guess_statuses.append(statuses)

            for i in range(5):
                letter = user_input[i]
                new_st = statuses[i]
                curr = keyboard_status.get(letter)
                if curr is None or COLOR_PRIORITY[new_st] > COLOR_PRIORITY.get(curr, 0):
                    keyboard_status[letter] = new_st

            if user_input == secret_word:
                won = True

        print_board(guesses, guess_statuses)
        if won:
            print("🎉 GENIUS! You guessed the word correctly!")
        elif len(guesses) >= 6:
            print(f"😢 Game Over! The secret word was: {secret_word.upper()}")

        try:
            resp = input("\nWould you like to play a New Game? (y/n): ").strip().lower()
            if not resp.startswith("y"):
                play_again = False
                print("Thanks for playing!")
        except (EOFError, KeyboardInterrupt):
            print("\nThanks for playing!")
            play_again = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Wordle Terminal Game")
    parser.add_argument("--csv", type=str, default=None, help="Custom CSV word list path")
    cli_args = parser.parse_args()
    run_cli(cli_args.csv)
