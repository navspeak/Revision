# Setup notes — iteration 2 (schema-aware query tools)

Copy-paste additions only, assuming you already have a working Gradle
project with `io.spring.dependency-management` (like your Initializr
export) — not a full build.gradle replacement.

## 1. build.gradle — check/add these

**a) If `spring-ai-bom` isn't already imported**, add it to your existing
`dependencyManagement` block (don't duplicate `imports { }` if you already
have one — just add the `mavenBom` line inside it):

```groovy
ext {
    set('springAiVersion', "2.0.1")
}

dependencyManagement {
    imports {
        mavenBom "org.springframework.ai:spring-ai-bom:${springAiVersion}"
    }
}
```

**b) Add these to your existing `dependencies { }` block** (alongside
whatever you already have for lombok, `OeWebController`, etc.):

```groovy
// --- MCP server (stdio) — exposes your @Tool beans. Copilot is the MCP
//     client and brings its own LLM, so no spring-ai-starter-model-*
//     provider dependency is needed, and no API key either.
implementation 'org.springframework.ai:spring-ai-starter-mcp-server'

// --- local, key-free embedding model for the upcoming vector-store/RAG
//     tool — runs an ONNX model (e.g. all-MiniLM-L6-v2) in-process via
//     ONNX Runtime. No API key, no network calls at inference time
//     (model file downloads once on first use).
implementation 'org.springframework.ai:spring-ai-starter-model-transformers'

// --- needed for OeQueryService's mock-request bridge (in-process call
//     into the existing forwarder — no inter-process HTTP hop) ---
implementation 'org.springframework:spring-test' // NOT testImplementation — used in main code
```

**c) Remove, if present:** `spring-ai-starter-model-stability-ai` (an
Initializr default pick, not something this project uses).

Confirmed settled from earlier discussion, no action needed:
- Plain jar packaging (not WAR) — fits stdio MCP's "Copilot spawns
  `java -jar ...`" process model. No conflict to resolve.
- `spring-ai-bom:2.0.1` is GA and supports Spring Boot 4.0.x/4.1.x — no
  milestone/snapshot repos needed.
- No LLM API key anywhere: the MCP server only registers `@Tool` beans,
  Copilot's own model decides when to call them; the local ONNX embedding
  model is key-free too.
- LangGraph isn't a fit here — it's Python/TS-only, and moot anyway since
  Copilot supplies the agent loop, not this app.
- Stdio needs no extra property beyond the `spring-ai-starter-mcp-server`
  dependency — that starter defaults to stdio.

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
| `OeQueryService.java` | `com.progress.pasoe.boot.ai` *(iteration 1)* |
| `OeQueryTools.java` | `com.progress.pasoe.boot.ai` *(replaces iteration 1 version — now uses OeSchemaCatalog)* |
| `OeSchemaDefinitionParserTest.java` | `src/test/java/com/progress/pasoe/boot/ai/schema` |
| The actual `.df` file (e.g. `sports2000.df`) | Anywhere readable at runtime — e.g. `src/main/resources/schema/sports2000.df`, then set `OE_SCHEMA_DF_PATH` to its resolved filesystem path (a classpath resource inside a jar isn't a `Path`, so either point at a file on disk, or say so and I'll switch the loader to read via `ClassPathResource` instead). |

## 4. Where to get a Sports2000 `.df` for testing

Public copy for reference/testing: `sports2000.df` in
`consultingwerk/BigSports20000` on GitHub. Grab that (or export your own
copy via the Data Dictionary: **Admin > Dump Definitions... > Database
Definitions (.df)**) and point `OE_SCHEMA_DF_PATH` at it.

## 5. Still open from iteration 1

- Confirm `OeWebRouteResolver.resolve(...)` null-handling.
- Confirm the forwarder reads query params via `request.getParameter(...)` (vs. re-parsing `getQueryString()`).