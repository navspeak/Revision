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

// --- local, key-free embedding model for the vector-store/RAG tool —
//     runs an ONNX model (e.g. all-MiniLM-L6-v2) in-process via ONNX
//     Runtime. No API key, no network calls at inference time (model
//     file downloads once on first use).
implementation 'org.springframework.ai:spring-ai-starter-model-transformers'

// --- VectorStore / SimpleVectorStore live here — NOT pulled in
//     transitively by the transformers starter above, add explicitly.
//     Version comes from the BOM, no need to specify it.
implementation 'org.springframework.ai:spring-ai-vector-store'

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

## 6. Package correction (from live code review)

`OeWebRequestForwarder`, `OeWebRouteResolver`, and `OeWebRequestTarget`
actually live in **`com.progress.pasoe.boot.web`**, not `.controller`
(only `OeWebController` itself is in `.controller`). `OeQueryService.java`
has been updated to import from the correct package.

Also resolved: `OeWebRouteResolver.resolve(...)` **never returns null** —
it falls back to `defaultHandlerClass` — so open item #1 in section 5
above is settled, no null-check needed.

`mockito-core` comes with `spring-boot-starter-test`, already in your
dependencies — no new build.gradle entry needed for the tests below.

New test files and where they go:

| File | Package / location |
|---|---|
| `OeQueryServiceTest.java` | `src/test/java/com/progress/pasoe/boot/web` *(same package as OeWebRouteResolver/OeWebRequestTarget — see file comment for why)* |
| `OeQueryServiceLiveIT.java` | `src/test/java/com/progress/pasoe/boot/web` |

## 7. Iteration 3 — vector store / policy RAG tool

**One more build.gradle line needed** — `spring-ai-starter-model-transformers`
only provides the ONNX embedding model, not `VectorStore`/`SimpleVectorStore`.
Those live in a separate module (see the correction in section 1(b) above):

```groovy
implementation 'org.springframework.ai:spring-ai-vector-store'
```

New files and where they go:

| File | Package / location |
|---|---|
| `PolicyVectorStoreConfig.java` | `com.progress.pasoe.boot.ai.policy` |
| `PolicyDocumentIngestor.java` | `com.progress.pasoe.boot.ai.policy` |
| `PolicySearchTools.java` | `com.progress.pasoe.boot.ai.policy` |
| `oe-support-policy.md` | `src/main/resources/policy/oe-support-policy.md` |
| `PolicySearchToolsTest.java` | `src/test/java/com/progress/pasoe/boot/ai/policy` |

No `application.yml` changes needed for this piece — `SimpleVectorStore`
and the ONNX embedding model both work with zero config. The embedding
model file downloads once on first run and is cached locally afterwards
(first run needs network; later runs don't).

## 8. Iteration 4 — MCP server registration

No new build.gradle dependencies — `spring-ai-starter-mcp-server` (already
added in section 1) is all that's needed; `ToolCallbackProvider` and
`MethodToolCallbackProvider` come from `spring-ai-core`, pulled in
transitively.

New files:

| File | Location |
|---|---|
| `McpToolsConfig.java` | `com.progress.pasoe.boot.ai` |
| `application-mcp.yml` | `src/main/resources/application-mcp.yml` — a Spring **profile**, not a replacement for your existing `application.yml` |

**application.yml — add if not already present** (from section 2, restated
here since it's directly relevant to this iteration):

```yaml
spring:
  ai:
    mcp:
      server:
        name: oe-query-server
        version: 1.0.0
        type: SYNC
        stdio: true
```

**Why a separate profile file:** this app is dual-purpose — it serves
`/oe/data` over HTTP normally, but Copilot spawns it fresh over stdio for
MCP sessions. Stdio MCP requires stdout to carry *only* JSON-RPC
messages; the Spring Boot banner or any console log line corrupts that
stream. `application-mcp.yml` turns off the web server and console
logging, but **only** for the process Copilot spawns
(`--spring.profiles.active=mcp`) — your normal `bootRun`/deployed
instance is untouched and keeps serving HTTP as before.

## 9. Iteration 3 follow-up — configurable doc path, modular ingestion, testable steps

**New property** — override the demo doc without touching code or rebuilding
around it (points anywhere Spring's Resource loader understands: another
classpath resource, an external file, a URL):

```yaml
oe:
  policy:
    document: classpath:policy/oe-support-policy.md   # override, e.g. file:/etc/pasoe/policy.md
```

**`PolicyDocumentIngestor` refactored** into three package-private steps
(`loadDocument`, `chunkDocuments`, `embedAndStore`) instead of one `run()`
— `loadDocument`/`chunkDocuments` need no embedding model, so they're
fast, pure-logic unit tests.

**`PolicyVectorStoreConfig`** is (and always was) the one place to swap
`SimpleVectorStore` for Chroma/Pinecone/pgvector later — now called out
explicitly in the file comment since it wasn't obvious before.

New file: `PolicyDocumentIngestorTest.java` → `src/test/java/com/progress/pasoe/boot/ai/policy`

## 10. Iteration 5 — tool-call auditing (the Advisor question)

**Important clarification, not just a naming detail:** Spring AI's
`Advisor` interface only wraps `ChatClient` calls — it has no meaning
without a `ChatClient`/LLM, which this app deliberately doesn't have.
What's below is the equivalent pattern (wrap the call, run logic
before/after) applied at the `ToolCallback` layer instead — the layer
that actually exists here.

No new build.gradle dependencies — `ToolCallback`/`ToolCallbackProvider`
already come from `spring-ai-core`, already on the classpath.

**New property** — guardrail threshold, tune per environment:

```yaml
oe:
  tools:
    audit:
      max-input-length: 4000   # tool calls with larger JSON input get blocked, not executed
```

New files:

| File | Location |
|---|---|
| `AuditingToolCallback.java` | `com.progress.pasoe.boot.ai` — cross-cutting, not feature-scoped, per the earlier packaging discussion |
| `AuditingToolCallbackTest.java` | `src/test/java/com/progress/pasoe/boot/ai` |

`McpToolsConfig.java` updated — every callback from `MethodToolCallbackProvider` now gets wrapped before being exposed, so this applies uniformly to `OeQueryTools` and `PolicySearchTools` without touching either of those classes.
