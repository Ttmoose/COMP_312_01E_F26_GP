# Wordle in Python (Web & CLI)

A complete Python port of the Java Wordle application, featuring both a **browser-based web game** and an **interactive terminal (CLI) game**.

---

## 🌟 Key Features

- **Zero-Dependency Web Server**: Built using Python 3's standard library (`http.server`). No `pip install` required!
- **Interactive Terminal Game**: Colored ANSI board and QWERTY keyboard with status tracking.
- **Identical Rules & Behavior**:
  - 607 five-letter dictionary loaded from `words.csv` (with built-in fallback).
  - 6 attempts per round.
  - Two-pass guess evaluation (green exact matches, orange wrong position, grey absent).
  - 5 hints per game (reveals unrevealed secret letter, highlights blue on keyboard, notifies if misplaced before).
  - Keyboard priority hierarchy: `grey < orange < blue < green`.
  - Independent game sessions for multiple players/browser tabs.
- **Automated Test Suite**: 15 unit and integration tests using Python's standard `unittest` module.

---

## 📋 Requirements

- **Python 3.8+** (tested up to Python 3.14)
- No external packages needed for the default server or CLI!

---

## 🚀 How to Run

### 1. Web Application (Recommended)

From the `wordle-python` folder:

```bash
# Using the helper script:
./run.sh

# Or directly with Python 3:
python3 server.py
```

Then open your browser to:
**<http://localhost:8080>**

*(To use a different port, pass `--port <number>`, e.g., `python3 server.py --port 8081`)*

### 2. Terminal / CLI Game

Play the classic terminal version directly in your console:

```bash
python3 wordle_cli.py
```

- Type any 5-letter word and press Enter.
- Type `HINT` during your turn to use one of your 5 hints.
- Type `RESET` to restart the current game.

### 3. Optional Flask Server

If you prefer running with Flask:

```bash
pip install flask
python3 app_flask.py
```

---

## 🧪 Running Automated Tests

Run the test suite with standard `unittest`:

```bash
python3 test_wordle.py
```

---

## 📁 File Structure

```text
wordle-python/
├── server.py          # Zero-dependency Python web server (API + Static files)
├── wordle_logic.py    # Core game rules, session state & dictionary
├── wordle_cli.py      # Terminal game with ANSI colors
├── test_wordle.py     # 15 automated test cases
├── run.sh             # Quick startup script
├── app_flask.py       # Alternative Flask server
├── requirements.txt   # Optional dependencies note
├── words.csv          # 607 five-letter word dictionary
└── static/            # Frontend assets (HTML, CSS, JS)
    ├── index.html
    ├── style.css
    └── app.js
```
