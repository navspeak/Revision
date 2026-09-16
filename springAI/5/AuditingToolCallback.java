package com.progress.pasoe.boot.ai;

import lombok.extern.slf4j.Slf4j;
import org.springframework.ai.chat.model.ToolContext;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.ai.tool.definition.ToolDefinition;
import org.springframework.ai.tool.metadata.ToolMetadata;

/**
 * Wraps a ToolCallback with logging/audit/guardrail behavior around every
 * invocation — logging what tool was called, with what input, how long
 * it took, and whether it succeeded, plus a basic input-size guardrail.
 *
 * This is the tool-call-layer equivalent of a Spring AI ChatClient
 * Advisor: same "wrap the call, run logic before/after" shape, but
 * operating on ToolCallback.call(...) instead of a chat request, since
 * this app has no ChatClient/LLM to attach a real Advisor to (see
 * McpToolsConfig for where these get applied).
 *
 * Extension points, if this grows beyond logging:
 *   - Swap the SLF4J logging in logStart/logResult/logFailure for a
 *     persisted audit trail (DB row per call) — this class is the one
 *     place that would change.
 *   - Add real guardrail logic in checkGuardrails(...) — e.g. blocking
 *     specific filterField/filterOp combinations, rate limiting per
 *     tool, rejecting inputs that look like injection attempts. Currently
 *     just an input-length check as a placeholder.
 */
@Slf4j
public class AuditingToolCallback implements ToolCallback {

    private final ToolCallback delegate;
    private final int maxInputLength;

    public AuditingToolCallback(ToolCallback delegate, int maxInputLength) {
        this.delegate = delegate;
        this.maxInputLength = maxInputLength;
    }

    @Override
    public ToolDefinition getToolDefinition() {
        return delegate.getToolDefinition();
    }

    @Override
    public ToolMetadata getToolMetadata() {
        return delegate.getToolMetadata();
    }

    @Override
    public String call(String toolInput) {
        return call(toolInput, null);
    }

    @Override
    public String call(String toolInput, ToolContext toolContext) {
        String toolName = delegate.getToolDefinition().name();

        String guardrailRejection = checkGuardrails(toolName, toolInput);
        if (guardrailRejection != null) {
            log.warn("Tool call BLOCKED: {} reason={}", toolName, guardrailRejection);
            return "Tool call blocked: " + guardrailRejection;
        }

        long start = System.nanoTime();
        log.info("Tool call START: {} input={}", toolName, truncate(toolInput));

        try {
            String result = (toolContext != null)
                    ? delegate.call(toolInput, toolContext)
                    : delegate.call(toolInput);
            long durationMs = (System.nanoTime() - start) / 1_000_000;
            log.info("Tool call OK: {} durationMs={} outputLength={}",
                    toolName, durationMs, result == null ? 0 : result.length());
            return result;
        } catch (RuntimeException e) {
            long durationMs = (System.nanoTime() - start) / 1_000_000;
            log.warn("Tool call FAILED: {} durationMs={} error={}", toolName, durationMs, e.toString());
            throw e;
        }
    }

    /**
     * Placeholder guardrail: rejects abnormally large input. Returns a
     * non-null rejection reason to block the call, or null to allow it.
     * Real guardrails (business-action gating, per-tool authorization,
     * etc.) would extend this method rather than living inline in
     * individual tools.
     */
    private String checkGuardrails(String toolName, String toolInput) {
        if (toolInput != null && toolInput.length() > maxInputLength) {
            return "input exceeds max length (" + toolInput.length() + " > " + maxInputLength + ")";
        }
        return null;
    }

    private static String truncate(String input) {
        if (input == null) return "null";
        return input.length() > 500 ? input.substring(0, 500) + "...(truncated)" : input;
    }
}
