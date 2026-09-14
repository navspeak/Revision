package com.progress.pasoe.boot.ai.policy;

import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.vectorstore.SimpleVectorStore;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * In-memory vector store for the policy-document RAG demo. The
 * EmbeddingModel bean here comes from spring-ai-starter-model-transformers
 * (a local ONNX model, e.g. all-MiniLM-L6-v2) — no API key, no outbound
 * calls at query time.
 *
 * SimpleVectorStore is in-memory only: everything ingested is lost on
 * restart, which is fine for this demo (ingestion happens at startup —
 * see PolicyDocumentIngestor). For anything beyond a demo, swap this for
 * a persistent VectorStore implementation (pgvector, etc.) — same
 * VectorStore interface, no changes needed in PolicySearchTools.
 */
@Configuration
public class PolicyVectorStoreConfig {

    @Bean
    public VectorStore policyVectorStore(EmbeddingModel embeddingModel) {
        return SimpleVectorStore.builder(embeddingModel).build();
    }
}
