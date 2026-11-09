package com.wordle.model;

import java.util.List;
import java.util.Map;

public record GameView(
        String gameId,
        List<GuessResult> guesses,
        Map<String, String> keyboardStatus,
        int attemptsRemaining,
        int hintsLeft,
        boolean won,
        boolean gameOver,
        String message
) {
}
