package com.progress.pasoe.boot.ai.policy;

import org.junit.jupiter.api.Test;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Unlike OeQueryService/OeQueryTools (which need a live OE service),
 * this pipeline is fully offline — the embedding model is local ONNX, no
 * API key, no network at query time. So it's genuinely testable end to
 * end, not just as a parser-style unit test.
 *
 * NOTE: the ONNX model file is downloaded on first use (by
 * spring-ai-starter-model-transformers) and cached afterwards, so the
 * very first run of this test needs network access; subsequent runs
 * don't.
 *
 * Relies on PolicyDocumentIngestor having already run as an
 * ApplicationRunner during context startup — that's the real startup
 * path, not a test-only shortcut, so this also verifies ingestion works.
 */
@SpringBootTest
class PolicySearchToolsTest {

    @Autowired
    private VectorStore policyVectorStore;

    @Autowired
    private PolicySearchTools policySearchTools;

    @Test
    void ingestionPopulatesTheVectorStore() {
        List<Document> results = policyVectorStore.similaritySearch(
                SearchRequest.builder().query("return policy").topK(5).build());

        assertThat(results).isNotEmpty();
    }

    @Test
    void searchPolicyFindsReturnWindowForDamagedItems() {
        String result = policySearchTools.searchPolicy("return window for damaged items", 3);

        assertThat(result).containsIgnoringCase("90 days");
    }

    @Test
    void searchPolicyFindsDiscountApprovalThreshold() {
        String result = policySearchTools.searchPolicy("who approves a discount over 20 percent", 3);

        assertThat(result).containsIgnoringCase("Regional Director");
    }

    @Test
    void searchPolicyReturnsNoMatchMessageForOffTopicQuery() {
        // topK=1 + a query with no real semantic match to the demo doc —
        // still returns *something* since SimpleVectorStore always returns
        // its nearest neighbors, so this mainly checks the tool doesn't
        // throw rather than asserting true "no results" behavior.
        String result = policySearchTools.searchPolicy("quarterly revenue forecast for Mars colony", 1);

        assertThat(result).isNotBlank();
    }
}
