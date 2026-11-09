# Wordle Web

A browser-based version of your Java Wordle-style game. The backend uses Java 17 and Spring Boot; the frontend uses HTML, CSS, and JavaScript.

## What's included

- Your original built-in five-letter dictionary (607 entries extracted from `WordleGame.java`)
- Six guesses per game
- Green = correct letter and position
- Orange = correct letter, different position
- Gray = letter not present
- Five blue hints per game
- Keyboard color priority: gray < orange < blue < green
- Browser keyboard and physical keyboard support
- Independent game sessions for different browser tabs/players
- New game / reset functionality

## Requirements

- Java 17 or newer
- Maven 3.6.3 or newer

The project is configured for Java 17, so it matches a Java 17 installation.

## How to Run

### Quickest way (Recommended):
Run the provided run script, which automatically detects your Java JDK and starts the server:
```bash
./run.sh
```

### Alternatively with Maven Wrapper:
```bash
./mvnw spring-boot:run
```

Once started, open your browser to:
**<http://localhost:8080>**

Stop the server anytime with `Control + C` in the terminal.

## API endpoints

- `POST /api/games` — create a new game
- `GET /api/games/{id}` — retrieve the current game state
- `POST /api/games/{id}/guesses` — submit `{"guess":"crane"}`
- `POST /api/games/{id}/hint` — use a hint
- `POST /api/games/{id}/reset` — start a fresh game

## Notes

- Game sessions are held in server memory. Restarting the server clears active games.
- There are no user accounts, database, or leaderboard yet; those can be added later.
- The original console-only `Scanner`, `System.out.println`, and ANSI terminal-color code have been replaced by HTTP endpoints and browser UI.
- The uploaded original program is preserved in `reference/WordleGame.java`.
