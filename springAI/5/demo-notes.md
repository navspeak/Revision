# Demo runbook: PASOE Boot (15 min)

Updated from your actual AI module (Spring AI 2.0.1, MCP server over stdio).

## Setup (do tonight)

- IntelliJ: project open, terminal tab ready in the repo root
- Browser: slides open full screen on a separate tab
- **Run the MCP profile once with network on.** The ONNX embedding model (all-MiniLM-L6-v2) downloads on first use; after that it is cached and works offline.
- Copilot with the MCP server configured, tested once end to end
- `.df` file for your demo database (e.g. sports2000.df) on disk, `OE_SCHEMA_DF_PATH` pointing at it
- The policy document in place (`classpath:policy/oe-support-policy.md` by default)
- Sonar reachable, last analysis already run as a fallback
- Backup: screenshots or a short screen recording of each demo

## Presenting the slides

Install once:

```
npm install -g @marp-team/marp-cli
```

Serve the deck in a browser (live reload while you edit):

```
marp -s .
```

Then open `http://localhost:8080/pasoe-boot.md`.

Other options:

```
marp pasoe-boot.md --html          # export to HTML
marp pasoe-boot.md --pdf           # export PDF backup for the laptop
marp pasoe-boot.md --preview       # opens a preview window
```

Tips:

- Press **F11** in the browser for full screen
- In the exported HTML, press **P** for presenter view (shows your notes)
- Switch between IntelliJ terminal and browser with Alt+Tab, or use two virtual desktops
- IntelliJ: the Markdown plugin shows a text preview; use the Marp plugin if you have it for in-IDE slides

## Timeline

| Min | What |
|---|---|
| 0-1 | Title, agenda |
| 1-4 | PASOE today, pain points |
| 4-8 | **Demo 1** (build, test, Sonar) |
| 8-10 | PASOE Boot, parity |
| 10-12 | AI diagram |
| 12-14 | **Demo 2** (MCP + Copilot) |
| 14-15 | Summary, questions |

## Demo 1: build, break, fix

1. `./gradlew clean build` shows a clean build, tests pass, one jar produced
2. `java -jar build/libs/pasoe-boot.jar` shows startup, one port, one command
3. Show the Actuator health endpoint, e.g. `curl localhost:8810/actuator/health`
4. **Show a test, not just a number.** Open `PolicyDocumentIngestorTest`: the whole class under test is built with `new PolicyDocumentIngestor(vectorStore, null, null)`. Constructor injection (Lombok `@RequiredArgsConstructor`) means no Spring context, no XML, no container. That is the DI/testability story in one line.
5. `./gradlew build -x test` skips tests. If a coverage gate (JaCoCo verification) is configured, show it failing here. Say: "Not Boot specific, but Boot's DI makes this easy to pass."
6. Show the Sonar dashboard: coverage, SAST findings, debt

Tests that exist in the AI module (mention the count, not the list):

- `AuditingToolCallbackTest` (4 tests: passes through, propagates errors, blocks oversized input, metadata unchanged)
- `PolicyDocumentIngestorTest` (6 tests: load, chunk, store, multi-document loop)
- `OeSchemaDefinitionParserTest`, `OeQueryServiceTest`, `PolicySearchToolsTest`, plus `OeQueryServiceLiveIT` (integration)

Say while it builds: no install directory, no instance creation, no WAR deploy.

## Demo 2: MCP with Copilot

Show first, in one minute, how little it took:

- `build.gradle`: `spring-ai-starter-mcp-server` and `spring-ai-starter-model-transformers`. No LLM provider dependency, no API key anywhere.
- `McpToolsConfig`: one bean registers both tool classes and wraps each tool in `AuditingToolCallback`.

Suggested prompts (adjust to your data; Sports2000 names shown):

1. "What tables are available in the database?" (OeQueryTools, table discovery)
2. "Describe the customer table." (columns and types from the `.df` catalog)
3. "Show me customers in <country>." (dynamic ABL query through the web handler, with a filter)
4. "What is the order cancellation policy?" (PolicySearchTools, RAG over the dropped document)
5. A combined question needing both, e.g. a customer's order status plus what the policy says about cancelling it

Say: "The MCP server has no LLM and no API key. The model is in Copilot. Any MCP client works the same way, including your own orchestration."

Optional beat: customers add their own documents by adding a path to `oe.ai.rag.document-paths` in `application.yml`. No code change.

### Copilot MCP config (stdio)

The `mcp` profile turns off the web server and console logging, because stdio MCP needs stdout to carry only JSON-RPC. Your normal `bootRun` or deployed instance is unaffected.

```json
{
  "servers": {
    "oe-query-server": {
      "type": "stdio",
      "command": "java",
      "args": [
        "-jar", "C:/path/to/pasoe-boot.jar",
        "--spring.profiles.active=mcp"
      ],
      "env": {
        "OE_SCHEMA_DF_PATH": "C:/path/to/sports2000.df"
      }
    }
  }
}
```

(Server name matches `spring.ai.mcp.server.name` in your notes. Adjust the jar path and your Copilot's config location.)

### Config reference

```yaml
oe:
  ai:
    schema:
      df-path: ${OE_SCHEMA_DF_PATH:}      # empty -> live _file discovery
    rag:
      document-paths:
        - classpath:policy/oe-support-policy.md
  tools:
    audit:
      max-input-length: 4000              # larger tool input is blocked

spring:
  ai:
    mcp:
      server:
        name: oe-query-server
        version: 1.0.0
        type: SYNC
        stdio: true
```

## Likely questions

- **"Why not do DI in the current model?"** You can. It's retrofitting against XML wiring; Boot makes it the default path.
- **"Do we lose any PASOE capability?"** No. ABL apps, REST and web handlers are unchanged.
- **"What about security?"** Java/annotation based config instead of XML, so it's testable.
- **"Does the MCP server call an LLM?"** No. It only registers tools. The agent side owns the model, and there is no API key in the app.
- **"Where does the table schema come from?"** The database's `.df`, parsed at startup into a catalog, with a live `_file` query as fallback. Switch databases by changing one property.
- **"Is the vector store production ready?"** It is an in-memory store (lost on restart, linear scan), fine for a demo corpus. `PolicyVectorStoreConfig` is the one place to swap in Chroma, Pinecone or pgvector.
- **"What stops the agent doing something dangerous?"** Every tool call goes through `AuditingToolCallback`: logged, timed, and guardrailed. Today it blocks oversized input; real guardrails extend one method.
- **"Does embedding send our documents anywhere?"** No. The ONNX model runs in-process, no outbound calls at query time (only a one-time model download).
- **"How do we migrate?"** Inventory instances and WARs, map CATALINA_BASE config to `application.yml`, run side by side, cut over.

## Things to verify before presenting

- Port names on the "PASOE today" slide match what you actually see (startup, HTTP, HTTPS, shutdown...)
- Exact MCP tool names as Copilot shows them. I did not have `OeQueryTools.java` or `PolicySearchTools.java` (they weren't in the folder), so tool names and the `filterField`/`filterOp` parameters come from your tests and comments only.
- Where audit log lines go in the `mcp` profile (console logging is off). Know this before you promise to "show the audit log live".
- Property names and ports in any config you show on screen
