# Testing & demo — iteration 2 (schema-aware query tools)

## What's unit-tested (not runnable from outside)

`OeSchemaDefinitionParser` is pure text-in/records-out — no server, no
network — so it's covered by `OeSchemaDefinitionParserTest.java` instead of
a live demo step. Run it with:

```bash
./gradlew test --tests "com.progress.pasoe.boot.ai.schema.OeSchemaDefinitionParserTest"
```

It checks: table/field names parse correctly, data type/format/label parse
correctly, `MANDATORY` is captured per-field, the primary key comes from a
`UNIQUE PRIMARY` index's `INDEX-FIELD` lines (and *not* from a non-primary
index), and an empty `.df` produces an empty map rather than throwing.

## What's live-testable

### Step 1 — get a Sports2000 `.df` and point the app at it

```bash
export OE_SCHEMA_DF_PATH=/path/to/sports2000.df
./gradlew bootRun
```

Watch the startup log for:

```
Loaded NN tables from /path/to/sports2000.df
```

If you see the "not readable" or "not set" warning instead, the catalog is
empty and tools will fall back to live `_file` discovery — still functional,
just without column-level detail.

### Step 2 — exercise the tools directly over HTTP (bypassing the LLM)

If you've wired `OeQueryTools` behind a `ChatClient` endpoint already, the
fastest sanity check is skipping the model entirely and hitting the
underlying service call your tool delegates to — i.e. your existing
`/oe/data/...` endpoint, same as curl.txt:

```bash
# table discovery still works even with the .df loaded (sanity check
# the live path hasn't broken)
curl -k "http://localhost:8080/oe/data/_file?columns=_file-name&limit=50"

# a table your .df claims exists
curl -k "http://localhost:8080/oe/data/Customer?columns=CustNum,Name&limit=5"
```

### Step 3 — exercise it through the model (the actual demo)

Once you've got a `ChatClient` wired with these tools (next iteration),
demo script:

1. **"What tables can I query?"**
   → should invoke `listAvailableTables`, and since `.df` is loaded, answer
   instantly from the catalog (no REST round trip) rather than the live
   `_file` query — worth pointing out during the demo as the "smart" path.

2. **"What columns does the Customer table have?"**
   → should invoke `describeTable("Customer")`, returning field
   name/type/label/mandatory and the primary key (`CustNum`).

3. **"Show me 5 customers with a balance over 1000."**
   → should invoke `describeTable` first (or already know from step 2),
   then `queryTable("Customer", "CustNum,Name,Balance", "Balance", "GT", "1000", 5)`.

4. **Negative test — ask about a table that doesn't exist**, e.g. *"query
   the Widgets table"* → should invoke `listAvailableTables`/`describeTable`,
   get "no table named Widgets", and say so instead of guessing or calling
   `queryTable` blind. This demonstrates the discovery-before-query guardrail
   actually working, which is a good thing to narrate in the demo.

### Step 4 — MCP discovery from GitHub Copilot CLI

Once the MCP server starter is wired (iteration 3), test discovery with:

```bash
copilot
/mcp add
# Server Name: oe-query-server
# Server Type: STDIO
# Command: java -jar build/libs/<your-app>.jar
```

Then in the Copilot CLI session, ask it something that should trigger
`listAvailableTables`/`queryTable` and confirm it calls out to your server
rather than hallucinating an answer.

## Iteration 3 — vector store / policy RAG tool

### What's actually testable end-to-end (not just unit-tested)

Unlike the OE query tools, this pipeline needs no live external service —
the embedding model is local ONNX, no API key, no network calls at query
time. So `PolicySearchToolsTest` is a real integration test, not a
parser-style stand-in: it boots the full context (so
`PolicyDocumentIngestor` actually runs as it would in production),
confirms the vector store gets populated, and checks `searchPolicy`
surfaces the right passage for a few sample questions.

```bash
./gradlew test --tests "com.progress.pasoe.boot.ai.policy.PolicySearchToolsTest"
```

First run downloads the ONNX model — needs network once, then it's
cached. If you're offline or want to skip the download in CI, mark the
test `@Disabled` or exclude the package.

### Demo script

1. **"What's our policy on returning a damaged item?"**
   → should invoke `searchPolicy`, surfacing the 90-day damaged-item
   window from Section 2 — distinct from the 30-day standard return
   window, good "it actually read the nuance" moment for the demo.

2. **"Can a sales rep approve a 25% discount on their own?"**
   → should invoke `searchPolicy`, surfacing Section 3 (Regional Director
   approval required above 20%).

3. **Combined query — the interesting one:** *"Customer 12 wants to
   return a damaged Item they ordered last month — are they still within
   policy, and what was on that order?"*
   → this should make the model call **both** tools: `searchPolicy` for
   the 90-day damaged-item window, and `queryTable`/`describeTable` for
   Customer 12's actual order data. Worth narrating explicitly in the
   demo since it's the clearest illustration of tool orchestration across
   your two different data sources (structured OE data vs. unstructured
   policy text) — this is the payoff moment for the whole exercise.

4. **Off-topic query** — e.g. *"what's the weather like"* — a good
   moment to show the model correctly *not* calling `searchPolicy` (or
   calling it and reporting no relevant match) rather than fabricating a
   policy answer.

## Iteration 4 — MCP server registration

### Sanity check before involving Copilot at all

Build the jar and run it standalone in MCP mode to confirm it starts
cleanly and doesn't immediately crash or print anything to stdout:

```bash
./gradlew bootJar
java -jar build/libs/<your-app>.jar --spring.profiles.active=mcp
```

It should sit there silently (no banner, no log lines) waiting on stdin —
that silence is actually the success signal. Ctrl+C to stop; if you see
any Spring Boot banner or log output here, `application-mcp.yml` isn't
being picked up (check the profile name/spelling) and Copilot's
connection will fail the same way.

### Register with GitHub Copilot CLI

```bash
copilot
/mcp add
# Server Name: oe-query-server
# Server Type: STDIO
# Command: java
# Args: -jar /full/path/to/build/libs/<your-app>.jar --spring.profiles.active=mcp
```

Use an absolute path for the jar — Copilot spawns the process from
wherever the CLI itself is running, not necessarily your project
directory.

### Demo script (this is the actual payoff moment)

1. **"What OpenEdge tables can I query?"** → Copilot should discover and
   call `listAvailableTables` on its own, no prompting needed — this is
   the first real proof MCP discovery is working end to end.

2. **"What's our policy on returning a damaged item?"** → `searchPolicy`.

3. **The combined one** (same as iteration 3's demo script, now actually
   running through Copilot instead of a direct method call): *"Customer
   12 wants to return a damaged Item they ordered last month — are they
   still within policy, and what was on that order?"* Watch Copilot
   choose to call both `searchPolicy` and `queryTable`/`describeTable`
   without being told which tools exist for which purpose — that
   orchestration coming from the tool descriptions alone (not any
   Copilot-specific prompting) is the whole point of this exercise.

4. **Negative test** — ask about a nonexistent table or an off-topic
   question, confirm Copilot reports what the tools actually returned
   rather than filling in a plausible-sounding answer itself.

If Copilot's connection fails outright (not "assistant gave a wrong
answer" but "couldn't reach the server"), the fix is almost always one of:
- Console output leaking into stdout (see the standalone check above).
- Wrong/relative jar path in the `/mcp add` command.
- The jar wasn't rebuilt after the latest code changes (`./gradlew bootJar`
  first).
