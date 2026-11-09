package com.wordle.service;

import com.wordle.model.GameView;
import com.wordle.model.GuessResult;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class GameService {

    // Fallback five-letter dictionary from WordleGame.java.
    private static final Set<String> FALLBACK_DICTIONARY = new HashSet<>(List.of(
            "apple", "beach", "chair", "dance", "eagle", "faith", "grape", "happy", "image", "juice",
            "knife", "lemon", "mouse", "night", "ocean", "peace", "queen", "river", "smile", "train",
            "urban", "voice", "water", "youth", "zebra", "blend", "crane", "drift", "ember", "frost",
            "glory", "hound", "input", "jolly", "kneel", "lurch", "maple", "noble", "orbit", "pearl",
            "quake", "rider", "scope", "twist", "ultra", "vigor", "waltz", "xenon", "yield", "about",
            "above", "actor", "admit", "adopt", "adult", "after", "again", "agent", "agree", "ahead",
            "alarm", "album", "alert", "alike", "alive", "allow", "alone", "along", "alter", "among",
            "anger", "angle", "angry", "apart", "apply", "arena", "argue", "arise", "armor", "array",
            "arrow", "aside", "asset", "audio", "audit", "avoid", "award", "aware", "badly", "baker",
            "bases", "basic", "basis", "began", "begin", "begun", "being", "below", "bench", "billy",
            "birth", "black", "blame", "blind", "block", "blood", "board", "boost", "booth", "bound",
            "brain", "brand", "bread", "break", "breed", "brief", "bring", "broad", "broke", "brown",
            "brush", "build", "built", "buyer", "cable", "canal", "candy", "canon", "cargo", "carry",
            "catch", "cause", "chain", "chart", "chase", "cheap", "check", "chest", "chief", "child",
            "china", "chose", "civil", "claim", "class", "clean", "clear", "click", "clock", "close",
            "coach", "coast", "could", "count", "court", "cover", "crack", "craft", "crash", "cream",
            "crime", "cross", "crowd", "crown", "curve", "cycle", "daily", "dated", "dealt", "death",
            "debut", "delay", "depth", "dirty", "doing", "doubt", "dozen", "draft", "drama", "drawn",
            "dream", "dress", "drill", "drink", "drive", "drove", "dying", "eager", "early", "earth",
            "eaten", "eight", "elite", "empty", "enemy", "enjoy", "enter", "entry", "equal", "error",
            "event", "every", "exact", "exist", "extra", "faint", "false", "fault", "favor", "feast",
            "fence", "fetch", "fiber", "field", "fifth", "fifty", "fight", "final", "first", "fixed",
            "flash", "fleet", "floor", "fluid", "focus", "force", "forth", "forty", "forum", "found",
            "frame", "frank", "fraud", "fresh", "front", "fruit", "fully", "funny", "giant", "given",
            "glass", "globe", "glove", "going", "grace", "grade", "grand", "grant", "grass", "grave",
            "great", "green", "gross", "group", "grown", "guard", "guess", "guest", "guide", "harry",
            "heart", "heavy", "hence", "henry", "horse", "hotel", "house", "human", "ideal", "index",
            "inner", "irony", "issue", "japan", "jimmy", "joint", "jones", "judge", "known", "label",
            "large", "laser", "later", "laugh", "layer", "learn", "lease", "least", "leave", "legal",
            "level", "lewis", "light", "limit", "links", "liver", "lives", "local", "lodge", "logic",
            "loose", "lower", "lucky", "lunch", "lying", "magic", "major", "maker", "march", "maria",
            "match", "maybe", "mayor", "meant", "media", "metal", "might", "minor", "minus", "mixed",
            "model", "money", "month", "moral", "motor", "mount", "mouth", "movie", "music", "naked",
            "nasty", "naval", "needs", "never", "newly", "noise", "north", "noted", "novel", "nurse",
            "occur", "offer", "often", "order", "other", "ought", "paint", "panel", "paper", "party",
            "pasta", "patch", "pause", "phase", "phone", "photo", "piece", "pilot", "pitch", "place",
            "plain", "plane", "plant", "plate", "point", "poker", "pound", "power", "press", "price",
            "pride", "prime", "print", "prior", "prize", "proof", "proud", "prove", "quick", "quiet",
            "quite", "radio", "raise", "range", "rapid", "ratio", "reach", "react", "ready", "realm",
            "rebel", "refer", "reign", "relax", "relay", "renal", "renew", "reply", "reset", "resin",
            "ridge", "right", "rigid", "ripen", "risen", "rival", "roast", "robin", "robot", "rocky",
            "roman", "rough", "round", "route", "royal", "ruler", "rural", "scale", "scene", "score",
            "sense", "serve", "seven", "shall", "shape", "share", "sharp", "sheet", "shelf", "shell",
            "shift", "shirt", "shock", "shoot", "short", "shown", "sight", "since", "sixth", "sixty",
            "sized", "skill", "sleep", "slide", "small", "smart", "smell", "smoke", "snake", "solid",
            "solve", "sorry", "sound", "south", "space", "spare", "speak", "speed", "spend", "spent",
            "split", "spoke", "sport", "staff", "stage", "stake", "stand", "start", "state", "steam",
            "steel", "steep", "steer", "stick", "stiff", "still", "stock", "stone", "stood", "store",
            "storm", "story", "strip", "stuck", "study", "stuff", "style", "sugar", "suite", "super",
            "sweet", "swift", "swing", "sword", "table", "taken", "taste", "taxes", "teach", "teeth",
            "teddy", "tears", "tempo", "tends", "tenth", "terms", "testy", "thank", "theft", "their",
            "theme", "there", "these", "thick", "thief", "third", "those", "three", "threw", "throw",
            "thumb", "tiger", "tight", "times", "tired", "title", "today", "token", "tooth", "topic",
            "total", "touch", "tough", "tower", "track", "trade", "treat", "trend", "trial", "tribe",
            "trick", "tried", "tries", "truck", "truly", "trunk", "trust", "truth", "twice", "under",
            "union", "unity", "until", "upper", "upset", "usage", "usual", "valid", "value", "vault",
            "video", "viral", "virus", "visit", "vital", "vivid", "vocal", "wagon", "waist", "waste",
            "watch", "weary", "weigh", "weird", "welsh", "whale", "wheat", "wheel", "where", "which",
            "while", "white", "whole", "whose", "widow", "width", "woman", "women", "world", "worry",
            "worse", "worst", "worth", "would", "wound", "woven", "wrist", "write", "wrong", "yacht",
            "yards", "years", "yeast", "young", "yours", "youth", "zones"
    ));

    private final Set<String> dictionary;
    private final List<String> wordList;

    // Each browser game receives its own independent game session.
    private final Map<String, GameSession> games = new ConcurrentHashMap<>();

    public GameService() {
        Set<String> loaded = loadWordsFromCsv();
        if (loaded != null && !loaded.isEmpty()) {
            this.dictionary = loaded;
        } else {
            this.dictionary = FALLBACK_DICTIONARY;
        }
        this.wordList = new ArrayList<>(this.dictionary);
    }

    private static Set<String> loadWordsFromCsv() {
        // 1. Try classpath resource: words.csv
        try (InputStream is = GameService.class.getClassLoader().getResourceAsStream("words.csv")) {
            if (is != null) {
                Set<String> words = parseWords(new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8)));
                if (!words.isEmpty()) {
                    return words;
                }
            }
        } catch (Exception ignored) {
        }

        // 2. Try file system relative paths
        String[] candidatePaths = {
            "words.csv",
            "reference/words.csv",
            "src/main/resources/words.csv",
            "../words.csv"
        };
        for (String path : candidatePaths) {
            File file = new File(path);
            if (file.exists() && file.isFile()) {
                try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                    Set<String> words = parseWords(reader);
                    if (!words.isEmpty()) {
                        return words;
                    }
                } catch (IOException ignored) {
                }
            }
        }
        return null;
    }

    private static Set<String> parseWords(BufferedReader reader) throws IOException {
        Set<String> words = new HashSet<>();
        String line;
        while ((line = reader.readLine()) != null) {
            String[] tokens = line.split(",");
            for (String token : tokens) {
                String clean = token.replaceAll("[^a-zA-Z]", "").trim().toLowerCase();
                if (clean.length() == 5 && !clean.equalsIgnoreCase("words")) {
                    words.add(clean);
                }
            }
        }
        return words;
    }

    public GameView newGame() {
        evictOldSessionsIfNeeded();
        String id = UUID.randomUUID().toString();
        String secret = wordList.get((int) (Math.random() * wordList.size()));
        GameSession game = new GameSession(id, secret);
        games.put(id, game);
        return toView(game);
    }

    /**
     * Package-private helper used by unit tests to initialize a deterministic game session.
     */
    GameView createGameWithSecret(String secret) {
        evictOldSessionsIfNeeded();
        String id = UUID.randomUUID().toString();
        GameSession game = new GameSession(id, secret.toLowerCase());
        games.put(id, game);
        return toView(game);
    }

    public GameView resetGame(String id) {
        GameSession game = findGame(id);
        synchronized (game) {
            game.secretWord = wordList.get((int) (Math.random() * wordList.size()));
            game.guesses.clear();
            game.keyboardStatus.clear();
            game.hintsLeft = 5;
            game.won = false;
            game.gameOver = false;
            game.message = "Game reset. Guess the new five-letter word.";
            game.touch();
            return toView(game);
        }
    }

    private void evictOldSessionsIfNeeded() {
        if (games.size() > 500) {
            long twoHoursAgo = System.currentTimeMillis() - (2 * 3600 * 1000);
            games.entrySet().removeIf(entry -> entry.getValue().lastAccessed < twoHoursAgo);
        }
    }

    public Set<String> getDictionary() {
        return Set.copyOf(dictionary);
    }

    public GameView getGame(String id) {
        return toView(findGame(id));
    }

    public GameView submitGuess(String id, String rawGuess) {
        GameSession game = findGame(id);
        synchronized (game) {
            if (game.gameOver) {
                game.message = "This game is finished. Start a new game to play again.";
                return toView(game);
            }

            String guess = rawGuess == null ? "" : rawGuess.trim().toLowerCase();

            if (guess.length() != 5 || !guess.matches("[a-z]{5}")) {
                game.message = "Your guess must be exactly five letters.";
                return toView(game);
            }

            if (!dictionary.contains(guess)) {
                game.message = "That word is not in the game's dictionary.";
                return toView(game);
            }

            List<String> statuses = evaluateGuess(guess, game.secretWord);
            game.guesses.add(new GuessResult(guess, statuses));

            for (int i = 0; i < 5; i++) {
                updateKeyboardStatus(game, guess.charAt(i), statuses.get(i));
            }

            if (guess.equals(game.secretWord)) {
                game.won = true;
                game.gameOver = true;
                game.message = "Genius! You guessed the word!";
            } else if (game.guesses.size() >= 6) {
                game.gameOver = true;
                game.message = "Game over! The word was " + game.secretWord.toUpperCase() + ".";
            } else {
                game.message = "Good guess. Keep going!";
            }

            return toView(game);
        }
    }

    public GameView useHint(String id) {
        GameSession game = findGame(id);
        synchronized (game) {
            if (game.gameOver) {
                game.message = "This game is finished. Start a new game to play again.";
                return toView(game);
            }
            if (game.hintsLeft <= 0) {
                game.message = "You have no hints remaining.";
                return toView(game);
            }

            Character targetLetter = null;
            for (int i = 0; i < 5; i++) {
                char letter = game.secretWord.charAt(i);
                boolean alreadySolved = false;
                for (GuessResult result : game.guesses) {
                    if (result.guess().charAt(i) == letter
                            && result.statuses().get(i).equals("green")) {
                        alreadySolved = true;
                        break;
                    }
                }
                String kbd = game.keyboardStatus.get(Character.toString(letter));
                boolean alreadyHinted = "blue".equals(kbd) || "green".equals(kbd);
                if (!alreadySolved && !alreadyHinted) {
                    targetLetter = letter;
                    break;
                }
            }

            if (targetLetter == null) {
                game.message = "All letters in the secret word have already been revealed or hinted!";
                return toView(game);
            }

            game.hintsLeft--;
            updateKeyboardStatus(game, targetLetter, "blue");

            boolean playedWrongLocation = false;
            for (GuessResult result : game.guesses) {
                if (result.guess().indexOf(targetLetter) >= 0) {
                    playedWrongLocation = true;
                    break;
                }
            }

            String letter = Character.toString(targetLetter).toUpperCase();
            game.message = "Hint used: " + letter + " is highlighted blue on the keyboard."
                    + (playedWrongLocation ? " Consider trying it in a different position." : "");
            return toView(game);
        }
    }

    private List<String> evaluateGuess(String guess, String target) {
        String[] statuses = new String[5];
        Arrays.fill(statuses, "grey");
        char[] targetChars = target.toCharArray();

        // First pass: exact matches (green).
        for (int i = 0; i < 5; i++) {
            if (guess.charAt(i) == targetChars[i]) {
                statuses[i] = "green";
                targetChars[i] = '_';
            }
        }

        // Second pass: letters present in another position (orange).
        for (int i = 0; i < 5; i++) {
            if (statuses[i].equals("green")) {
                continue;
            }
            char c = guess.charAt(i);
            for (int j = 0; j < 5; j++) {
                if (targetChars[j] == c) {
                    statuses[i] = "orange";
                    targetChars[j] = '_';
                    break;
                }
            }
        }
        return List.of(statuses);
    }

    private void updateKeyboardStatus(GameSession game, char letter, String newStatus) {
        Map<String, Integer> priority = Map.of(
                "grey", 1, "orange", 2, "blue", 3, "green", 4
        );
        String key = Character.toString(letter);
        String current = game.keyboardStatus.get(key);
        if (current == null || priority.get(newStatus) > priority.get(current)) {
            game.keyboardStatus.put(key, newStatus);
        }
    }

    private GameSession findGame(String id) {
        GameSession game = games.get(id);
        if (game == null) {
            throw new IllegalArgumentException("Game not found. Start a new game.");
        }
        game.touch();
        return game;
    }

    private GameView toView(GameSession game) {
        return new GameView(
                game.id,
                List.copyOf(game.guesses),
                Map.copyOf(game.keyboardStatus),
                6 - game.guesses.size(),
                game.hintsLeft,
                game.won,
                game.gameOver,
                game.message
        );
    }
}
