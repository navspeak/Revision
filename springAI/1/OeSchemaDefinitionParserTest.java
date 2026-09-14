package com.progress.pasoe.boot.ai.schema;

import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * The .df parser is pure text-in/records-out logic — no OpenEdge server,
 * no network, nothing to stand up. This is the right thing to unit test
 * rather than demo live; the live-service pieces (OeQueryService,
 * OeQueryTools) are exercised against a real running service instead
 * (see TESTING_AND_DEMO.md).
 */
class OeSchemaDefinitionParserTest {

    // A trimmed-down but structurally real .df fragment: one table, two
    // scalar fields, one mandatory field, one primary unique index.
    private static final List<String> SAMPLE_DF = List.of(
            "ADD TABLE \"Customer\"",
            "  AREA \"Schema Area\"",
            "  DUMP-NAME \"customer\"",
            "",
            "ADD FIELD \"CustNum\" OF \"Customer\" AS integer",
            "  FORMAT \"->,>>>,>>9\"",
            "  INITIAL \"0\"",
            "  LABEL \"Cust Num\"",
            "  POSITION 2",
            "  MAX-WIDTH 4",
            "  ORDER 10",
            "  MANDATORY",
            "",
            "ADD FIELD \"Name\" OF \"Customer\" AS character",
            "  FORMAT \"x(30)\"",
            "  INITIAL \"\"",
            "  LABEL \"Name\"",
            "  POSITION 3",
            "  MAX-WIDTH 60",
            "  ORDER 20",
            "",
            "ADD INDEX \"CustNum\" ON \"Customer\"",
            "  AREA \"Schema Area\"",
            "  UNIQUE PRIMARY",
            "  INDEX-FIELD \"CustNum\" ASCENDING",
            "."
    );

    @Test
    void parsesTableAndFieldNames() {
        Map<String, OeTableSchema> result = OeSchemaDefinitionParser.parse(SAMPLE_DF);

        assertThat(result).containsKey("Customer");
        assertThat(result.get("Customer").fields())
                .extracting(OeTableSchema.OeFieldSchema::name)
                .containsExactly("CustNum", "Name");
    }

    @Test
    void parsesFieldDataTypeFormatAndLabel() {
        OeTableSchema.OeFieldSchema custNum = fieldNamed(result(), "CustNum");

        assertThat(custNum.dataType()).isEqualTo("integer");
        assertThat(custNum.format()).isEqualTo("->,>>>,>>9");
        assertThat(custNum.label()).isEqualTo("Cust Num");
    }

    @Test
    void parsesMandatoryFlagPerField() {
        OeTableSchema table = result().get("Customer");

        assertThat(fieldNamed(result(), "CustNum").mandatory()).isTrue();
        assertThat(fieldNamed(result(), "Name").mandatory()).isFalse();
    }

    @Test
    void parsesPrimaryKeyFromUniquePrimaryIndex() {
        OeTableSchema table = result().get("Customer");

        assertThat(table.primaryKeyFields()).containsExactly("CustNum");
    }

    @Test
    void tableWithNoDataIsEmptyMapNotException() {
        Map<String, OeTableSchema> result = OeSchemaDefinitionParser.parse(List.of());

        assertThat(result).isEmpty();
    }

    @Test
    void nonPrimaryIndexDoesNotSetPrimaryKey() {
        List<String> df = List.of(
                "ADD TABLE \"Item\"",
                "ADD FIELD \"ItemNum\" OF \"Item\" AS integer",
                "  FORMAT \">>>>9\"",
                "ADD INDEX \"ItemNumSecondary\" ON \"Item\"",
                "  INDEX-FIELD \"ItemNum\" ASCENDING",
                "."
        );

        Map<String, OeTableSchema> result = OeSchemaDefinitionParser.parse(df);

        assertThat(result.get("Item").primaryKeyFields()).isEmpty();
    }

    private static Map<String, OeTableSchema> result() {
        return OeSchemaDefinitionParser.parse(SAMPLE_DF);
    }

    private static OeTableSchema.OeFieldSchema fieldNamed(Map<String, OeTableSchema> result, String name) {
        return result.get("Customer").fields().stream()
                .filter(f -> f.name().equals(name))
                .findFirst()
                .orElseThrow();
    }
}
