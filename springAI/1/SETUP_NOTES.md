# Setup notes — iteration 2 (schema-aware query tools)

This file is meant to be regenerated/updated every iteration so you have one
place to copy build config and file locations from, without re-reading chat.

## 1. build.gradle additions

Dependencies needed so far (cumulative — includes iteration 1):

```groovy
dependencies {
    // --- Spring AI core ---
    implementation platform('org.springframework.ai:spring-ai-bom:2.0.1')
    implementation 'org.springframework.ai:spring-ai-starter-model-openai' // swap for -anthropic, -ollama, etc.

    // --- MCP server (stdio, for GitHub Copilot CLI / VS Code discovery) ---
    implementation 'org.springframework.ai:spring-ai-starter-mcp-server'

    // --- needed for OeQueryService's mock-request bridge (iteration 1) ---
    implementation 'org.springframework:spring-test' // NOT testImplementation — used in main code

    // --- test ---
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}

repositories {
    mavenCentral()
}
```

Notes:
- `spring-ai-bom:2.0.1` is the current GA and officially supports Spring Boot 4.0.x/4.1.x — no milestone/snapshot repos needed.
- **Is LangGraph a fit?** No — LangGraph is a Python/TypeScript library; there's no first-class Java port. For a Spring/Java stack, Spring AI's own `ChatClient` + `@Tool` + `Advisor` model *is* the agent framework — it covers tool-calling loops, RAG (via `QuestionAnswerAdvisor`), and memory without pulling in a second, foreign-language framework. Don't add LangGraph here.
- Stdio MCP: no extra property needed beyond adding `spring-ai-starter-mcp-server` — that starter defaults to stdio. (The `-webmvc`/`-webflux` starters are for HTTP/SSE instead, not needed for Copilot CLI stdio.)

## 2. application.yml additions

```yaml
oe:
  schema:
    # Path to the .df for whichever OpenEdge database this deployment is
    # currently pointed at. Optional — if unset, table discovery falls
    # back to a live _file query and column discovery falls back to the
    # model doing a small unfiltered read.
    df-path: ${OE_SCHEMA_DF_PATH:}

spring:
  ai:
    mcp:
      server:
        name: oe-query-server
        version: 1.0.0
        type: SYNC
```

## 3. Where files go

| File | Package / location |
|---|---|
| `OeTableSchema.java` | `com.progress.pasoe.boot.ai.schema` |
| `OeSchemaDefinitionParser.java` | `com.progress.pasoe.boot.ai.schema` |
| `OeSchemaCatalog.java` | `com.progress.pasoe.boot.ai.schema` |
| `OeQueryService.java` | `com.progress.pasoe.boot.ai` *(from iteration 1)* |
| `OeQueryTools.java` | `com.progress.pasoe.boot.ai` *(replaces iteration 1 version — now uses OeSchemaCatalog)* |
| `OeSchemaDefinitionParserTest.java` | `src/test/java/com/progress/pasoe/boot/ai/schema` |
| The actual `.df` file (e.g. `sports2000.df`) | Anywhere readable at runtime — e.g. `src/main/resources/schema/sports2000.df`, then set `OE_SCHEMA_DF_PATH` to its resolved filesystem path (a classpath resource inside a jar isn't a `Path`, so either point at a file on disk, or — if you want it packaged in the jar — say so and I'll switch the loader to read via `ClassPathResource` instead of `Files.readAllLines`). |

## 4. Where to get a Sports2000 `.df` for testing

Public copy for reference/testing: `sports2000.df` in
`consultingwerk/BigSports20000` on GitHub. Grab that (or export your own
copy via the Data Dictionary: **Admin > Dump Definitions... > Database
Definitions (.df)**) and point `OE_SCHEMA_DF_PATH` at it.

## 5. Still open from iteration 1

- Confirm `OeWebRouteResolver.resolve(...)` null-handling.
- Confirm the forwarder reads query params via `request.getParameter(...)` (vs. re-parsing `getQueryString()`).
