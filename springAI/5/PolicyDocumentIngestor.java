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
 * Loads the configured document(s) into the vector store at startup.
 *
 * Configurable document locations: oe.ai.rag.document-paths (via
 * AiProperties) — a list, so multiple documents can be ingested. Each
 * entry can point anywhere Spring's ResourceLoader understands: a
 * classpath resource, an external file (file:/path/to/doc.md), a URL,
 * etc. Defaults to a single bundled demo doc so this works out of the
 * box with zero config.
 *
 * Split into three independently-testable steps rather than one run()
 * method:
 *   - loadDocument: I/O only, no embedding model needed
 *   - chunkDocuments: pure logic over an in-memory list, no I/O, no
 *     embedding model needed
 *   - embedAndStore: the only step that actually needs the real
 *     embedding model / vector store wired up
 * run() just loops these three over every configured path.
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
        List<String> paths = aiProperties.rag().documentPaths();
        int totalChunks = 0;

        for (String path : paths) {
            Resource resource = resourceLoader.getResource(path);

            List<Document> rawDocs = loadDocument(resource);
            List<Document> chunks = chunkDocuments(rawDocs);
            int stored = embedAndStore(chunks);
            totalChunks += stored;

            log.info("Ingested {} chunks from {} into the vector store.", stored, describe(resource));
        }

        log.info("Ingestion complete: {} total chunks from {} document(s).", totalChunks, paths.size());
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