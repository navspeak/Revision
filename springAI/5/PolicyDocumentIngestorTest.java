package com.progress.pasoe.boot.ai.policy;

import com.progress.pasoe.boot.ai.AiProperties;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.DefaultResourceLoader;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

/**
 * Unit tests for the modular ingestion steps. loadDocument and
 * chunkDocuments need no embedding model and no Spring context — fast,
 * pure-logic tests. embedAndStore and run() touch a (mocked) VectorStore
 * only — no real embedding model needed, since the mock just records
 * what it was called with rather than actually embedding anything.
 *
 * Complements PolicySearchToolsTest, which covers the full pipeline
 * end-to-end with the real ONNX embedding model.
 */
class PolicyDocumentIngestorTest {

    private final VectorStore vectorStore = mock(VectorStore.class);

    // aiProperties/resourceLoader are null here: none of loadDocument,
    // chunkDocuments, or embedAndStore touch them — only run() does,
    // which gets its own instance with real values further down.
    private final PolicyDocumentIngestor ingestor = new PolicyDocumentIngestor(vectorStore, null, null);

    @Test
    void loadDocumentReadsClasspathResourceIntoDocuments() {
        List<Document> docs = ingestor.loadDocument(new ClassPathResource("policy/oe-support-policy.md"));

        assertThat(docs).isNotEmpty();
        assertThat(docs.get(0).getText()).contains("Order Cancellation");
    }

    @Test
    void chunkDocumentsSplitsLongTextIntoMultipleChunks() {
        Document longDoc = new Document("word ".repeat(2000));

        List<Document> chunks = ingestor.chunkDocuments(List.of(longDoc));

        assertThat(chunks.size()).isGreaterThan(1);
    }

    @Test
    void chunkDocumentsOnEmptyInputReturnsEmptyList() {
        List<Document> chunks = ingestor.chunkDocuments(List.of());

        assertThat(chunks).isEmpty();
    }

    @Test
    void embedAndStoreDelegatesToVectorStoreAndReturnsCount() {
        List<Document> chunks = List.of(new Document("a"), new Document("b"));

        int stored = ingestor.embedAndStore(chunks);

        assertThat(stored).isEqualTo(2);
        verify(vectorStore).add(chunks);
    }

    @Test
    void runIngestsEveryConfiguredDocumentPath() {
        // Same file listed twice, deliberately: this is testing that
        // run() LOOPS over documentPaths (calls vectorStore.add once per
        // path), not that the content differs between them.
        AiProperties properties = new AiProperties(
                new AiProperties.Schema(""),
                new AiProperties.Rag(List.of(
                        "classpath:policy/oe-support-policy.md",
                        "classpath:policy/oe-support-policy.md")));

        PolicyDocumentIngestor multiDocIngestor =
                new PolicyDocumentIngestor(vectorStore, properties, new DefaultResourceLoader());

        multiDocIngestor.run();

        @SuppressWarnings("unchecked")
        ArgumentCaptor<List<Document>> captor = ArgumentCaptor.forClass(List.class);
        verify(vectorStore, times(2)).add(captor.capture());

        assertThat(captor.getAllValues()).hasSize(2);
        assertThat(captor.getAllValues().get(0)).isNotEmpty();
        assertThat(captor.getAllValues().get(1)).isNotEmpty();
    }

    @Test
    void runWithSingleConfiguredPathCallsVectorStoreOnce() {
        AiProperties properties = new AiProperties(
                new AiProperties.Schema(""),
                new AiProperties.Rag(List.of("classpath:policy/oe-support-policy.md")));

        PolicyDocumentIngestor singleDocIngestor =
                new PolicyDocumentIngestor(vectorStore, properties, new DefaultResourceLoader());

        singleDocIngestor.run();

        verify(vectorStore, times(1)).add(org.mockito.ArgumentMatchers.anyList());
    }
}