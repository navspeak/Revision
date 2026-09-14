package com.progress.pasoe.boot.ai.schema;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Parses an OpenEdge .df (data-definition) file into Map&lt;TableName, OeTableSchema&gt;.
 *
 * Understands the ADD TABLE / ADD FIELD / ADD INDEX block grammar used by
 * every OpenEdge .df dump, regardless of which database produced it — this
 * is deliberately NOT hardcoded to Sports2000. Point OeSchemaCatalog at
 * whichever .df matches whatever database the OE Web service is currently
 * connected to.
 *
 * Ignored on purpose (safe for read-only discovery): TABLE-TRIGGER blocks,
 * SEQUENCE blocks, LOB storage details (LOB-AREA/LOB-BYTES/...), non-primary
 * index detail beyond field order.
 */
public final class OeSchemaDefinitionParser {

    private static final Pattern BLOCK_START = Pattern.compile("^ADD (TABLE|FIELD|INDEX)\\b.*");
    private static final Pattern ADD_TABLE = Pattern.compile("^ADD TABLE \"([^\"]+)\"");
    private static final Pattern ADD_FIELD = Pattern.compile("^ADD FIELD \"([^\"]+)\" OF \"([^\"]+)\" AS (\\S+)");
    private static final Pattern ADD_INDEX = Pattern.compile("^ADD INDEX \"([^\"]+)\" ON \"([^\"]+)\"");
    private static final Pattern FORMAT = Pattern.compile("^FORMAT \"([^\"]*)\"");
    private static final Pattern LABEL = Pattern.compile("^LABEL \"([^\"]*)\"");
    private static final Pattern EXTENT = Pattern.compile("^EXTENT (\\d+)");
    private static final Pattern INDEX_FIELD = Pattern.compile("^INDEX-FIELD \"([^\"]+)\"");

    private OeSchemaDefinitionParser() {
    }

    public static Map<String, OeTableSchema> parse(Path dfFile) {
        try {
            return parse(Files.readAllLines(dfFile));
        } catch (IOException e) {
            throw new UncheckedIOException("Failed to read .df file: " + dfFile, e);
        }
    }

    public static Map<String, OeTableSchema> parse(List<String> lines) {
        List<List<String>> blocks = splitIntoBlocks(lines);

        Map<String, List<OeTableSchema.OeFieldSchema>> fieldsByTable = new LinkedHashMap<>();
        Map<String, List<String>> primaryKeyByTable = new LinkedHashMap<>();

        for (List<String> block : blocks) {
            String head = block.get(0);
            Matcher table = ADD_TABLE.matcher(head);
            Matcher field = ADD_FIELD.matcher(head);
            Matcher index = ADD_INDEX.matcher(head);

            if (table.matches()) {
                fieldsByTable.computeIfAbsent(table.group(1), k -> new ArrayList<>());
            } else if (field.matches()) {
                String fieldName = field.group(1);
                String tableName = field.group(2);
                String dataType = field.group(3);

                String format = null;
                String label = null;
                boolean mandatory = false;
                int extent = 0;
                for (String line : block.subList(1, block.size())) {
                    Matcher m;
                    if ((m = FORMAT.matcher(line)).matches()) {
                        format = m.group(1);
                    } else if ((m = LABEL.matcher(line)).matches()) {
                        label = m.group(1);
                    } else if ((m = EXTENT.matcher(line)).matches()) {
                        extent = Integer.parseInt(m.group(1));
                    } else if (line.equals("MANDATORY")) {
                        mandatory = true;
                    }
                }

                fieldsByTable
                        .computeIfAbsent(tableName, k -> new ArrayList<>())
                        .add(new OeTableSchema.OeFieldSchema(fieldName, dataType, format, label, mandatory, extent));
            } else if (index.matches()) {
                String tableName = index.group(2);
                boolean unique = false;
                boolean primary = false;
                List<String> indexFields = new ArrayList<>();
                for (String line : block) {
                    if (line.contains("UNIQUE")) unique = true;
                    if (line.contains("PRIMARY")) primary = true;
                    Matcher m = INDEX_FIELD.matcher(line);
                    if (m.find()) indexFields.add(m.group(1));
                }
                if (unique && primary && !indexFields.isEmpty()) {
                    primaryKeyByTable.put(tableName, indexFields);
                }
            }
        }

        Map<String, OeTableSchema> result = new LinkedHashMap<>();
        fieldsByTable.forEach((tableName, fields) -> result.put(tableName,
                new OeTableSchema(tableName, fields, primaryKeyByTable.getOrDefault(tableName, List.of()))));
        return result;
    }

    private static List<List<String>> splitIntoBlocks(List<String> lines) {
        List<List<String>> blocks = new ArrayList<>();
        List<String> current = null;
        for (String raw : lines) {
            String line = raw.trim();
            if (line.isEmpty() || line.equals(".")) continue;
            if (BLOCK_START.matcher(line).matches()) {
                if (current != null) blocks.add(current);
                current = new ArrayList<>();
                current.add(line);
            } else if (current != null) {
                current.add(line);
            }
        }
        if (current != null) blocks.add(current);
        return blocks;
    }
}
