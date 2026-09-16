package com.progress.pasoe.boot.ai.policy;

import com.progress.pasoe.boot.ai.AiProperties;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.ai.document.Document;
import org.springframework.ai.reader.TextReader;
import org.springframework.ai.transformer.splitter.TokenTextSplitter;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * Loads the policy document into the vector store at startup.
 *
 * Configurable document location: oe.ai.rag.document-path (via
 * AiProperties) — override to point anywhere Spring's ResourceLoader
 * understands: a different classpath resource, an external file
 * (file:/path/to/doc.md), a URL, etc. Defaults to the bundled demo doc
 * so this works out of the box.
 *
 * Split into three independently-testable steps rather than one run()
 * method:
 *   - loadDocument: I/O only, no embedding model needed
 *   - chunkDocuments: pure logic over an in-memory list, no I/O, no
 *     embedding model needed
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
    private final AiProperties aiProperties;
    private final ResourceLoader resourceLoader;

    @Override
    public void run(String... args) {
        Resource policyDocument = resourceLoader.getResource(aiProperties.rag().documentPath());

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
