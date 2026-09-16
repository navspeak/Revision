package com.progress.pasoe.boot.ai.policy;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.ai.document.Document;
import org.springframework.ai.reader.TextReader;
import org.springframework.ai.transformer.splitter.TokenTextSplitter;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * Loads the policy document into the vector store at startup.
 *
 * Configurable document location: override oe.policy.document to point
 * anywhere Spring's Resource loader understands — a different classpath
 * resource, an external file (file:/path/to/doc.md), a URL, etc.
 * Defaults to the bundled demo doc so this works out of the box.
 *
 * Split into three independently-testable steps rather than one run()
 * method:
 *   - loadDocument: I/O only, no embedding model needed
 *   - chunkDocuments: pure logic over an in-memory list, no I/O, no
 *     embedding model needed — the one most worth unit testing in
 *     isolation since chunking behavior (chunk size, overlap) is the
 *     easiest thing to get subtly wrong
 *   - embedAndStore: the only step that actually needs the real
 *     embedding model / vector store wired up
 *
 * Package-private (not private) on purpose, so PolicyDocumentIngestorTest
 * can exercise each step directly without needing a full Spring context
 * or the ONNX model.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class PolicyDocumentIngestor implements CommandLineRunner {

    private final VectorStore policyVectorStore;

    @Value("${oe.policy.document:classpath:policy/oe-support-policy.md}")
    private Resource policyDocument;

    @Override
    public void run(String... args) {
        List<Document> rawDocs = loadDocument(policyDocument);
        List<Document> chunks = chunkDocuments(rawDocs);
        int stored = embedAndStore(chunks);

        log.info("Ingested {} policy chunks from {} into the vector store.",
                stored, describe(policyDocument));
    }

    List<Document> loadDocument(Resource resource) {
        TextReader reader = new TextReader(resource);
        reader.getCustomMetadata().put("source", describe(resource));
        return reader.get();
    }

    List<Document> chunkDocuments(List<Document> documents) {
        return TokenTextSplitter.builder().build().apply(documents);
    }

    int embedAndStore(List<Document> chunks) {
        policyVectorStore.add(chunks);
        return chunks.size();
    }

    private static String describe(Resource resource) {
        String filename = resource.getFilename();
        return filename != null ? filename : resource.getDescription();
    }
}
