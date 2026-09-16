package com.progress.pasoe.boot.ai;

import com.progress.pasoe.boot.ai.policy.PolicySearchTools;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.Arrays;
import java.util.List;

/**
 * Registers every @Tool-annotated method on OeQueryTools and
 * PolicySearchTools as MCP tools. spring-ai-starter-mcp-server's
 * auto-configuration detects any ToolCallbackProvider bean in the
 * context and exposes its tools over the MCP transport (stdio, per
 * SETUP_NOTES.md) — this is that bean.
 *
 * Every callback is wrapped in AuditingToolCallback before being
 * exposed, so logging/audit/guardrails apply uniformly to every tool
 * call — the equivalent of a ChatClient Advisor, but at the tool
 * invocation layer, since there's no ChatClient/LLM in this app to hang
 * a real Advisor off of. See AuditingToolCallback for what it does and
 * where to extend it.
 *
 * No separate registration needed for ChatClient use, if that's ever
 * added later — the same ToolCallbackProvider bean works for both.
 */
@Configuration
public class McpToolsConfig {

    @Value("${oe.tools.audit.max-input-length:4000}")
    private int maxToolInputLength;

    @Bean
    public ToolCallbackProvider aiTools(OeQueryTools oeQueryTools, PolicySearchTools policySearchTools) {
        ToolCallbackProvider rawProvider = MethodToolCallbackProvider.builder()
                .toolObjects(oeQueryTools, policySearchTools)
                .build();

        List<ToolCallback> audited = Arrays.stream(rawProvider.getToolCallbacks())
                .<ToolCallback>map(callback -> new AuditingToolCallback(callback, maxToolInputLength))
                .toList();

        return ToolCallbackProvider.from(audited);
    }
}
