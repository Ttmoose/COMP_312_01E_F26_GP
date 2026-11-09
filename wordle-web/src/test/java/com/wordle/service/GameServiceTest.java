package com.wordle.service;

import com.wordle.model.GameView;
import com.wordle.model.GuessResult;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class GameServiceTest {

    private GameService gameService;

    @BeforeEach
    void setUp() {
        gameService = new GameService();
    }

    @Test
    @DisplayName("New game initializes with 6 attempts, 5 hints, and empty board")
    void testGameInitialization() {
        GameView game = gameService.newGame();

        assertNotNull(game.gameId());
        assertEquals(6, game.attemptsRemaining());
        assertEquals(5, game.hintsLeft());
        assertTrue(game.guesses().isEmpty());
        assertTrue(game.keyboardStatus().isEmpty());
        assertFalse(game.won());
        assertFalse(game.gameOver());
    }

    @Test
    @DisplayName("Exact guess wins the game and colors all tiles green")
    void testExactGuessWinsGame() {
        GameView game = gameService.createGameWithSecret("apple");

        GameView result = gameService.submitGuess(game.gameId(), "apple");

        assertTrue(result.won());
        assertTrue(result.gameOver());
        assertEquals(5, result.attemptsRemaining());
        assertEquals(1, result.guesses().size());

        GuessResult guessResult = result.guesses().get(0);
        assertEquals("apple", guessResult.guess());
        assertEquals(List.of("green", "green", "green", "green", "green"), guessResult.statuses());

        assertEquals("green", result.keyboardStatus().get("a"));
        assertEquals("green", result.keyboardStatus().get("p"));
        assertEquals("green", result.keyboardStatus().get("l"));
        assertEquals("green", result.keyboardStatus().get("e"));
    }

    @Test
    @DisplayName("Partial matches evaluate green, orange, and grey correctly")
    void testPartialMatchesEvaluation() {
        // Target: CRANE
        // Guess:  BEACH -> B(grey), E(orange: crane has E at 4), A(green: match at 2), C(orange: crane has C at 0), H(grey)
        GameView game = gameService.createGameWithSecret("crane");

        GameView result = gameService.submitGuess(game.gameId(), "beach");

        assertFalse(result.won());
        assertFalse(result.gameOver());
        assertEquals(5, result.attemptsRemaining());

        List<String> statuses = result.guesses().get(0).statuses();
        assertEquals(List.of("grey", "orange", "green", "orange", "grey"), statuses);

        assertEquals("grey", result.keyboardStatus().get("b"));
        assertEquals("orange", result.keyboardStatus().get("e"));
        assertEquals("green", result.keyboardStatus().get("a"));
        assertEquals("orange", result.keyboardStatus().get("c"));
        assertEquals("grey", result.keyboardStatus().get("h"));
    }

    @Test
    @DisplayName("Duplicate letters algorithm masks used letters correctly (CRANE vs AGREE)")
    void testDuplicateLetterEvaluation() {
        // Target: CRANE (one C, one R, one A, one N, one E)
        // Guess:  AGREE (two E's: index 3 and index 4)
        // Both CRANE and AGREE are valid dictionary words.
        // Pass 1 (Green):  index 4 has 'E' -> GREEN (exact match with CRANE's E at index 4)
        // Pass 2 (Orange): index 0 has 'A' -> ORANGE (CRANE has A at index 2)
        //                  index 1 has 'G' -> GREY (no G in CRANE)
        //                  index 2 has 'R' -> ORANGE (CRANE has R at index 1)
        //                  index 3 has 'E' -> GREY (the only E in CRANE was already used by index 4!)
        GameView game = gameService.createGameWithSecret("crane");

        GameView result = gameService.submitGuess(game.gameId(), "agree");

        assertEquals(1, result.guesses().size());
        List<String> statuses = result.guesses().get(0).statuses();
        assertEquals("orange", statuses.get(0), "A should be orange");
        assertEquals("grey", statuses.get(1), "G should be grey");
        assertEquals("orange", statuses.get(2), "R should be orange");
        assertEquals("grey", statuses.get(3), "First E should be grey because CRANE only has one E and index 4 is green");
        assertEquals("green", statuses.get(4), "Second E should be green");
    }

    @Test
    @DisplayName("Keyboard color priority respects: grey < orange < blue < green")
    void testColorPriorityOnKeyboard() {
        GameView game = gameService.createGameWithSecret("crane");

        // 1. Guess "solid" (no C, R, A, N, E) -> all grey on keyboard
        gameService.submitGuess(game.gameId(), "solid");
        assertEquals("grey", gameService.getGame(game.gameId()).keyboardStatus().get("s"));

        // 2. Hint highlights an unrevealed letter blue
        GameView afterHint = gameService.useHint(game.gameId());
        assertEquals(4, afterHint.hintsLeft());

        // Find which letter was turned blue
        String blueLetter = afterHint.keyboardStatus().entrySet().stream()
                .filter(e -> "blue".equals(e.getValue()))
                .map(e -> e.getKey())
                .findFirst()
                .orElse(null);
        assertNotNull(blueLetter);

        // 3. Green overrides blue: guess the full word "crane"
        GameView afterWin = gameService.submitGuess(game.gameId(), "crane");
        assertEquals("green", afterWin.keyboardStatus().get(blueLetter));
    }

    @Test
    @DisplayName("Invalid guess length is rejected without consuming an attempt")
    void testInvalidGuessLengthRejected() {
        GameView game = gameService.newGame();

        GameView r1 = gameService.submitGuess(game.gameId(), "cat");
        assertEquals(6, r1.attemptsRemaining());
        assertTrue(r1.guesses().isEmpty());

        GameView r2 = gameService.submitGuess(game.gameId(), "banana");
        assertEquals(6, r2.attemptsRemaining());
        assertTrue(r2.guesses().isEmpty());
    }

    @Test
    @DisplayName("Word not in dictionary is rejected without consuming an attempt")
    void testWordNotInDictionaryRejected() {
        GameView game = gameService.newGame();

        GameView result = gameService.submitGuess(game.gameId(), "zzzzz");
        assertEquals(6, result.attemptsRemaining());
        assertTrue(result.guesses().isEmpty());
        assertTrue(result.message().toLowerCase().contains("not in"));
    }

    @Test
    @DisplayName("Consecutive hints reveal different letters without duplicating")
    void testDuplicateHintBugFix() {
        // Target: "orbit" (all 5 distinct letters: o, r, b, i, t)
        GameView game = gameService.createGameWithSecret("orbit");

        // 1st Hint
        GameView h1 = gameService.useHint(game.gameId());
        assertEquals(4, h1.hintsLeft());
        long blueCount1 = h1.keyboardStatus().values().stream().filter("blue"::equals).count();
        assertEquals(1, blueCount1, "First hint must highlight 1 letter blue");

        // 2nd Hint immediately (no guess made)
        GameView h2 = gameService.useHint(game.gameId());
        assertEquals(3, h2.hintsLeft());
        long blueCount2 = h2.keyboardStatus().values().stream().filter("blue"::equals).count();
        assertEquals(2, blueCount2, "Second hint must highlight a DIFFERENT letter blue");

        // 3rd Hint immediately
        GameView h3 = gameService.useHint(game.gameId());
        assertEquals(2, h3.hintsLeft());
        long blueCount3 = h3.keyboardStatus().values().stream().filter("blue"::equals).count();
        assertEquals(3, blueCount3, "Third hint must highlight another distinct letter blue");
    }

    @Test
    @DisplayName("Hints cannot be used when hintsLeft reaches 0")
    void testNoHintsRemaining() {
        GameView game = gameService.createGameWithSecret("orbit");

        for (int i = 0; i < 5; i++) {
            gameService.useHint(game.gameId());
        }

        GameView exhausted = gameService.getGame(game.gameId());
        assertEquals(0, exhausted.hintsLeft());

        GameView extraHint = gameService.useHint(game.gameId());
        assertEquals(0, extraHint.hintsLeft(), "Hints left cannot drop below 0");
        assertTrue(extraHint.message().toLowerCase().contains("no hints remaining"));
    }

    @Test
    @DisplayName("Game over occurs after 6 incorrect guesses")
    void testGameOverAfterSixFailedGuesses() {
        GameView game = gameService.createGameWithSecret("apple");

        String[] guesses = {"beach", "chair", "dance", "eagle", "faith", "grape"};
        GameView current = game;
        for (String g : guesses) {
            current = gameService.submitGuess(game.gameId(), g);
        }

        assertEquals(0, current.attemptsRemaining());
        assertEquals(6, current.guesses().size());
        assertTrue(current.gameOver());
        assertFalse(current.won());
        assertTrue(current.message().toLowerCase().contains("game over"));
        assertTrue(current.message().contains("APPLE"));
    }

    @Test
    @DisplayName("Submitting guess after game over is rejected")
    void testGuessAfterGameOverRejected() {
        GameView game = gameService.createGameWithSecret("apple");
        gameService.submitGuess(game.gameId(), "apple"); // won

        GameView extraGuess = gameService.submitGuess(game.gameId(), "beach");
        assertEquals(1, extraGuess.guesses().size());
        assertTrue(extraGuess.message().toLowerCase().contains("finished"));
    }

    @Test
    @DisplayName("resetGame preserves the game session ID and restores fresh state")
    void testResetGamePreservesSessionId() {
        GameView original = gameService.createGameWithSecret("apple");
        String originalId = original.gameId();

        gameService.submitGuess(originalId, "beach");
        gameService.useHint(originalId);

        GameView reset = gameService.resetGame(originalId);

        assertEquals(originalId, reset.gameId(), "Game ID must remain identical after reset");
        assertEquals(6, reset.attemptsRemaining());
        assertEquals(5, reset.hintsLeft());
        assertTrue(reset.guesses().isEmpty());
        assertTrue(reset.keyboardStatus().isEmpty());
        assertFalse(reset.won());
        assertFalse(reset.gameOver());
    }

    @Test
    @DisplayName("Dictionary loads 5-letter words from words.csv")
    void testDictionaryLoadedFromCsv() {
        Set<String> dictionary = gameService.getDictionary();
        assertNotNull(dictionary);
        assertTrue(dictionary.size() >= 600, "Dictionary should contain at least 600 words");

        for (String word : dictionary) {
            assertEquals(5, word.length(), "Each dictionary word must be exactly 5 letters");
            assertTrue(word.matches("[a-z]{5}"), "Each dictionary word must be lowercase alpha");
        }
    }
}
