const rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];
let game = null;
let currentInput = "";
let selectedDifficulty = "medium";
let selectedWordLength = 5;

const board = document.getElementById("board");
const keyboard = document.getElementById("keyboard");
const message = document.getElementById("message");
const attempts = document.getElementById("attempts");
const hintsCount = document.getElementById("hints-count");
const hintButton = document.getElementById("hint-button");
const gameSubtitle = document.getElementById("game-subtitle");

function makeBoard() {
    board.innerHTML = "";
    board.className = `board len-${game.wordLength}`;
    for (let r = 0; r < game.maxAttempts; r++) {
        const row = document.createElement("div");
        row.className = "board-row";
        for (let c = 0; c < game.wordLength; c++) {
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
    if (!game || game.gameOver || currentInput.length >= game.wordLength) return;
    currentInput += letter;
    renderBoard();
}
function removeLetter() {
    if (!game || game.gameOver || currentInput.length === 0) return;
    currentInput = currentInput.slice(0, -1);
    renderBoard();
}

function renderBoard() {
    if (!game) return;

    for (let r = 0; r < game.maxAttempts; r++) {
    for (let c = 0; c < game.wordLength; c++) {
            const tile = document.getElementById(`tile-${r}-${c}`);
            tile.className = "tile";
            tile.textContent = "";
        }
    }
    

    game.guesses.forEach((guess, r) => {
        for (let c = 0; c < game.wordLength; c++) {
            const tile = document.getElementById(`tile-${r}-${c}`);
            tile.textContent = guess.guess[c].toUpperCase();
            tile.classList.add(guess.statuses[c]);
        }
    });

    const activeRow = game.guesses.length;
    if (!game.gameOver && activeRow < game.maxAttempts) {
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

function updateControlStates() {
    document.querySelectorAll(".difficulty button[data-difficulty]").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.difficulty === selectedDifficulty);
    });
    document.querySelectorAll(".word-length button[data-length]").forEach(btn => {
        btn.classList.toggle("active", Number(btn.dataset.length) === selectedWordLength);
    });
}

function renderGame() {
    renderBoard();
    renderKeyboard();
    updateControlStates();
    attempts.textContent = game.attemptsRemaining;
    hintsCount.textContent = game.hintsLeft;
    document.getElementById("hint-cost").textContent = `${game.hintsLeft} left`;
    if (gameSubtitle) {
        gameSubtitle.textContent = `Find the hidden ${game.wordLength}-letter word in ${game.maxAttempts} tries.`;
    }
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

async function startNewGame(difficulty = selectedDifficulty, wordLength = selectedWordLength) {
    selectedDifficulty = difficulty;
    selectedWordLength = wordLength;
    try {
        game = await api("/api/games", {
            method: "POST",
            body: JSON.stringify({ difficulty: selectedDifficulty, wordLength: selectedWordLength })
        });
        currentInput = "";
        makeBoard();
        renderGame();
    } catch (error) {
        message.textContent = error.message;
    }
}

async function submitGuess() {
    if (!game || game.gameOver) return;
        if (currentInput.length !== game.wordLength) {
        message.textContent = "Enter a " + game.wordLength + "-letter word first.";
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
    if (event.key === "Enter") {
        event.preventDefault();
        submitGuess();
    } else if (event.key === "Backspace") {
        event.preventDefault();
        removeLetter();
    } else if (/^[a-zA-Z]$/.test(event.key)) {
        addLetter(event.key.toLowerCase());
    }
});

document.getElementById("new-game-button").addEventListener("click", e => {
    e.currentTarget.blur();
    startNewGame(selectedDifficulty, selectedWordLength);
});

document.getElementById("new-game-top").addEventListener("click", e => {
    e.currentTarget.blur();
    startNewGame(selectedDifficulty, selectedWordLength);
});
hintButton.addEventListener("click", e => {
    e.currentTarget.blur();
    useHint();
});
document.getElementById("easy").addEventListener("click", e => {
    e.currentTarget.blur();
    startNewGame("easy", selectedWordLength);
});

document.getElementById("medium").addEventListener("click", e => {
    e.currentTarget.blur();
    startNewGame("medium", selectedWordLength);
});

document.getElementById("hard").addEventListener("click", e => {
    e.currentTarget.blur();
    startNewGame("hard", selectedWordLength);
});

document.querySelectorAll(".word-length button[data-length]").forEach(btn => {
    btn.addEventListener("click", e => {
        e.currentTarget.blur();
        startNewGame(selectedDifficulty, Number(btn.dataset.length));
    });
});

makeKeyboard();
startNewGame();
