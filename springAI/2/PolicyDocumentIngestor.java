package com.progress.pasoe.boot.ai.policy;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.ai.document.Document;
import org.springframework.ai.reader.TextReader;
import org.springframework.ai.transformer.splitter.TokenTextSplitter;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * Loads the demo policy document into the in-memory vector store once at
 * startup. Runs as an ApplicationRunner so it happens after the context
 * (including the ONNX embedding model) is fully wired, and before any
 * MCP tool call could arrive.
 *
 * Swap the classpath resource for whatever document(s) you actually want
 * to demo with — this is deliberately just one small file for now.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class PolicyDocumentIngestor implements ApplicationRunner {

    private final VectorStore policyVectorStore;

    @Value("classpath:policy/oe-support-policy.md")
    private Resource policyDocument;

    @Override
    public void run(ApplicationArguments args) {
        TextReader reader = new TextReader(policyDocument);
        reader.getCustomMetadata().put("source", "oe-support-policy.md");

        List<Document> rawDocs = reader.get();
        List<Document> chunks = new TokenTextSplitter().apply(rawDocs);

        policyVectorStore.add(chunks);
        log.info("Ingested {} policy chunks from {} into the in-memory vector store.",
                chunks.size(), policyDocument.getFilename());
    }
}
