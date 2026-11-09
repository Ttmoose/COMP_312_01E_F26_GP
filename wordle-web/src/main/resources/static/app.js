const rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];
let game = null;
let currentInput = "";

const board = document.getElementById("board");
const keyboard = document.getElementById("keyboard");
const message = document.getElementById("message");
const attempts = document.getElementById("attempts");
const hintsCount = document.getElementById("hints-count");
const hintButton = document.getElementById("hint-button");

function makeBoard() {
    board.innerHTML = "";
    for (let r = 0; r < 6; r++) {
        const row = document.createElement("div");
        row.className = "board-row";
        for (let c = 0; c < 5; c++) {
            const tile = document.createElement("div");
            tile.className = "tile";
            tile.id = `tile-${r}-${c}`;
            row.appendChild(tile);
        }
        board.appendChild(row);
    }
}

function makeKeyboard() {
    keyboard.innerHTML = "";
    rows.forEach((letters, index) => {
        const row = document.createElement("div");
        row.className = "key-row";
        if (index === 2) {
            row.appendChild(makeKey("ENTER", "wide", submitGuess));
        }
        [...letters].forEach(letter => row.appendChild(makeKey(letter, "", () => addLetter(letter))));
        if (index === 2) {
            row.appendChild(makeKey("⌫", "wide", removeLetter));
        }
        keyboard.appendChild(row);
    });
}

function makeKey(label, extraClass, action) {
    const button = document.createElement("button");
    button.className = `key ${extraClass}`;
    button.textContent = label;
    button.type = "button";
    button.addEventListener("click", action);
    if (label.length === 1 && /^[a-z]$/.test(label)) button.dataset.letter = label;
    return button;
}

function addLetter(letter) {
    if (!game || game.gameOver || currentInput.length >= 5) return;
    currentInput += letter;
    renderBoard();
}
function removeLetter() {
    if (!game || game.gameOver || currentInput.length === 0) return;
    currentInput = currentInput.slice(0, -1);
    renderBoard();
}

function renderBoard() {
    for (let r = 0; r < 6; r++) {
        for (let c = 0; c < 5; c++) {
            const tile = document.getElementById(`tile-${r}-${c}`);
            tile.className = "tile";
            tile.textContent = "";
        }
    }
    if (!game) return;

    game.guesses.forEach((guess, r) => {
        for (let c = 0; c < 5; c++) {
            const tile = document.getElementById(`tile-${r}-${c}`);
            tile.textContent = guess.guess[c].toUpperCase();
            tile.classList.add(guess.statuses[c]);
        }
    });

    const activeRow = game.guesses.length;
    if (!game.gameOver && activeRow < 6) {
        [...currentInput].forEach((letter, c) => {
            const tile = document.getElementById(`tile-${activeRow}-${c}`);
            tile.textContent = letter.toUpperCase();
            tile.classList.add("filled");
        });
    }
}

function renderKeyboard() {
    document.querySelectorAll(".key[data-letter]").forEach(key => {
        key.classList.remove("green", "orange", "blue", "grey");
        const status = game?.keyboardStatus?.[key.dataset.letter];
        if (status) key.classList.add(status);
    });
}

function renderGame() {
    renderBoard();
    renderKeyboard();
    attempts.textContent = game.attemptsRemaining;
    hintsCount.textContent = game.hintsLeft;
    document.getElementById("hint-cost").textContent = `${game.hintsLeft} left`;
    message.textContent = game.message;
    hintButton.disabled = game.gameOver || game.hintsLeft <= 0;
    document.getElementById("new-game-button").disabled = false;
}

async function api(path, options = {}) {
    const response = await fetch(path, {
        headers: { "Content-Type": "application/json" },
        ...options
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || "Something went wrong.");
    return data;
}

async function startNewGame() {
    try {
        game = await api("/api/games", { method: "POST" });
        currentInput = "";
        renderGame();
    } catch (error) {
        message.textContent = error.message;
    }
}

async function submitGuess() {
    if (!game || game.gameOver) return;
    if (currentInput.length !== 5) {
        message.textContent = "Enter a five-letter word first.";
        return;
    }
    try {
        const previousGuessCount = game.guesses.length;
        game = await api(`/api/games/${game.gameId}/guesses`, {
            method: "POST",
            body: JSON.stringify({ guess: currentInput })
        });
        if (game.guesses.length > previousGuessCount) currentInput = "";
        renderGame();
    } catch (error) {
        message.textContent = error.message;
    }
}

async function useHint() {
    if (!game || game.gameOver || game.hintsLeft <= 0) return;
    try {
        game = await api(`/api/games/${game.gameId}/hint`, { method: "POST" });
        renderGame();
    } catch (error) {
        message.textContent = error.message;
    }
}

document.addEventListener("keydown", event => {
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    if (event.key === "Enter") submitGuess();
    else if (event.key === "Backspace") removeLetter();
    else if (/^[a-zA-Z]$/.test(event.key)) addLetter(event.key.toLowerCase());
});

document.getElementById("new-game-button").addEventListener("click", startNewGame);
document.getElementById("new-game-top").addEventListener("click", startNewGame);
hintButton.addEventListener("click", useHint);

makeBoard();
makeKeyboard();
startNewGame();
