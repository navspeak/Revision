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
 * *** THIS IS THE SWAP POINT ***
 * SimpleVectorStore is in-memory only: everything ingested is lost on
 * restart, and it's a linear-scan similarity search — fine for a demo
 * corpus, not for scale. To move to Chroma, Pinecone, pgvector, etc.:
 *   1. Add the corresponding spring-ai-starter-vector-store-* dependency
 *   2. Replace the method body below with that store's builder/bean
 * Nothing else changes — PolicyDocumentIngestor, PolicySearchTools, and
 * RagController all depend on the VectorStore interface only, never on
 * SimpleVectorStore directly, so they're unaffected by this swap.
 */
@Configuration
public class PolicyVectorStoreConfig {

    @Bean
    public VectorStore policyVectorStore(EmbeddingModel embeddingModel) {
        return SimpleVectorStore.builder(embeddingModel).build();
    }
}
