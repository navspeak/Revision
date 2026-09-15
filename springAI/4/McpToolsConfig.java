package com.progress.pasoe.boot.ai;

import com.progress.pasoe.boot.ai.policy.PolicySearchTools;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Registers every @Tool-annotated method on OeQueryTools and
 * PolicySearchTools as MCP tools. spring-ai-starter-mcp-server's
 * auto-configuration detects any ToolCallbackProvider bean in the
 * context and exposes its tools over the MCP transport (stdio, per
 * SETUP_NOTES.md) — this is that bean.
 *
 * No separate registration needed for ChatClient use, if that's ever
 * added later — the same ToolCallbackProvider bean works for both.
 */
@Configuration
public class McpToolsConfig {

    @Bean
    public ToolCallbackProvider aiTools(OeQueryTools oeQueryTools, PolicySearchTools policySearchTools) {
        return MethodToolCallbackProvider.builder()
                .toolObjects(oeQueryTools, policySearchTools)
                .build();
    }
}
