package com.wordle.controller;

import com.wordle.model.GameView;
import com.wordle.service.GameService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/games")
public class GameController {
    private final GameService gameService;

    public GameController(GameService gameService) {
        this.gameService = gameService;
    }

    @PostMapping
    public GameView newGame() {
        return gameService.newGame();
    }

    @GetMapping("/{id}")
    public GameView getGame(@PathVariable String id) {
        return gameService.getGame(id);
    }

    @PostMapping("/{id}/guesses")
    public GameView submitGuess(@PathVariable String id, @RequestBody GuessRequest request) {
        return gameService.submitGuess(id, request.guess());
    }

    @PostMapping("/{id}/hint")
    public GameView useHint(@PathVariable String id) {
        return gameService.useHint(id);
    }

    @PostMapping("/{id}/reset")
    public GameView reset(@PathVariable String id) {
        return gameService.resetGame(id);
    }

    public record GuessRequest(String guess) {
    }

    @ExceptionHandler(IllegalArgumentException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(IllegalArgumentException exception) {
        return new ErrorResponse(exception.getMessage());
    }

    public record ErrorResponse(String message) {
    }
}
