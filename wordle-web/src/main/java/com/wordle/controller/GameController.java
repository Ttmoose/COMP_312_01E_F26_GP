package com.wordle.controller;

import com.wordle.model.GameView;
import com.wordle.service.GameService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/api/games")
public class GameController {
    private final GameService gameService;

    public GameController(GameService gameService) {
        this.gameService = gameService;
    }

    @PostMapping
    public GameView newGame(@RequestBody(required = false) NewGameRequest request) {
        if (request != null && request.wordLength() != null) {
            int len = request.wordLength();
            if (len != 5 && len != 6 && len != 7) {
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Word length must be 5, 6, or 7.");
            }
            return gameService.newGame(len);
        }
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

    public record NewGameRequest(Integer wordLength) {
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
