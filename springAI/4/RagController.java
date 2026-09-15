package com.progress.pasoe.boot.ai.policy;

import lombok.RequiredArgsConstructor;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * Debug/test endpoint for the policy vector store — lets you try
 * different topK values directly over HTTP without going through
 * Copilot each time. Separate from PolicySearchTools (the actual @Tool
 * the model calls): this returns structured JSON with per-passage scores
 * so you can SEE how relevance degrades as topK grows, rather than the
 * flat concatenated string the model gets.
 *
 * NOT part of the MCP surface — this is a plain REST controller, only
 * reachable when the app is running with the web server on (i.e. NOT
 * the "mcp" profile, which disables the web server entirely — see
 * application-mcp.yml). Use your normal `./gradlew bootRun` for this.
 */
@RestController
@RequestMapping("/rag")
@RequiredArgsConstructor
public class RagController {

    private final VectorStore policyVectorStore;

    @PostMapping("/search")
    public List<RagResult> search(@RequestBody RagSearchRequest request) {
        SearchRequest searchRequest = SearchRequest.builder()
                .query(request.query())
                .topK(request.topK() == null ? 3 : request.topK())
                .build();

        List<Document> results = policyVectorStore.similaritySearch(searchRequest);

        return results.stream()
                .map(d -> new RagResult(d.getText(), d.getScore()))
                .toList();
    }

    public record RagSearchRequest(String query, Integer topK) {}

    public record RagResult(String text, Double score) {}
}
