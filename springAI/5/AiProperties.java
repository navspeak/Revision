package com.progress.pasoe.boot.ai;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.bind.DefaultValue;

/**
 * Single source of configuration for the AI module, under one oe.ai
 * prefix — replaces the previous separate oe.schema.df-path and
 * oe.policy.document @Value fields.
 *
 * <pre>
 * oe:
 *   ai:
 *     schema:
 *       df-path: /path/to/sports2000.df       # empty/unset -> falls back to live _file discovery
 *     rag:
 *       document-path: classpath:policy/oe-support-policy.md
 * </pre>
 *
 * Registered via @EnableConfigurationProperties(AiProperties.class) on
 * McpToolsConfig — move that annotation elsewhere if the app already
 * uses @ConfigurationPropertiesScan.
 */
@ConfigurationProperties(prefix = "oe.ai")
public record AiProperties(Schema schema, Rag rag) {

    public record Schema(@DefaultValue("") String dfPath) {
    }

    public record Rag(@DefaultValue("classpath:policy/oe-support-policy.md") String documentPath) {
    }
}
