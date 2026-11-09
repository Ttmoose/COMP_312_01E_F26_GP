package com.wordle.service;

import com.wordle.model.GuessResult;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class GameSession {
    final String id;
    String secretWord;
    final List<GuessResult> guesses = new ArrayList<>();
    final Map<String, String> keyboardStatus = new HashMap<>();
    int hintsLeft = 5;
    boolean won = false;
    boolean gameOver = false;
    String message = "Guess the five-letter word.";
    long lastAccessed = System.currentTimeMillis();

    GameSession(String id, String secretWord) {
        this.id = id;
        this.secretWord = secretWord;
    }

    void touch() {
        this.lastAccessed = System.currentTimeMillis();
    }
}
