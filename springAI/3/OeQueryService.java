package com.progress.pasoe.boot.ai;

import com.progress.pasoe.boot.web.OeWebRequestForwarder;
import com.progress.pasoe.boot.web.OeWebRouteResolver;
import lombok.RequiredArgsConstructor;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.util.UriComponentsBuilder;

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
 * CONFIRMED against live code (OeWebRouteResolver.java /
 * Open4GlOeWebRequestForwarder.java):
 *   1. resolve(String path) expects the path AFTER the "/oe" prefix,
 *      e.g. "/data/Customer" — confirmed, matches pathWithinOeMapping().
 *   2. resolve(...) never returns null (falls back to defaultHandlerClass)
 *      — no null-check needed.
 *   3. The forwarder reads the request via OeWebRequestEncoder.encode(request,
 *      pathVariables) to build the payload sent to the AppServer. The
 *      OeQueryServiceLiveIT run on 2026-09-14 showed a filtered query
 *      returning the SAME result size as an unfiltered one — i.e.
 *      setParameter(...) alone was NOT enough for the filter to take
 *      effect, which points at the encoder reading getQueryString()
 *      rather than (or in addition to) the parsed parameter map. Fixed
 *      below by setting both. Re-run OeQueryServiceLiveIT to confirm this
 *      resolves it; if it's still not narrowing, share
 *      OeWebRequestEncoder.java so this can be nailed down exactly rather
 *      than covering both possibilities defensively.
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
        String requestUri = "/oe" + routePath;

        Map<String, String> params = new LinkedHashMap<>();
        if (columns != null && !columns.isBlank()) params.put("columns", columns);
        if (filterField != null && !filterField.isBlank()) params.put("filterField", filterField);
        if (filterOp != null && !filterOp.isBlank()) params.put("filterOp", filterOp);
        if (filterValue != null && !filterValue.isBlank()) params.put("filterValue", filterValue);
        if (limit != null) params.put("limit", String.valueOf(limit));

        MockHttpServletRequest request = new MockHttpServletRequest("GET", requestUri);
        request.setContextPath("");
        params.forEach(request::setParameter);

        // Set the raw query string too — setParameter() alone populates the
        // parsed parameter map but does NOT synthesize a query string, so
        // any code reading request.getQueryString() directly would see
        // nothing without this.
        if (!params.isEmpty()) {
            UriComponentsBuilder uriBuilder = UriComponentsBuilder.newInstance();
            params.forEach(uriBuilder::queryParam);
            String queryString = uriBuilder.build().getQuery();
            request.setQueryString(queryString);
        }

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