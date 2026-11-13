# Wordle in Python (Built on ShhRey's Architecture)

A modular Python implementation of Wordle built on the architectural foundation of **[ShhRey/Wordle-In-Python](https://github.com/ShhRey/Wordle-In-Python)** (and Pixegami's design), expanded to support both an **interactive terminal CLI game** and a **zero-dependency full-stack Web application**.

---

## 🏛️ Architecture & Component Design

The codebase adopts ShhRey's clean object-oriented structure:

1. **`letter_state.py` (`LetterState`)**:
   - Represents the state of an individual character within a guess.
   - Properties: `character`, `is_in_word`, `is_in_position`, and `status` (`"green"`, `"orange"`, or `"grey"`).

2. **`wordle.py` (`Wordle`)**:
   - The central game engine class.
   - Encapsulates `secret`, `attempts`, `results`, `keyboard_status`, and `hints_left`.
   - Uses a two-pass matching algorithm in `guess(word)` to properly handle duplicate letters (e.g., `AGREE` vs. `CRANE`).
   - Properties: `is_solved`, `remaining_attempts`, `can_attempt`, `is_game_over`.

3. **`main.py` (CLI Runner)**:
   - Terminal game runner inspired by ShhRey's `main.py`.
   - Imports `Wordle` and `LetterState` to render the colored ANSI game board and interactive virtual keyboard.

4. **`wordle_logic.py` (`GameService` & `GameSession`)**:
   - Multi-session service layer wrapping `Wordle` instances to support multiple concurrent players and browser tabs.

5. **`server.py` (Web Server & REST API)**:
   - Standard-library multithreaded HTTP server exposing REST endpoints (`/api/games/*`) and serving the responsive web UI.

---

## 🚀 How to Run

### 1. Terminal / CLI Game (ShhRey Style)
```bash
cd wordle-python
python3 main.py
```
*(Or run `python3 wordle_cli.py`)*

- Enter a 5-letter word to guess.
- Type `HINT` during your turn to reveal an unrevealed letter in blue (up to 5 hints).
- Type `RESET` to restart the current game round.

### 2. Browser Web Application
```bash
cd wordle-python
python3 server.py
# (or './run.sh')
```
Then visit **<http://localhost:8080>**.

*(If port 8080 is already occupied, the server automatically switches to port 8081).*

---

## 🧪 Automated Test Suite

Includes 22 unit and integration tests covering `LetterState`, `Wordle`, `GameService`, and the HTTP API:

```bash
cd wordle-python
python3 test_wordle.py
```

---

## 📁 File Structure

```text
wordle-python/
├── letter_state.py      # LetterState class (character, is_in_word, is_in_position)
├── wordle.py            # Wordle class (attempts, two-pass evaluation, hints)
├── main.py              # Interactive CLI game runner
├── wordle_cli.py        # Convenience launcher for main.py
├── wordle_logic.py      # Multi-session GameService wrapping Wordle
├── server.py            # Zero-dependency Web Server & REST API
├── run.sh               # Quick startup shell script
├── test_wordle.py       # 22 automated unit and integration tests
├── words.csv            # 607-word five-letter dictionary
├── app_flask.py         # Optional Flask alternative
└── static/              # Browser UI assets (HTML, CSS, JavaScript)
    ├── index.html
    ├── style.css
    └── app.js
```
