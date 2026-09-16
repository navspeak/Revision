package com.progress.pasoe.boot.ai;

import org.junit.jupiter.api.Test;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.ai.tool.definition.ToolDefinition;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class AuditingToolCallbackTest {

    private final ToolCallback delegate = mock(ToolCallback.class);
    private final ToolDefinition toolDefinition = mock(ToolDefinition.class);

    @Test
    void delegatesSuccessfulCallAndReturnsItsResult() {
        when(toolDefinition.name()).thenReturn("queryTable");
        when(delegate.getToolDefinition()).thenReturn(toolDefinition);
        when(delegate.call("input")).thenReturn("result");
        AuditingToolCallback auditing = new AuditingToolCallback(delegate, 4000);

        String result = auditing.call("input");

        assertThat(result).isEqualTo("result");
        verify(delegate).call("input");
    }

    @Test
    void propagatesExceptionFromDelegate() {
        when(toolDefinition.name()).thenReturn("queryTable");
        when(delegate.getToolDefinition()).thenReturn(toolDefinition);
        when(delegate.call("bad input")).thenThrow(new RuntimeException("boom"));
        AuditingToolCallback auditing = new AuditingToolCallback(delegate, 4000);

        assertThatThrownBy(() -> auditing.call("bad input"))
                .isInstanceOf(RuntimeException.class)
                .hasMessage("boom");
    }

    @Test
    void blocksOversizedInputWithoutCallingDelegate() {
        when(toolDefinition.name()).thenReturn("queryTable");
        when(delegate.getToolDefinition()).thenReturn(toolDefinition);
        AuditingToolCallback auditing = new AuditingToolCallback(delegate, 10);

        String result = auditing.call("this input is way over the ten char limit");

        assertThat(result).contains("blocked").contains("exceeds max length");
        verify(delegate, org.mockito.Mockito.never()).call(org.mockito.ArgumentMatchers.anyString());
    }

    @Test
    void toolDefinitionAndMetadataPassThroughUnchanged() {
        when(delegate.getToolDefinition()).thenReturn(toolDefinition);
        AuditingToolCallback auditing = new AuditingToolCallback(delegate, 4000);

        assertThat(auditing.getToolDefinition()).isSameAs(toolDefinition);
    }
}
