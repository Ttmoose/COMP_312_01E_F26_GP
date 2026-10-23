import java.util.*;

public class WordleGame {
    // Built-in 5-letter dictionary collection
    private static final Set<String> DICTIONARY = new HashSet<>(Arrays.asList(
        "apple", "beach", "chair", "dance", "eagle", "faith", "grape", "happy", "image", "juice",
        "knife", "lemon", "mouse", "night", "ocean", "peace", "queen", "river", "smile", "train",
        "urban", "voice", "water", "youth", "zebra", "blend", "crane", "drift", "ember",
        "frost", "glory", "hound", "input", "jolly", "kneel", "lurch", "maple", "noble", "orbit",
        "pearl", "quake", "rider", "scope", "twist", "ultra", "vigor", "waltz", "xenon", "yield",
        "about", "above", "actor", "admit", "adopt", "adult", "after", "again", "agent", "agree",
        "ahead", "alarm", "album", "alert", "alike", "alive", "allow", "alone", "along", "alter",
        "among", "anger", "angle", "angry", "apart", "apply", "arena", "argue", "arise",
        "armor", "array", "arrow", "aside", "asset", "audio", "audit", "avoid", "award", "aware",
        "badly", "baker", "bases", "basic", "basis", "began", "begin", "begun", "being",
        "below", "bench", "billy", "birth", "black", "blame", "blind", "block", "blood", "board",
        "boost", "booth", "bound", "brain", "brand", "bread", "break", "breed", "brief", "bring",
        "broad", "broke", "brown", "brush", "build", "built", "buyer", "cable", "canal",
        "candy", "canon", "cargo", "carry", "catch", "cause", "chain", "chart", "chase",
        "cheap", "check", "chest", "chief", "child", "china", "chose", "civil", "claim", "class",
        "clean", "clear", "click", "clock", "close", "coach", "coast", "could", "count", "court",
        "cover", "crack", "craft", "crash", "cream", "crime", "cross", "crowd", "crown", "curve",
        "cycle", "daily", "dated", "dealt", "death", "debut", "delay", "depth", "dirty",
        "doing", "doubt", "dozen", "draft", "drama", "drawn", "dream", "dress", "drill", "drink",
        "drive", "drove", "dying", "eager", "early", "earth", "eaten", "eight", "elite", "empty",
        "enemy", "enjoy", "enter", "entry", "equal", "error", "event", "every", "exact", "exist",
        "extra", "faint", "false", "fault", "favor", "feast", "fence", "fetch", "fiber",
        "field", "fifth", "fifty", "fight", "final", "first", "fixed", "flash", "fleet", "floor",
        "fluid", "focus", "force", "forth", "forty", "forum", "found", "frame", "frank", "fraud",
        "fresh", "front", "fruit", "fully", "funny", "giant", "given", "glass", "globe",
        "glove", "going", "grace", "grade", "grand", "grant", "grass", "grave", "great", "green",
        "gross", "group", "grown", "guard", "guess", "guest", "guide", "harry", "heart",
        "heavy", "hence", "henry", "horse", "hotel", "house", "human", "ideal", "index",
        "inner", "irony", "issue", "japan", "jimmy", "joint", "jones", "judge", "known", "label",
        "large", "laser", "later", "laugh", "layer", "learn", "lease", "least",
        "leave", "legal", "level", "lewis", "light", "limit", "links", "liver", "lives",
        "local", "lodge", "logic", "loose", "lower", "lucky", "lunch", "lying", "magic", "major",
        "maker", "march", "maria", "match", "maybe", "mayor", "meant", "media", "metal", "might",
        "minor", "minus", "mixed", "model", "money", "month", "moral", "motor", "mount",
        "mouth", "movie", "music", "naked", "nasty", "naval", "needs", "never", "newly",
        "noise", "north", "noted", "novel", "nurse", "occur", "offer", "often", "order",
        "other", "ought", "paint", "panel", "paper", "party", "pasta", "patch", "pause",
        "phase", "phone", "photo", "piece", "pilot", "pitch", "place", "plain", "plane", "plant",
        "plate", "point", "poker", "pound", "power", "press", "price", "pride", "prime", "print",
        "prior", "prize", "proof", "proud", "prove", "quick", "quiet", "quite", "radio",
        "raise", "range", "rapid", "ratio", "reach", "react", "ready", "realm", "rebel", "refer",
        "reign", "relax", "relay", "renal", "renew", "reply", "reset", "resin", "ridge",
        "right", "rigid", "ripen", "risen", "rival", "roast", "robin", "robot", "rocky",
        "roman", "rough", "round", "route", "royal", "ruler", "rural", "scale", "scene",
        "score", "sense", "serve", "seven", "shall", "shape", "share", "sharp", "sheet", "shelf",
        "shell", "shift", "shirt", "shock", "shoot", "short", "shown", "sight", "since", "sixth",
        "sixty", "sized", "skill", "sleep", "slide", "small", "smart", "smell", "smoke",
        "snake", "solid", "solve", "sorry", "sound", "south", "space", "spare", "speak", "speed",
        "spend", "spent", "split", "spoke", "sport", "staff", "stage", "stake", "stand", "start",
        "state", "steam", "steel", "steep", "steer", "stick", "stiff", "still", "stock", "stone",
        "stood", "store", "storm", "story", "strip", "stuck", "study", "stuff", "style", "sugar",
        "suite", "super", "sweet", "swift", "swing", "sword", "table", "taken", "taste", "taxes",
        "teach", "teeth", "teddy", "tears", "tempo", "tends", "tenth", "terms", "testy",
        "thank", "theft", "their", "theme", "there", "these", "thick", "thief", "third",
        "those", "three", "threw", "throw", "thumb", "tiger", "tight", "times", "tired", "title",
        "today", "token", "tooth", "topic", "total", "touch", "tough", "tower", "track", "trade",
        "treat", "trend", "trial", "tribe", "trick", "tried", "tries", "truck", "truly",
        "trunk", "trust", "truth", "twice", "under", "union", "unity", "until", "upper", "upset",
        "usage", "usual", "valid", "value", "vault", "video", "viral", "virus", "visit",
        "vital", "vivid", "vocal", "wagon", "waist", "waste", "watch", "weary",
        "weigh", "weird", "welsh", "whale", "wheat", "wheel", "where", "which", "while", "white",
        "whole", "whose", "widow", "width", "woman", "women", "world", "worry", "worse", "worst",
        "worth", "would", "wound", "woven", "wrist", "write", "wrong", "yacht", "yards", "years",
        "yeast", "young", "yours", "youth", "zones"
    ));

    // ANSI Escape Codes for console colors
    public static final String RESET = "\u001B[0m";
    public static final String GREEN_BG = "\u001B[42m";
    public static final String BLUE_BG = "\u001B[44m";
    public static final String ORANGE_BG = "\u001B[43m";
    public static final String GREY_BG = "\u001B[100m";
    public static final String BLACK_TEXT = "\u001B[30m";
    public static final String WHITE_TEXT = "\u001B[37m";

    private static String secretWord;
    private static List<String> guesses;
    private static List<String[]> guessStatuses;
    private static Map<Character, String> keyboardStatus; // green, blue, orange, grey
    private static int hintsLeft;

    // Priority map: Grey(1) < Orange(2) < Blue(3) < Green(4)
    private static final Map<String, Integer> COLOR_PRIORITY = Map.of(
        "grey", 1,
        "orange", 2,
        "blue", 3,
        "green", 4
    );

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        List<String> wordListAsList = new ArrayList<>(DICTIONARY);
        Random random = new Random();

        boolean playAgain = true;
        while (playAgain) {
            secretWord = wordListAsList.get(random.nextInt(wordListAsList.size()));
            guesses = new ArrayList<>();
            guessStatuses = new ArrayList<>();
            keyboardStatus = new HashMap<>();
            hintsLeft = 5;

            boolean won = false;

            System.out.println("\n==================================");
            System.out.println("       WELCOME TO JAVA WORDLE      ");
            System.out.println("==================================");
            System.out.println("Commands during your turn: Type a 5-letter word, type 'HINT', or 'RESET'.");

            while (guesses.size() < 6 && !won) {
                printBoard();
                printKeyboard();
                System.out.print("\nGuess #" + (guesses.size() + 1) + " (or type HINT/RESET): ");
                String input = scanner.nextLine().trim().toLowerCase();

                if (input.equals("reset")) {
                    System.out.println("🔄 Resetting game...");
                    break; // breaks current game loop to restart
                }

                if (input.equals("hint")) {
                    handleHint(scanner);
                    continue;
                }

                if (input.length() != 5) {
                    System.out.println("❌ Error: Guess must be exactly 5 letters.");
                    continue;
                }

                if (!DICTIONARY.contains(input)) {
                    System.out.println("❌ Error: Not in official word list.");
                    continue;
                }

                // Evaluate guess
                String[] status = evaluateGuess(input, secretWord);
                guesses.add(input);
                guessStatuses.add(status);

                // Update keyboard priorities
                for (int i = 0; i < 5; i++) {
                    updateKeyboardStatus(input.charAt(i), status[i]);
                }

                if (input.equals(secretWord)) {
                    won = true;
                }
            }

            printBoard();
            if (won) {
                System.out.println("🎉 GENIUS! You guessed the word correctly!");
            } else if (guesses.size() >= 6) {
                System.out.println("😢 Game Over! The secret word was: " + secretWord.toUpperCase());
            }

            System.out.print("\nWould you like to play a New Game? (y/n): ");
            String response = scanner.nextLine().trim().toLowerCase();
            if (!response.startsWith("y")) {
                playAgain = false;
                System.out.println("Thanks for playing!");
            }
        }
        scanner.close();
    }

    private static String[] evaluateGuess(String guess, String target) {
        String[] status = new String[5];
        Arrays.fill(status, "grey");
        char[] targetChars = target.toCharArray();

        // 1st Pass: Greens
        for (int i = 0; i < 5; i++) {
            if (guess.charAt(i) == targetChars[i]) {
                status[i] = "green";
                targetChars[i] = '_'; // mark used
            }
        }

        // 2nd Pass: Oranges
        for (int i = 0; i < 5; i++) {
            if (status[i].equals("green")) continue;
            char c = guess.charAt(i);
            boolean found = false;
            for (int j = 0; j < 5; j++) {
                if (targetChars[j] == c) {
                    found = true;
                    targetChars[j] = '_';
                    break;
                }
            }
            if (found) {
                status[i] = "orange";
            }
        }
        return status;
    }

    private static void updateKeyboardStatus(char letter, String newStatus) {
        String current = keyboardStatus.get(letter);
        if (current == null || COLOR_PRIORITY.get(newStatus) > COLOR_PRIORITY.get(current)) {
            keyboardStatus.put(letter, newStatus);
        }
    }

    private static void handleHint(Scanner scanner) {
        if (hintsLeft <= 0) {
            System.out.println("❌ No hints remaining!");
            return;
        }

        // Find an unrevealed correct letter
        Character targetLetter = null;
        for (int i = 0; i < 5; i++) {
            char letter = secretWord.charAt(i);
            boolean alreadySolved = false;
            for (int r = 0; r < guesses.size(); r++) {
                if (guesses.get(r).charAt(i) == letter && guessStatuses.get(r)[i].equals("green")) {
                    alreadySolved = true;
                    break;
                }
            }
            if (!alreadySolved) {
                targetLetter = letter;
                break;
            }
        }

        if (targetLetter == null) {
            System.out.println("✨ All letters have already been revealed!");
            return;
        }

        hintsLeft--;
        updateKeyboardStatus(targetLetter, "blue");
        System.out.println("💡 Hint used! " + hintsLeft + " hints remaining.");
        System.out.println("🔵 Letter '" + Character.toUpperCase(targetLetter) + "' highlighted in BLUE on keyboard.");

        // Check if letter was previously played in a wrong location
        boolean playedWrongLoc = false;
        for (String g : guesses) {
            if (g.indexOf(targetLetter) != -1) {
                playedWrongLoc = true;
                break;
            }
        }

        if (playedWrongLoc) {
            System.out.println("👉 Since '" + Character.toUpperCase(targetLetter) + "' was played in the wrong location before, it is suggested for your next guess!");
        }
    }

    private static void printBoard() {
        System.out.println("\n--- GAME BOARD ---");
        for (int r = 0; r < 6; r++) {
            StringBuilder sb = new StringBuilder("| ");
            for (int c = 0; c < 5; c++) {
                if (r < guesses.size()) {
                    char letter = guesses.get(r).charAt(c);
                    String status = guessStatuses.get(r)[c];
                    sb.append(formatColoredChar(letter, status)).append(" | ");
                } else {
                    sb.append("   | ");
                }
            }
            System.out.println(sb.toString());
        }
    }

    private static String formatColoredChar(char c, String status) {
        String uppercase = String.valueOf(c).toUpperCase();
        switch (status) {
            - case "green": return GREEN_BG + BLACK_TEXT + " " + uppercase + " " + RESET;
            - case "orange": return ORANGE_BG + BLACK_TEXT + " " + uppercase + " " + RESET;
            - case "blue": return BLUE_BG + WHITE_TEXT + " " + uppercase + " " + RESET;
            default: return GREY_BG + WHITE_TEXT + " " + uppercase + " " + RESET;
        }
    }

    private static void printKeyboard() {
        System.out.println("\nVirtual Keyboard (Grey < Orange < Blue < Green):");
        char[][] rows = {
            {'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'},
            {'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'},
            {'z', 'x', 'c', 'v', 'b', 'n', 'm'}
        };

        for (char[] row : rows) {
            StringBuilder sb = new StringBuilder();
            for (char key : row) {
                String status = keyboardStatus.get(key);
                String formattedKey = " " + Character.toUpperCase(key) + " ";
                if (status != null) {
                    switch (status) {
                        case "green": sb.append(GREEN_BG).append(BLACK_TEXT).append(formattedKey).append(RESET).append(" "); break;
                        case "blue": sb.append(BLUE_BG).append(WHITE_TEXT).append(formattedKey).append(RESET).append(" "); break;
                        case "orange": sb.append(ORANGE_BG).append(BLACK_TEXT).append(formattedKey).append(RESET).append(" "); break;
                        case "grey": sb.append(GREY_BG).append(WHITE_TEXT).append(formattedKey).append(RESET).append(" "); break;
                    }
                } else {
                    sb.append("\u001B[47m").append(BLACK_TEXT).append(formattedKey).append(RESET).append(" ");
                }
            }
            System.out.println(sb.toString());
        }
    }
}