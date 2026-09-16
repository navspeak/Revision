package com.progress.pasoe.boot.ai.schema;

import com.progress.pasoe.boot.ai.AiProperties;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Collections;
import java.util.Map;
import java.util.Optional;

/**
 * Runtime-loaded schema catalog. Parses whichever .df file is configured
 * for the currently-connected OpenEdge database (oe.ai.schema.df-path,
 * via AiProperties), so table/column discovery works for any database
 * this deployment happens to be pointed at — Sports2000 today, a
 * different one tomorrow, no code changes required, just a different
 * property value.
 *
 * If oe.ai.schema.df-path is unset or unreadable, the catalog stays
 * empty and callers fall back to the live _file metaschema query — see
 * OeQueryTools.listAvailableTables().
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class OeSchemaCatalog {

    private final AiProperties aiProperties;

    private volatile Map<String, OeTableSchema> tables = Collections.emptyMap();

    @PostConstruct
    void load() {
        String dfPath = aiProperties.schema().dfPath();
        if (dfPath == null || dfPath.isBlank()) {
            log.info("oe.ai.schema.df-path not set — schema catalog empty, live _file discovery only.");
            return;
        }
        Path path = Path.of(dfPath);
        if (!Files.isReadable(path)) {
            log.warn("oe.ai.schema.df-path={} is not readable — schema catalog empty.", path);
            return;
        }
        try {
            this.tables = OeSchemaDefinitionParser.parse(Files.readAllLines(path));
            log.info("Loaded {} tables from {}", tables.size(), path);
        } catch (IOException e) {
            log.warn("Failed to parse {}: {}", path, e.getMessage());
        }
    }

    public boolean isLoaded() {
        return !tables.isEmpty();
    }

    public Map<String, OeTableSchema> allTables() {
        return tables;
    }

    public Optional<OeTableSchema> describe(String tableName) {
        return tables.entrySet().stream()
                .filter(e -> e.getKey().equalsIgnoreCase(tableName))
                .map(Map.Entry::getValue)
                .findFirst();
    }
}
