package com.progress.pasoe.boot.ai;

import com.progress.pasoe.boot.web.OeWebRequestForwarder;
import com.progress.pasoe.boot.web.OeWebRouteResolver;
import lombok.RequiredArgsConstructor;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * In-process bridge from Spring AI tool calls to the existing OE Web
 * forwarding pipeline (OeWebRequestForwarder / OeWebRouteResolver) —
 * deliberately NOT an inter-process HTTP call to localhost:8080/oe/data/...
 *
 * We build a lightweight mock servlet request carrying the same query
 * params OeWebController would receive, plus a response wrapper that
 * captures the body instead of writing to a real socket, and drive the
 * *exact same* forward(request, response, route) call the controller uses.
 *
 * ASSUMPTIONS — please confirm against your actual classes, I only had
 * visibility into OeWebController.java:
 *   1. OeWebRouteResolver.resolve(String path) expects the path AFTER the
 *      "/oe" prefix, e.g. "/data/Customer" — this mirrors
 *      OeWebController.pathWithinOeMapping(request).
 *   2. OeWebRequestForwarder reads columns/filterField/filterOp/filterValue
 *      /limit off the HttpServletRequest's parameters (request.getParameter),
 *      not by re-parsing a raw query string itself.
 *   3. The forwarder writes the OE response body to the HttpServletResponse's
 *      writer/output stream (which MockHttpServletResponse captures) rather
 *      than doing something servlet-container-specific (async dispatch,
 *      committing headers it expects to read back, etc).
 *
 * If any of these don't hold, share OeWebRequestForwarder.java and
 * OeWebRouteResolver.java and this will get adjusted.
 *
 * NOTE: MockHttpServletRequest/Response come from `org.springframework:spring-test`.
 * That's normally a test-only dependency — add it as a regular
 * `implementation` (not `testImplementation`) dependency in build.gradle
 * for this to compile in main source.
 */
@Service
@RequiredArgsConstructor
public class OeQueryService {

    private final OeWebRequestForwarder requestForwarder;
    private final OeWebRouteResolver routeResolver;

    /**
     * Runs a single-table filtered read through the existing OE forwarding
     * service and returns the raw response body (JSON, presumably) as a
     * String for the LLM to reason over.
     */
    public String query(String table, String columns, String filterField,
                         String filterOp, String filterValue, Integer limit) throws IOException {

        String tableSegment = "/" + table.replaceFirst("^/", "");
        String routePath = "/data" + tableSegment; // mirrors pathWithinOeMapping() output

        MockHttpServletRequest request = new MockHttpServletRequest("GET", "/oe" + routePath);
        request.setContextPath("");

        Map<String, String> params = new LinkedHashMap<>();
        if (columns != null && !columns.isBlank()) params.put("columns", columns);
        if (filterField != null && !filterField.isBlank()) params.put("filterField", filterField);
        if (filterOp != null && !filterOp.isBlank()) params.put("filterOp", filterOp);
        if (filterValue != null && !filterValue.isBlank()) params.put("filterValue", filterValue);
        if (limit != null) params.put("limit", String.valueOf(limit));
        params.forEach(request::setParameter);

        MockHttpServletResponse response = new MockHttpServletResponse();

        requestForwarder.forward(request, response, routeResolver.resolve(routePath));

        int status = response.getStatus();
        String body = response.getContentAsString();

        if (status >= 400) {
            String detail = (body == null || body.isBlank())
                    ? String.valueOf(response.getErrorMessage())
                    : body;
            return "HTTP " + status + " from OE service for table '" + table + "': " + detail;
        }
        return body;
    }
}
