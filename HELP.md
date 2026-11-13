# Wordle Application — Setup & Run Guide

A full-stack Wordle game featuring both a **Python 3 implementation** (standard library, zero external dependencies) and a **Java 17 / Spring Boot implementation**, paired with a responsive **HTML5, CSS3, and JavaScript** web frontend and an interactive **Terminal / CLI mode**.

---

## 🐍 Part 1: Running with Python (Recommended / Quickest)

The Python version runs on standard Python 3 with **zero third-party dependencies** required (no `pip install` needed).

### System Requirements
- **Python 3.8+** (check with `python3 --version`)
- Modern web browser (Chrome, Safari, Firefox, Edge)

---

### Option A: Python Web Application (Browser Game)

1. Open your terminal and navigate to the `wordle-python` directory:
   ```bash
   cd wordle-python
   ```
2. Start the Python web server:
   ```bash
   # Using the runner script:
   ./run.sh

   # Or running directly with python3:
   python3 server.py
   ```
   *(To use an alternate port: `python3 server.py --port 8081`)*

3. Open your browser and navigate to:
   **<http://localhost:8080>**

4. Press `Ctrl + C` in the terminal anytime to stop the server.

---

### Option B: Python Terminal / CLI Game (Console Game)

You can also play the classic Wordle game directly in your terminal with colored ANSI graphics:

```bash
cd wordle-python
python3 wordle_cli.py
```
- Type any 5-letter word and press **Enter** to submit your guess.
- Type `HINT` during your turn to reveal an unrevealed letter (up to 5 hints).
- Type `RESET` to restart the current game round.

---

### Option C: Running Python Automated Tests

The Python test suite mirrors the full Java test specification (15 unit and integration tests):

```bash
cd wordle-python
python3 test_wordle.py
```

---

## ☕ Part 2: Running with Java (Spring Boot)

### System Requirements
- **Java JDK 17 or higher** (`java -version`)
- Maven Wrapper is included (`mvnw` / `mvnw.cmd`), so Maven does not need to be pre-installed.

---

### How to Run the Java Backend

#### Method 1: Helper Script (macOS & Linux)
```bash
cd wordle-web
./run.sh
```
*(Automatically detects your JDK installation, exports `JAVA_HOME`, and launches Spring Boot).*

> If you get `Permission denied`, run: `chmod +x wordle-web/run.sh wordle-web/mvnw`

#### Method 2: Maven Wrapper (macOS & Linux)
```bash
cd wordle-web
./mvnw spring-boot:run
```

#### Method 3: Maven Wrapper (Windows)
```cmd
cd wordle-web
mvnw.cmd spring-boot:run
```
*(In PowerShell: `.\mvnw.cmd spring-boot:run`)*

#### Method 4: Build and Run Standalone JAR
```bash
cd wordle-web
./mvnw clean package
java -jar target/wordle-web-0.0.1-SNAPSHOT.jar
```

#### Running Java Automated Tests
```bash
cd wordle-web
./mvnw test
```

---

## 🎮 How to Play

1. Open your browser to **<http://localhost:8080>** (after starting either the Python or Java server).
2. **Rules & Objective**:
   - Guess the hidden 5-letter secret word in **6 attempts**.
   - Input words using your physical keyboard or the clickable on-screen keyboard.
3. **Color Codes**:
   - 🟩 **Green**: Correct letter in the correct position.
   - 🟧 **Orange / Yellow**: Correct letter, but in the wrong position.
   - ⬛ **Gray**: Letter does not exist in the secret word.
   - 🟦 **Blue**: Revealed hint letter on the keyboard.
4. **Hints**: Click **Hint** (up to 5 per round) to reveal an unrevealed letter in blue.
5. **New Game**: Click **Play Again** at any time to begin a fresh round.

---

## 🛠️ Troubleshooting & FAQs

### 1. `Port 8080 was already in use`
- **For Python**: Specify an alternate port when running:
  ```bash
  python3 server.py --port 8081
  ```
  Then visit `http://localhost:8081`.
- **For Java**: Pass the server port parameter:
  ```bash
  ./mvnw spring-boot:run -Dspring-boot.run.arguments=--server.port=8081
  ```
- **Or free port 8080**:
  - macOS/Linux: `lsof -i :8080` then `kill -9 <PID>`
  - Windows: `netstat -ano | findstr :8080` then `taskkill /PID <PID> /F`

### 2. Java: `The JAVA_HOME environment variable is not defined correctly`
- Use the **Python version** (`cd wordle-python && python3 server.py`), which has no JDK dependency!
- Or set `JAVA_HOME` on macOS:
  ```bash
  export JAVA_HOME=$(/usr/libexec/java_home -v 17)
  ```

### 3. `Permission denied` on shell scripts
```bash
chmod +x wordle-python/run.sh wordle-python/wordle_cli.py wordle-web/run.sh wordle-web/mvnw
```

---

## 📁 Repository Structure

```text
COMP_312_01E_F26_GP/
├── HELP.md                    # Root setup and run guide (this document)
├── wordle-python/             # Python Implementation (Standard Library)
│   ├── server.py              # Zero-dependency Python web server
│   ├── wordle_logic.py        # Core game rules, dictionary & session state
│   ├── wordle_cli.py          # Terminal game with ANSI colors
│   ├── test_wordle.py         # 15 automated test cases
│   ├── run.sh                 # Quick startup script
│   ├── app_flask.py           # Optional Flask alternative
│   ├── requirements.txt       # Optional dependencies
│   ├── words.csv              # 607 five-letter word dictionary
│   ├── README.md              # Python guide
│   └── static/                # Web frontend assets (HTML, CSS, JS)
│       ├── index.html
│       ├── style.css
│       └── app.js
└── wordle-web/                # Java 17 / Spring Boot Implementation
    ├── HELP.md                # Java setup guide
    ├── README.md              # Java project overview
    ├── pom.xml                # Maven configuration
    ├── run.sh                 # Java startup script
    ├── mvnw / mvnw.cmd        # Maven wrapper scripts
    ├── words.csv              # 607 five-letter word dictionary
    └── src/
        ├── main/java/...      # Spring Boot controller, service, models
        ├── main/resources/... # Application properties & static assets
        └── test/java/...      # JUnit 5 & Mockito test suite
```
