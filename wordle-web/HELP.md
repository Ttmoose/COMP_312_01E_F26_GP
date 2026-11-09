# Wordle Web Application — Setup & Run Guide

A browser-based Wordle game built with a **Java 17 / Spring Boot** backend and a responsive **HTML5, CSS3, and JavaScript** frontend.

---

## 📋 System Requirements & Prerequisites

Before running the application, make sure you have:

1. **Java JDK 17 or higher** (Java 17, 21, etc.)
   - Check your installed version in the terminal:
     ```bash
     java -version
     ```
   - If not installed, download from [Adoptium / Eclipse Temurin](https://adoptium.net/) or [Oracle Java](https://www.oracle.com/java/technologies/downloads/).
2. **Maven**: *Optional*. A self-contained Maven Wrapper (`mvnw` / `mvnw.cmd`) is included in the project, so you do not need Maven pre-installed.
3. **Web Browser**: Any modern browser (Chrome, Firefox, Safari, Edge).

---

## 🚀 How to Run the Application

You can launch the application using any of the methods below. Choose the one that best fits your environment:

### Method 1: Helper Script (Recommended for macOS & Linux)

The repository provides a startup script (`run.sh`) that automatically locates your Java installation, sets `JAVA_HOME`, and boots the server:

```bash
# 1. From the repository root, change to the wordle-web directory:
cd wordle-web

# 2. Run the startup script:
./run.sh
```

*(Alternatively, run directly from the repository root: `./wordle-web/run.sh`)*

> **Note**: If you get a `Permission denied` error, grant execution permissions:
> ```bash
> chmod +x run.sh mvnw
> ```

---

### Method 2: Maven Wrapper (macOS & Linux)

If you prefer using the Maven Wrapper directly in your terminal:

```bash
cd wordle-web
./mvnw spring-boot:run
```

---

### Method 3: Maven Wrapper (Windows Command Prompt or PowerShell)

On Windows systems:

```cmd
cd wordle-web
mvnw.cmd spring-boot:run
```

Or in PowerShell:
```powershell
cd wordle-web
.\mvnw.cmd spring-boot:run
```

---

### Method 4: Using Locally Installed Maven (`mvn`)

If you have Apache Maven installed and configured in your `PATH`:

```bash
cd wordle-web
mvn spring-boot:run
```

---

### Method 5: Build and Run as a Standalone Executable JAR

To package the application into a standalone JAR file:

```bash
cd wordle-web

# Build and package (skipping tests is optional)
./mvnw clean package

# Run the packaged JAR
java -jar target/wordle-web-0.0.1-SNAPSHOT.jar
```
*(On Windows, replace `./mvnw` with `mvnw.cmd`)*

---

### Method 6: Running inside an IDE (IntelliJ IDEA, Eclipse, VS Code)

1. Open your IDE and import/open the `wordle-web` directory (or the repository root) as an existing **Maven** project.
2. Ensure your Project SDK is set to **Java 17 or higher**.
3. Navigate to:  
   `src/main/java/com/wordle/WordleWebApplication.java`
4. Run the `main` method (click the green "Play" icon or right-click `WordleWebApplication` -> **Run**).

---

## 🌐 Playing the Game

1. Once the application starts, open your web browser and navigate to:
   ```
   http://localhost:8080
   ```
2. **How to Play**:
   - **Goal**: Guess the hidden 5-letter word within **6 attempts**.
   - **Input**: Use either your physical keyboard or click the interactive on-screen keyboard.
   - **Color Feedback**:
     - 🟩 **Green**: Correct letter in the correct position.
     - 🟧 **Orange**: Correct letter, but in the wrong position.
     - ⬛ **Gray**: Letter does not exist in the target word.
     - 🟦 **Blue**: Revealed hint letter.
   - **Hints**: Click the **Hint** button (up to **5 hints per game**) to reveal a random remaining letter from the secret word.
   - **New Game**: Click the **Play Again** or **New Game** button at any time to start a fresh round.
3. **Stopping the Server**:
   - Press `Ctrl + C` in the terminal where the server is running.

---

## 🧪 Running Automated Tests

The project includes unit and integration tests covering game logic, hint generation, dictionary validation, and API endpoints.

To run the test suite:

```bash
cd wordle-web
./mvnw test
```
*(On Windows: `mvnw.cmd test`)*

---

## 🛠️ Troubleshooting & FAQs

### 1. `The JAVA_HOME environment variable is not defined correctly`
- Ensure Java 17+ is installed.
- **macOS**:
  ```bash
  export JAVA_HOME=$(/usr/libexec/java_home -v 17)
  # or if using Java 21:
  export JAVA_HOME=$(/usr/libexec/java_home -v 21)
  ```
- **Linux (Ubuntu/Debian)**:
  ```bash
  export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
  export PATH=$JAVA_HOME/bin:$PATH
  ```
- **Windows**:
  - Open **System Properties** > **Environment Variables**.
  - Add or update `JAVA_HOME` pointing to your JDK folder (e.g., `C:\Program Files\Eclipse Adoptium\jdk-17...`).
  - Add `%JAVA_HOME%\bin` to your `Path` variable.
- *Tip*: On macOS/Linux, running `./run.sh` attempts to auto-detect your JDK path automatically!

### 2. `Web server failed to start. Port 8080 was already in use`
Another application is already using port 8080. You can either:
- **Free port 8080**:
  - macOS/Linux:
    ```bash
    lsof -i :8080
    kill -9 <PID>
    ```
  - Windows:
    ```cmd
    netstat -ano | findstr :8080
    taskkill /PID <PID> /F
    ```
- **Or run on a different port** (e.g., port 8081):
  ```bash
  ./mvnw spring-boot:run -Dspring-boot.run.arguments=--server.port=8081
  ```
  Then access the application at `http://localhost:8081`.

### 3. `./run.sh: Permission denied` or `./mvnw: Permission denied`
Make the scripts executable with:
```bash
chmod +x run.sh mvnw
```

---

## 📁 Project Directory Structure

```text
COMP_312_01E_F26_GP/
└── wordle-web/
    ├── HELP.md                    # This setup and run guide
    ├── README.md                  # Project overview and features
    ├── pom.xml                    # Maven configuration and dependencies
    ├── run.sh                     # Helper startup script (macOS/Linux)
    ├── mvnw / mvnw.cmd            # Maven wrapper scripts
    ├── words.csv                  # 5-letter word dictionary
    ├── src/
    │   ├── main/
    │   │   ├── java/com/wordle/
    │   │   │   ├── WordleWebApplication.java  # Main Spring Boot entry point
    │   │   │   ├── controller/               # REST API endpoints
    │   │   │   ├── service/                  # Game state & business logic
    │   │   │   └── model/                    # Data transfer models
    │   │   └── resources/
    │   │       ├── application.properties    # Server settings
    │   │       ├── words.csv                 # Classpath word list
    │   │       └── static/                   # Frontend assets
    │   │           ├── index.html            # Web UI markup
    │   │           ├── style.css             # UI styling & animations
    │   │           └── app.js                # Game client logic
    │   └── test/                             # Automated test suite
    └── reference/
        └── WordleGame.java                   # Original reference console game
```

---

## 📚 Reference Documentation

For additional technical details on the underlying frameworks:
* [Official Apache Maven documentation](https://maven.apache.org/guides/index.html)
* [Spring Boot Maven Plugin Reference Guide](https://docs.spring.io/spring-boot/3.3.4/maven-plugin)
* [Spring Boot Reference Documentation](https://docs.spring.io/spring-boot/3.3.4/reference/index.html)
