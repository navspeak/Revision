---
marp: true
theme: default
paginate: true
backgroundColor: #0d1117
color: #c9d1d9
style: |
  section { font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace; font-size: 27px; }
  h1, h2 { color: #58a6ff; }
  strong { color: #f0883e; }
  code { background: #161b22; color: #7ee787; }
  pre { background: #161b22; border: 1px solid #30363d; font-size: 18px; }
  table { font-size: 22px; }
  th { background: #161b22; color: #58a6ff; }
  td { background: #0d1117; }
  section.demo { background: #1a1305; text-align: center; justify-content: center; }
  section.demo h1 { color: #f0883e; }
---

# PASOE Boot

### From WAR deployments to a single fat jar

`$ java -jar pasoe-boot.jar`

<!--
15 min total. Slides are anchors; the terminal does the heavy lifting.
Open: "What if PASOE was just a jar?"
-->

---

## Agenda

1. PASOE architecture today
2. Pain points and tech debt
3. **Live:** build, test, Sonar
4. PASOE Boot
5. **Live:** AI + MCP

<!-- Keep this under 20 seconds. -->

---

## PASOE today

- Tomcat + OpenEdge ABL runtime
- **CATALINA_HOME** + **CATALINA_BASE**: two trees to manage
- **WAR** deployments and the tooling around them
- Many ports: startup, HTTP, HTTPS, shutdown...
- Tailoring needed between install dir and instance

<!--
Talking points:
- Home = shared binaries, Base = per-instance conf/webapps/logs.
- Every instance means port assignments, tailoring scripts, WAR deploy steps.
- All of this is configuration that has to be correct, versioned and patched.
-->

---

## Pain points

- **XML-based Spring Security**, heavy property substitution
- Third-party jars assembled by hand, **no starters**
- **SAST findings** and tech debt rooted in XML bean wiring
- DI and testability **retrofitted**, not natural

<!--
Talking points:
- XML: hard to maintain, beans don't auto-wire easily, testing is difficult.
- Dependencies: plain Gradle, transitive deps cherry-picked. With a starter, a CVE fix is "bump the starter".
- SAST/debt: the framework doesn't enforce modern Java. Boot's config + beans + autowiring pushes you to testable code, so JUnit coverage (even 100%) becomes realistic. Management cares about this.
- Proof from the AI module: constructor injection means a test is just
  new PolicyDocumentIngestor(mockVectorStore, props, loader). No Spring context, no XML, no container. (PolicyDocumentIngestorTest)
- If asked "why can't you do DI today?": You can, DI isn't new to Boot. But the current setup is deeply XML-wired, so clean DI means fighting the structure. Boot makes it the path of least resistance.
-->

---

<!-- _class: demo -->

# LIVE

## Build it. Break it. Fix it.

`./gradlew build` · `build -x test` · Sonar

<!--
Switch to IntelliJ terminal. See demo-notes.md for the exact sequence.
Message: this isn't Boot-specific, but Boot makes it the default way of working.
-->

---

## PASOE Boot

One **fat jar**: embedded Tomcat + ABL app + defaults

| Today | PASOE Boot |
|---|---|
| CATALINA_HOME | Embedded in jar |
| CATALINA_BASE | `application.yml` / env vars |
| WARs | Servlet **filters**, in the jar |
| Many ports | One server port |
| Tailoring | Nothing to tailor |

<!--
Talking points:
- Configuration becomes code, so there is less of it. Everything is a program or a function.
- No WAR deployments: behaviour is composed with filters. Big cut in tooling sprawl.
- Everything is jar based, so no tailoring between install directory and instance.
-->

---

## Same capabilities. Better operations.

- ABL apps, REST, web handlers: **unchanged**
- Management: **Actuator** health, metrics, env
- Containers: small immutable image, one `ENTRYPOINT`
- Patching: bump a starter, ship a new jar
- CI/CD: the jar **is** the release

<!--
Talking points:
- Customers keep everything PASOE gives them today.
- Dockerfile is 4 lines: FROM temurin jre, COPY jar, EXPOSE, ENTRYPOINT java -jar.
- Kubernetes: liveness/readiness from Actuator, config via ConfigMaps/Secrets.
-->

---

## AI on PASOE Boot

```
 Agent loop (Copilot / LangGraph / any MCP client)   <- LLM lives here
                  │  MCP over STDIO
                  ▼
 ┌──────────────── PASOE Boot  (profile: mcp) ────────────────┐
 │  Spring AI MCP server           no LLM · no API key         │
 │   └─ AuditingToolCallback   log · time · guardrail          │
 │       ├─ OeQueryTools   list tables · describe · query      │
 │       │    .df schema (or live _file) → generic ABL         │
 │       │    → web handler (in-process) → OpenEdge DB         │
 │       └─ PolicySearchTools   RAG, bring your own docs       │
 │            local ONNX embeddings → vector store → KNN       │
 └─────────────────────────────────────────────────────────────┘
```

**Two starters:** MCP server + local embeddings.

<!--
Talking points:
- OeQueryTools answers questions on live customer data. Table/column schema comes from the database's .df (OeSchemaCatalog), with a live _file query as fallback, so it works for any OpenEdge database by changing one property. Queries go through the same PASOE web handler mechanism, called in-process (no extra HTTP hop).
- PolicySearchTools covers what tables can't: customers bring their own documents (oe.ai.rag.document-paths, a list). Chunked, embedded with a local ONNX model (all-MiniLM-L6-v2), held in an in-memory vector store, retrieved by KNN similarity.
- MCP layer only exposes tools. No LLM inside, no API key. Copilot (or your own LangGraph orchestration) owns the model.
- AuditingToolCallback wraps every tool: logs name, input, duration, outcome, and blocks oversized input (max 4000 chars, configurable). Same idea as a ChatClient Advisor, but at the tool layer since there is no ChatClient here.
- Vector store swap: PolicyVectorStoreConfig is the one place to move from in-memory to Chroma/Pinecone/pgvector.
-->

---

<!-- _class: demo -->

# LIVE

## Ask OpenEdge in plain English

Copilot → MCP → PASOE Boot

<!--
Switch to IntelliJ / Copilot. See demo-notes.md for suggested prompts.
-->

---

## Summary

- **Same capabilities**, one jar
- Fewer ports, no WARs, no tailoring
- Less tech debt, testable by default
- AI-ready through Spring AI and MCP

### Questions?

`$ exit 0`
