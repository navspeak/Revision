package com.progress.pasoe.boot.ai.schema;

import java.util.List;

/**
 * Parsed representation of a single ADD TABLE block from an OpenEdge .df
 * data-definition file.
 */
public record OeTableSchema(
        String name,
        List<OeFieldSchema> fields,
        List<String> primaryKeyFields // from the first UNIQUE PRIMARY ADD INDEX block, if any
) {
    public record OeFieldSchema(
            String name,
            String dataType,   // e.g. character, integer, decimal, date, logical
            String format,     // OpenEdge display format, e.g. "x(30)", "->,>>>,>>9"
            String label,
            boolean mandatory,
            int extent          // 0 = scalar, >0 = array field
    ) {}
}
