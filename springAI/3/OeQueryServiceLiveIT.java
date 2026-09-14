package com.progress.pasoe.boot.web;

import com.progress.pasoe.boot.ai.OeQueryService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.EnabledIfEnvironmentVariable;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Exercises OeQueryService against a REAL running OE connection — boots
 * the full Spring context, including the actual Open4GlOeWebRequestForwarder
 * and its AppServer connection, exactly as the running app would.
 *
 * Disabled by default (no live service assumed present in CI/normal
 * `./gradlew test` runs). Enable explicitly:
 *
 *   OE_LIVE_TEST=true ./gradlew test --tests "*OeQueryServiceLiveIT"
 *
 * Requires the app's normal OpenEdge connection properties to already be
 * configured (application.yml / env vars) exactly as they would be to
 * run the app itself, and Sports2000 (or whatever DB) reachable.
 */
@SpringBootTest
@EnabledIfEnvironmentVariable(named = "OE_LIVE_TEST", matches = "true")
class OeQueryServiceLiveIT {

    @Autowired
    private OeQueryService oeQueryService;

    @Test
    void unfilteredReadReturnsRealCustomerRows() throws Exception {
        String result = oeQueryService.query("Customer", "CustNum,Name", null, null, null, 5);

        assertThat(result).isNotBlank();
        assertThat(result).doesNotContain("HTTP 4").doesNotContain("HTTP 5");
    }

    @Test
    void filteredReadActuallyNarrowsResults() throws Exception {
        String unfiltered = oeQueryService.query("Customer", "CustNum", null, null, null, 50);
        String filtered = oeQueryService.query("Customer", "CustNum", "CustNum", "EQ", "4", 50);

        // Resolves open item #2 from SETUP_NOTES.md: if `filtered` still
        // comes back the same size as `unfiltered`, OeWebRequestEncoder
        // isn't reading the filter params the way OeQueryService assumes
        // (e.g. it re-parses getQueryString() instead of using
        // request.getParameter(...)), and the mock request needs
        // setQueryString(...) added too.
        assertThat(filtered.length()).isLessThan(unfiltered.length());
    }

    @Test
    void unknownTableReturnsCleanErrorNotAStackTrace() throws Exception {
        String result = oeQueryService.query("Widgets", null, null, null, null, null);

        assertThat(result).contains("HTTP 404").doesNotContain("Exception");
    }
}
