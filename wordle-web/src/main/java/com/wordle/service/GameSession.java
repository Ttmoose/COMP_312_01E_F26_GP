package com.wordle.service;

import com.wordle.model.GuessResult;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class GameSession {
    final String id;
    final int wordLength;
    String secretWord;
    final List<GuessResult> guesses = new ArrayList<>();
    final Map<String, String> keyboardStatus = new HashMap<>();
    int hintsLeft = 5;
    boolean won = false;
    boolean gameOver = false;
    String message;
    long lastAccessed = System.currentTimeMillis();

    GameSession(String id, String secretWord) {
        this.id = id;
        this.secretWord = secretWord;
        this.wordLength = secretWord.length();
        this.message = "Guess the " + this.wordLength + "-letter word.";
    }

    void touch() {
        this.lastAccessed = System.currentTimeMillis();
    }
}
