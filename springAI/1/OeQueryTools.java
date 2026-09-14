package com.progress.pasoe.boot.ai;

import com.progress.pasoe.boot.ai.schema.OeSchemaCatalog;
import com.progress.pasoe.boot.ai.schema.OeTableSchema;
import lombok.RequiredArgsConstructor;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.stream.Collectors;

/**
 * Tools exposed to the LLM (via ChatClient and the MCP server) for
 * discovering and querying OpenEdge tables through the existing OE Web
 * forwarding service. This is intentionally NOT SQL — it's a single-table
 * read with at most one comparison filter, matching the REST contract in
 * curl.txt (columns / filterField / filterOp / filterValue / limit).
 *
 * Discovery is two-tiered:
 *   1. If a .df was configured (oe.schema.df-path), table + column info
 *      comes from OeSchemaCatalog — fast, exact, works offline.
 *   2. Otherwise, table names come from the live _file metaschema query,
 *      and column names are learned by the model doing a small unfiltered
 *      read (limit=5) — see queryTable's tool description.
 */
@Component
@RequiredArgsConstructor
public class OeQueryTools {

    private final OeQueryService oeQueryService;
    private final OeSchemaCatalog schemaCatalog;

    @Tool(description = "Lists OpenEdge tables available to query. Call this first when you " +
            "don't already know the exact table name the user is asking about — table names " +
            "are case-sensitive and must match exactly (e.g. 'Customer', not 'customer').")
    public String listAvailableTables() {
        if (schemaCatalog.isLoaded()) {
            return String.join(", ", schemaCatalog.allTables().keySet());
        }
        try {
            // Bonus trick from curl.txt: the schema metadata table is just
            // another table, so the same generic read endpoint lists it.
            return oeQueryService.query("_file", "_file-name", null, null, null, 200);
        } catch (IOException e) {
            return "Error listing tables: " + e.getMessage();
        }
    }

    @Tool(description = "Describes a table's columns (name, data type, label, mandatory) from " +
            "the loaded schema definition, when available. Call this BEFORE queryTable whenever " +
            "you're not certain of a column name — guessing wrong wastes a round trip and can " +
            "return a 400. If this returns 'no schema loaded', fall back to calling queryTable " +
            "with no columns/filter and a small limit to inspect the shape instead.")
    public String describeTable(
            @ToolParam(description = "Exact OpenEdge table name, e.g. Customer, Order, Item.")
            String table) {
        if (!schemaCatalog.isLoaded()) {
            return "No schema loaded for '" + table + "' (no .df configured). " +
                    "Call queryTable with columns/filter omitted and limit=5 to inspect the shape instead.";
        }
        return schemaCatalog.describe(table)
                .map(this::render)
                .orElse("No table named '" + table + "' found in the loaded schema. " +
                        "Call listAvailableTables to see valid table names.");
    }

    @Tool(description = "Runs a filtered read against a single OpenEdge table via the OE Web " +
            "REST service. This is NOT SQL: it returns at most one table's rows, optionally " +
            "narrowed by ONE equality/comparison filter on ONE field. If you don't know the " +
            "table's column names yet, call describeTable first, or call this once with " +
            "columns and filter omitted and a small limit to inspect the shape before filtering.")
    public String queryTable(
            @ToolParam(description = "Exact OpenEdge table name, e.g. Customer, Order, Item, Salesrep.")
            String table,
            @ToolParam(description = "Comma-separated column names to return, e.g. 'CustNum,Name'. Omit for the table's default columns.", required = false)
            String columns,
            @ToolParam(description = "Column name to filter on, e.g. 'CustNum'. Omit for no filter.", required = false)
            String filterField,
            @ToolParam(description = "Filter operator supported by the service (e.g. EQ, GT, LT, GE, LE). Do not guess unsupported operators like LIKE.", required = false)
            String filterOp,
            @ToolParam(description = "Value to filter by. Must match the field's type — numeric fields need a numeric value, not quoted text.", required = false)
            String filterValue,
            @ToolParam(description = "Max rows to return. Keep this small (<=20) unless the user explicitly needs more; defaults to 10.", required = false)
            Integer limit) {
        try {
            return oeQueryService.query(table, columns, filterField, filterOp, filterValue,
                    limit == null ? 10 : limit);
        } catch (IOException e) {
            return "Query against '" + table + "' failed: " + e.getMessage();
        }
    }

    private String render(OeTableSchema schema) {
        String cols = schema.fields().stream()
                .map(f -> "  - " + f.name() + " (" + f.dataType() + ")"
                        + (f.label() != null ? " \"" + f.label() + "\"" : "")
                        + (f.mandatory() ? " [mandatory]" : "")
                        + (f.extent() > 0 ? " [array x" + f.extent() + "]" : ""))
                .collect(Collectors.joining("\n"));
        String pk = schema.primaryKeyFields().isEmpty()
                ? "unknown"
                : String.join(", ", schema.primaryKeyFields());
        return "Table " + schema.name() + " (primary key: " + pk + ")\n" + cols;
    }
}
