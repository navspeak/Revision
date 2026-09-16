package com.progress.pasoe.boot.ai;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.bind.DefaultValue;

import java.util.List;

/**
 * Single source of configuration for the AI module, under one oe.ai
 * prefix.
 *
 * <pre>
 * oe:
 *   ai:
 *     schema:
 *       df-path: /path/to/sports2000.df       # empty/unset -> falls back to live _file discovery
 *     rag:
 *       document-paths:
 *         - classpath:policy/oe-support-policy.md
 *         - classpath:policy/another-doc.md    # add more as needed
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

    public record Rag(@DefaultValue("classpath:policy/oe-support-policy.md") List<String> documentPaths) {
    }
}