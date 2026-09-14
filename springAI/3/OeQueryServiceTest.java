package com.progress.pasoe.boot.web;

import com.progress.pasoe.boot.ai.OeQueryService;
import jakarta.servlet.http.HttpServletRequest;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.mock.web.MockHttpServletResponse;

import java.io.IOException;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

/**
 * Unit test for OeQueryService's bridge into the existing forward
 * pipeline — mocks both OeWebRequestForwarder and OeWebRouteResolver, so
 * this runs with NO live OpenEdge service. It verifies OeQueryService
 * builds the right request/params and handles the response correctly,
 * independent of whether Open4GlOeWebRequestForwarder or the AppServer
 * connection actually works.
 *
 * Lives in the same package as OeWebRouteResolver (com.progress.pasoe.boot.web)
 * because OeWebRequestTarget appears to be package-private — OeQueryService
 * itself never names the type, only passes it through opaquely (the only
 * way external-package code could use it). Being in-package sidesteps
 * that question entirely rather than guessing at its visibility.
 *
 * Confirmed from OeWebRouteResolver.java: resolve(...) never returns
 * null (it falls back to defaultHandlerClass), so the null-handling item
 * from SETUP_NOTES.md #5 is resolved — no defensive null-check needed in
 * OeQueryService.
 */
class OeQueryServiceTest {

    private final OeWebRequestForwarder forwarder = mock(OeWebRequestForwarder.class);
    private final OeWebRouteResolver routeResolver = mock(OeWebRouteResolver.class);
    private final OeQueryService oeQueryService = new OeQueryService(forwarder, routeResolver);

    @Test
    void resolvesRouteUsingPathAfterOePrefix() throws IOException {
        stubRouteResolverToReturnDefaultTarget();

        oeQueryService.query("Customer", null, null, null, null, 10);

        verify(routeResolver).resolve("/data/Customer");
    }

    @Test
    void leadingSlashOnTableNameIsNormalized() throws IOException {
        stubRouteResolverToReturnDefaultTarget();

        oeQueryService.query("/Customer", null, null, null, null, null);

        verify(routeResolver).resolve("/data/Customer");
    }

    @Test
    void buildsRequestWithGivenParametersAndCorrectUri() throws IOException {
        stubRouteResolverToReturnDefaultTarget();
        ArgumentCaptor<HttpServletRequest> requestCaptor = ArgumentCaptor.forClass(HttpServletRequest.class);

        oeQueryService.query("Customer", "CustNum,Name", "CustNum", "EQ", "4", 5);

        verify(forwarder).forward(requestCaptor.capture(), any(), any());
        HttpServletRequest captured = requestCaptor.getValue();

        assertThat(captured.getRequestURI()).isEqualTo("/oe/data/Customer");
        assertThat(captured.getParameter("columns")).isEqualTo("CustNum,Name");
        assertThat(captured.getParameter("filterField")).isEqualTo("CustNum");
        assertThat(captured.getParameter("filterOp")).isEqualTo("EQ");
        assertThat(captured.getParameter("filterValue")).isEqualTo("4");
        assertThat(captured.getParameter("limit")).isEqualTo("5");
    }

    @Test
    void omitsUnsetParametersEntirelyRatherThanSendingBlanks() throws IOException {
        stubRouteResolverToReturnDefaultTarget();
        ArgumentCaptor<HttpServletRequest> requestCaptor = ArgumentCaptor.forClass(HttpServletRequest.class);

        oeQueryService.query("Item", null, null, null, null, null);

        verify(forwarder).forward(requestCaptor.capture(), any(), any());
        HttpServletRequest captured = requestCaptor.getValue();

        assertThat(captured.getParameter("columns")).isNull();
        assertThat(captured.getParameter("filterField")).isNull();
        assertThat(captured.getParameter("filterOp")).isNull();
        assertThat(captured.getParameter("filterValue")).isNull();
        assertThat(captured.getParameter("limit")).isNull();
    }

    @Test
    void returnsResponseBodyOnSuccess() throws IOException {
        stubRouteResolverToReturnDefaultTarget();
        doAnswer(invocation -> {
            MockHttpServletResponse response = invocation.getArgument(1);
            response.setStatus(200);
            response.getWriter().write("[{\"CustNum\":4,\"Name\":\"Test Co\"}]");
            return null;
        }).when(forwarder).forward(any(), any(), any());

        String result = oeQueryService.query("Customer", "CustNum,Name", "CustNum", "EQ", "4", 5);

        assertThat(result).isEqualTo("[{\"CustNum\":4,\"Name\":\"Test Co\"}]");
    }

    @Test
    void returnsReadableErrorMessageOn400Plus() throws IOException {
        stubRouteResolverToReturnDefaultTarget();
        doAnswer(invocation -> {
            MockHttpServletResponse response = invocation.getArgument(1);
            response.setStatus(404);
            response.getWriter().write("Unknown table: Widgets");
            return null;
        }).when(forwarder).forward(any(), any(), any());

        String result = oeQueryService.query("Widgets", null, null, null, null, null);

        assertThat(result)
                .contains("HTTP 404")
                .contains("Widgets")
                .contains("Unknown table: Widgets");
    }

    private void stubRouteResolverToReturnDefaultTarget() {
        when(routeResolver.resolve(anyString()))
                .thenReturn(new OeWebRequestTarget("SomeHandler", Map.of()));
    }
}
