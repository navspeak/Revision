package com.progress.pasoe.boot.ai.policy;

import lombok.RequiredArgsConstructor;
import org.springframework.ai.document.Document;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Tool for answering policy/procedure questions (returns, discounts,
 * escalation, etc.) — distinct from OeQueryTools, which answers
 * data questions against live OpenEdge tables. The model is expected to
 * pick whichever tool fits the question; a question can need both
 * (e.g. "what's our return policy, and does customer 12 have any
 * recent orders that would qualify?").
 */
@Component
@RequiredArgsConstructor
public class PolicySearchTools {

    private final VectorStore policyVectorStore;

    @Tool(description = "Searches the company's internal policy document for procedural " +
            "questions — returns/refunds, order cancellation, discount authorization limits, " +
            "backorder handling, escalation procedures, expense approval, warehouse transfer " +
            "rules, and similar. Use this for 'what's the policy on...' / 'who approves...' / " +
            "'how do we handle...' questions. Do NOT use this for questions about specific " +
            "customer, order, or inventory data — use queryTable for that instead.")
    public String searchPolicy(
            @ToolParam(description = "The policy question or topic to search for, in plain language, e.g. 'discount approval over 20 percent' or 'return window for damaged items'.")
            String query,
            @ToolParam(description = "Max number of matching passages to return. Defaults to 3.", required = false)
            Integer topK) {

        SearchRequest request = SearchRequest.builder()
                .query(query)
                .topK(topK == null ? 3 : topK)
                .build();

        List<Document> results = policyVectorStore.similaritySearch(request);

        if (results == null || results.isEmpty()) {
            return "No matching policy passages found for: " + query;
        }

        return results.stream()
                .map(Document::getText)
                .collect(Collectors.joining("\n---\n"));
    }
}
