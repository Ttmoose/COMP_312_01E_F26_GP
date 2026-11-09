package com.wordle.model;

import java.util.List;

public record GuessResult(String guess, List<String> statuses) {
}
