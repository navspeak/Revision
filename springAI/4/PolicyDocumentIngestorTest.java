package com.progress.pasoe.boot.ai.policy;

import org.junit.jupiter.api.Test;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.core.io.ClassPathResource;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;

/**
 * Unit tests for the modular ingestion steps. loadDocument and
 * chunkDocuments need no embedding model and no Spring context — fast,
 * pure-logic tests. Only embedAndStore touches a (mocked) VectorStore.
 *
 * Complements PolicySearchToolsTest, which covers the full pipeline
 * end-to-end with the real ONNX embedding model.
 */
class PolicyDocumentIngestorTest {

    private final VectorStore vectorStore = mock(VectorStore.class);
    private final PolicyDocumentIngestor ingestor = new PolicyDocumentIngestor(vectorStore);

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
}
