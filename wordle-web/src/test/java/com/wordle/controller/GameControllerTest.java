package com.wordle.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class GameControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    @DisplayName("POST /api/games creates a new game session with 6 attempts")
    void testCreateNewGame() throws Exception {
        mockMvc.perform(post("/api/games"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.gameId").isNotEmpty())
                .andExpect(jsonPath("$.attemptsRemaining").value(6))
                .andExpect(jsonPath("$.hintsLeft").value(5))
                .andExpect(jsonPath("$.won").value(false))
                .andExpect(jsonPath("$.gameOver").value(false));
    }

    @Test
    @DisplayName("GET /api/games/{id} retrieves existing game session")
    void testGetGame() throws Exception {
        MvcResult created = mockMvc.perform(post("/api/games"))
                .andExpect(status().isOk())
                .andReturn();

        JsonNode root = objectMapper.readTree(created.getResponse().getContentAsString());
        String gameId = root.get("gameId").asText();

        mockMvc.perform(get("/api/games/" + gameId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.gameId").value(gameId))
                .andExpect(jsonPath("$.attemptsRemaining").value(6));
    }

    @Test
    @DisplayName("POST /api/games/{id}/guesses submits a valid guess and returns updated state")
    void testSubmitGuess() throws Exception {
        MvcResult created = mockMvc.perform(post("/api/games"))
                .andExpect(status().isOk())
                .andReturn();

        String gameId = objectMapper.readTree(created.getResponse().getContentAsString()).get("gameId").asText();

        mockMvc.perform(post("/api/games/" + gameId + "/guesses")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"guess\":\"crane\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.attemptsRemaining").value(5))
                .andExpect(jsonPath("$.guesses.length()").value(1))
                .andExpect(jsonPath("$.guesses[0].guess").value("crane"));
    }

    @Test
    @DisplayName("POST /api/games/{id}/hint deducts a hint and highlights a letter blue")
    void testUseHint() throws Exception {
        MvcResult created = mockMvc.perform(post("/api/games"))
                .andExpect(status().isOk())
                .andReturn();

        String gameId = objectMapper.readTree(created.getResponse().getContentAsString()).get("gameId").asText();

        mockMvc.perform(post("/api/games/" + gameId + "/hint"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.hintsLeft").value(4));
    }

    @Test
    @DisplayName("POST /api/games/{id}/reset resets the game state while preserving the same ID")
    void testResetGamePreservesId() throws Exception {
        MvcResult created = mockMvc.perform(post("/api/games"))
                .andExpect(status().isOk())
                .andReturn();

        String gameId = objectMapper.readTree(created.getResponse().getContentAsString()).get("gameId").asText();

        // Make a guess first
        mockMvc.perform(post("/api/games/" + gameId + "/guesses")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"guess\":\"beach\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.attemptsRemaining").value(5));

        // Now reset the game session
        mockMvc.perform(post("/api/games/" + gameId + "/reset"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.gameId").value(gameId))
                .andExpect(jsonPath("$.attemptsRemaining").value(6))
                .andExpect(jsonPath("$.hintsLeft").value(5))
                .andExpect(jsonPath("$.guesses").isEmpty());
    }

    @Test
    @DisplayName("GET /api/games/{id} returns 404 for unknown game ID")
    void testGetUnknownGameReturns404() throws Exception {
        mockMvc.perform(get("/api/games/non-existent-uuid-12345"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.message").isNotEmpty());
    }
}
