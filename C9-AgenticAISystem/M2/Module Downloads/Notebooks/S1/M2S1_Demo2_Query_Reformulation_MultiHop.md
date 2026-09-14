# Notebook Walkthrough: Query Reformulation and Multi-Hop Retrieval

Source: `M2S1_Demo2_Query_Reformulation_MultiHop.ipynb`

## Overall Intent

This notebook teaches **agentic retrieval techniques that go beyond a single similarity search** — ways to reformulate a query, break it into hops, or route it to a different tool/backend before retrieving, using LangChain + LangGraph, model-agnostically.

- **HyDE** – embed a hypothetical answer instead of the raw question to fix lexically-thin queries
- **Query decomposition** – split a multi-hop question into ordered sub-questions via structured output
- **Iterative multi-hop retrieval** – loop over sub-questions, dedupe evidence, synthesize a final answer
- **Tool-augmented retrieval** *(🔧 LLM Tool Call pattern)* – let the LLM choose between retriever tools and a calculator via `bind_tools`
- **Routing** *(🚦 Dispatch pattern)* – a cheap, typed classifier (`with_structured_output`) that dispatches a question to `docs` / `calc` / `general`

---

## Questions Explored in This Session

- What makes the shared `retrieve()` function the notebook's "key design choice" (controlling for confounds across sections)?
- In the multi-hop loop, does the final LLM call use the retrieved EVIDENCE as its sole source of truth?
- What's the real difference between an **LLM tool call** (`bind_tools`, Cell 33) and a **dispatch call** (`dispatch()`, Cell 38) — since both end up calling `search_docs`/`search_math`?

---

## Unit 0 — Boilerplate (Cells 0–4)

Cells 0–2: markdown only (title, corpus rationale, "Setup" header) — nothing to explain.

Cells 3–4: pip install (commented) + imports, and LLM/embedding initialization:
```python
llm   = init_chat_model('gemini-2.5-flash-lite', model_provider='google_genai', temperature=0)
embed = init_embeddings('sentence-transformers/all-MiniLM-L6-v2', provider='huggingface')
```
Standard boilerplate, nothing special.

---

## Unit 1 — Two-Domain Corpus & Shared `retrieve()` (Cells 5–9)

```python
# 12-doc corpus deliberately split across two domains.
# d1..d7  -> company-ops chain (Atlas -> Helios -> Snowflake -> 400-credit quota)
# m1..m5  -> math / numeric facts (calculator-domain, not wiki-domain)
CORPUS = [
    {'id': 'd1', 'domain': 'docs', 'text': 'Project Atlas is the flagship customer-analytics product, owned by the Data Platform group.'},
    {'id': 'd2', 'domain': 'docs', 'text': 'Atlas depends on the Helios ingestion service for all upstream event data.'},
    {'id': 'd3', 'domain': 'docs', 'text': 'Helios streams data into the Snowflake warehouse via a Kafka -> Snowpipe bridge.'},
    {'id': 'd4', 'domain': 'docs', 'text': 'The Snowflake warehouse enforces a per-customer compute quota of 400 credits per month for any landing pipeline.'},
    {'id': 'd5', 'domain': 'docs', 'text': 'Priya Raman leads the Atlas product team and reports to Arjun Mehta, Director of Data Platform.'},
    {'id': 'd6', 'domain': 'docs', 'text': 'Karthik Iyer leads Ingestion Platform and owns Helios; he reports to Arjun Mehta.'},
    {'id': 'd7', 'domain': 'docs', 'text': 'Nadia Haq leads the Warehouse team and enforces the Snowflake compute quota and cost-allocation tags.'},
    {'id': 'm1', 'domain': 'math', 'text': 'One Snowflake credit currently costs 3 US dollars on the standard tier.'},
    {'id': 'm2', 'domain': 'math', 'text': 'There are 1024 megabytes in one gigabyte and 1024 gigabytes in one terabyte.'},
    {'id': 'm3', 'domain': 'math', 'text': 'A typical Helios partition processes 250 events per second on a standard worker.'},
    {'id': 'm4', 'domain': 'math', 'text': 'The Atlas SLA is 99.9 percent monthly uptime, which allows roughly 43.2 minutes of downtime per month.'},
    {'id': 'm5', 'domain': 'math', 'text': 'Pi is approximately 3.14159 and e is approximately 2.71828.'},
]
docs = [Document(page_content=c['text'], metadata={'id': c['id'], 'domain': c['domain']}) for c in CORPUS]
store = InMemoryVectorStore.from_documents(docs, embedding=embed)
```
```python
def retrieve(query: str, k: int = 3) -> List[Document]:
    """Top-k similarity retrieval shared by every later section..."""
    return store.similarity_search(query, k=k)

Q_RAW    = 'Who runs Atlas?'
Q_HOP    = 'What monthly compute quota applies to the warehouse used by the upstream service of Atlas?'
Q_NUM    = 'If Helios writes 400 credits worth of data this month, how many US dollars is that?'
```

**Explanation:**
- `d1`–`d7` are hand-built as a **chain**: Atlas → Helios → Snowflake → 400-credit quota, plus an org chart — the multi-hop fixture the decomposition/loop sections depend on.
- `m1`–`m5` are numeric facts that deliberately don't belong in the docs domain — they exist so the router/tool-selection sections have something to send to a calculator instead of the wiki retriever.
- `retrieve()` is defined **once** and reused everywhere. This is the key design choice of the whole notebook.

**Why the shared `retrieve()` matters (Q&A deep dive):**
If every section used a different retrieval setup (different `k`, vector store, similarity metric, reranker), you couldn't tell whether an improvement came from the reformulation technique or from a better retriever underneath — the comparison would be confounded. By freezing `retrieve()`, the vector store, the embedding model, and `k` across every section, the **only** variable that changes across sections is *what string gets handed to `retrieve()`*: raw question vs. HyDE's hypothetical answer vs. a decomposed sub-question. This makes every "ID delta" comparison in the notebook causally attributable to the reformulation strategy — not an artifact of a differently-configured retriever. Same principle as holding all variables constant except one in a controlled experiment.

- The three eval questions are each engineered to expose a specific weakness: `Q_RAW` is lexically thin → HyDE; `Q_HOP` hides multiple lookups → decomposition; `Q_NUM` needs lookup + arithmetic → tool use.

---

## Unit 2 — HyDE (Cells 10–16)

```python
raw_hits = retrieve(Q_RAW, k=3)   # baseline
```
```python
HYDE_PROMPT = """You are drafting a HYPOTHETICAL one-paragraph answer to a user question.
It is fine if you do not know the true answer — write the kind of paragraph you WOULD expect
to find in a wiki or runbook that addresses this question. Use full sentences, named entities,
and concrete nouns. Do not hedge.
Question: {q}
Hypothetical answer:"""

def hyde_query(question: str) -> str:
    return llm.invoke(HYDE_PROMPT.format(q=question)).content   # 🔵 LLM call (generation only, no retrieval)
```
```python
hypo = hyde_query(Q_RAW)
hyde_hits = retrieve(hypo, k=3)   # retrieve against the hypothetical answer's embedding
```

**Explanation:**
- Cell 11 establishes a weak baseline: `Q_RAW = "Who runs Atlas?"` is short and lexically thin on purpose.
- Cell 13 is the core HyDE mechanic: ask the LLM to hallucinate a plausible-sounding answer first — even a wrong one — because answers and questions embed into different neighborhoods, but a fabricated answer's embedding lands closer to a real answer chunk than the question's embedding does.
- Cell 15 diffs `raw_hits` ids vs `hyde_hits` ids — the expectation is `d5` ("Priya Raman leads Atlas") appears in HyDE's results but not the baseline's, direct evidence the reformulation (not a better retriever) is responsible.
- Tip: HyDE costs one extra LLM call, no re-indexing needed; keep `temperature=0` for reproducibility.

---

## Unit 3 — Decomposition Schema (Cells 17–20)

```python
class SubQueries(BaseModel):
    """Decomposition schema..."""
    queries: List[str] = Field(
        description='Two or three focused sub-questions...',
        min_length=2, max_length=3,
    )
```
```python
DECOMPOSE_PROMPT = """You are a retrieval planner. ... Decompose it into 2-3 focused sub-questions
such that each sub-question can be answered by a single short paragraph. Order the sub-questions
from the first hop ... to the last hop ...
Question: {q}
"""
decomposer = llm.with_structured_output(SubQueries)

def decompose(question: str) -> SubQueries:
    return decomposer.invoke(DECOMPOSE_PROMPT.format(q=question))   # 🔵 LLM call (structured output)

subs = decompose(Q_HOP)
```

**Explanation:**
- `SubQueries`'s `min_length=2, max_length=3` is a structural constraint, not just a prompt suggestion — the LLM cannot return 9 sub-questions and blow up downstream loop cost.
- `llm.with_structured_output(SubQueries)` gives a typed call instead of free text you'd have to regex-parse.
- `Q_HOP` hides three lookups (upstream service of Atlas → its warehouse → that warehouse's quota); this cell should show the LLM correctly unpacking that chain, in retrieval order — because the next unit retrieves for them in that order.

---

## Unit 4 — Iterative Multi-Hop Retrieval Loop (Cells 21–27)

```python
def format_context(docs: List[Document]) -> str:
    return '\n'.join(f"[{d.metadata['id']}] {d.page_content}" for d in docs)
```
```python
ANSWER_PROMPT = """Answer the user's QUESTION using ONLY the EVIDENCE below. Cite [doc_ids] inline.
QUESTION: {q}
EVIDENCE:
{ctx}
"""

def multi_hop_retrieve(question: str, k: int = 3) -> dict:
    subs = decompose(question)                     # 🔵 LLM call #1 (structured output, see Unit 3)
    evidence: List[Document] = []
    seen_ids: set = set()
    trace: List[dict] = []
    for hop, sub in enumerate(subs.queries, 1):
        hits = retrieve(sub, k=k)                   # vector search, NOT an LLM call
        new = [d for d in hits if d.metadata['id'] not in seen_ids]
        seen_ids.update(d.metadata['id'] for d in new)
        evidence.extend(new)
        trace.append({'hop': hop, 'sub_query': sub, 'new_ids': [d.metadata['id'] for d in new]})
    answer = llm.invoke(ANSWER_PROMPT.format(q=question, ctx=format_context(evidence))).content  # 🔵 LLM call #2 (final synthesis)
    return {'sub_queries': subs.queries, 'evidence_ids': sorted(seen_ids), 'answer': answer, 'trace': trace}
```

**Explanation:**
- `format_context` serializes retrieved docs deterministically — evidence formatting is never the reason results differ across sections.
- The core pattern: `decompose → for each sub-question: retrieve + dedupe → synthesize`.
  - **Deduping by `metadata['id']`** across hops stops an easy first-hop chunk from re-winning `top-k` on every sub-question and crowding out harder-to-reach chunks later hops need.
  - **Hop count is bounded by the `SubQueries` schema** (max 3) — no loop guard needed here because the upstream contract already caps it.
- The final LLM call is instructed to use **ONLY the EVIDENCE** and cite `[doc_ids]` inline — this is the standard RAG grounding pattern: retrieval decides what's true, generation only decides how to phrase it, and citations make the grounding checkable/auditable. If decomposition/retrieval had failed to surface `d4`, this call could not answer correctly even in principle, since it's constrained to the evidence it's handed.
- Tip: decomposition and HyDE aren't mutually exclusive — you can embed the *hypothetical answer of each sub-question* instead of the sub-question text itself.

### Dry Run — `multi_hop_retrieve(Q_HOP)`

**🔵 LLM Call #1 — `decompose(Q_HOP)`**
```
OUT (SubQueries.queries):
  1. "What is the upstream service that Atlas depends on?"
  2. "Which warehouse does that upstream service use?"
  3. "What is the monthly compute quota for that warehouse?"
```

| Hop | sub_query | retrieve() top hit | new_ids |
|---|---|---|---|
| 1 | upstream service of Atlas? | `d2` Helios | `[d1, d2]` |
| 2 | which warehouse? | `d3` Snowflake | `[d3]` |
| 3 | monthly quota? | `d4` 400 credits | `[d4]` |

**🔵 LLM Call #2 — final synthesis**
```
IN  EVIDENCE: [d1] [d2] [d3] [d4] text blocks
OUT answer: "Atlas's upstream service is Helios [d2], which feeds the Snowflake
             warehouse [d3]. That warehouse enforces a monthly compute quota of
             400 credits [d4]."
```
Total: 2 LLM calls + 3 vector searches; a single raw-question `retrieve(Q_HOP)` would very likely miss `d4` entirely.

---

## Unit 5 — Tool-Augmented Retrieval with `bind_tools` 🔧 (Cells 28–34)

> **Marked as: LLM TOOL CALL pattern** — the LLM itself decides *which* tool(s) to call and *what arguments* to pass. Your code only executes the LLM's plan.

```python
@tool
def search_docs(query: str) -> str:
    """Search the company-ops wiki (Atlas, Helios, Snowflake, org chart, quotas).
    Use this for narrative questions about people, services, ownership, and policies."""
    hits = [d for d in retrieve(query, k=4) if d.metadata['domain'] == 'docs'][:3]
    return format_context(hits) if hits else 'No matching docs.'

@tool
def search_math(query: str) -> str:
    """Search the math / numeric facts table (constants, conversion rates, unit prices).
    Use this when you need to look up a numeric fact before computing with it."""
    hits = [d for d in retrieve(query, k=4) if d.metadata['domain'] == 'math'][:3]
    return format_context(hits) if hits else 'No matching math facts.'

@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression like '400 * 3' or '(1024 ** 2)'.
    Use this AFTER you have looked up the numeric facts you need."""
    allowed = set('0123456789+-*/()., ')
    expr = ''.join(c for c in expression if c in allowed)
    return str(eval(expr)) if expr else 'empty expression'
```
```python
tools = [search_docs, search_math, calculator]
tool_llm = llm.bind_tools(tools)   # declares the tools to the LLM; does not execute anything
```
```python
response = tool_llm.invoke(Q_NUM)          # 🔵 LLM call — produces a PLAN, not a result

# 🔧 TOOL CALLS (manual execution, in your code, NOT the LLM):
tool_by_name = {t.name: t for t in tools}
for tc in response.tool_calls:
    out = tool_by_name[tc['name']].invoke(tc['args'])   # <-- actual local execution happens HERE
```

**Explanation:**
- `search_docs`/`search_math` both reuse the same shared `retrieve()`, then post-hoc filter by `metadata['domain']` — the domain split is Python filtering, not a vector-store-level constraint. That's why `k=4` (larger than usual) is used: headroom for cross-domain hits to get filtered away.
- **Docstrings are the entire interface** the LLM sees for deciding when to use each tool. `calculator`'s docstring explicitly says "Use this AFTER you have looked up the numeric facts" — this is prompt-engineering the tool description itself to bias correct call ordering.
- `eval()` in `calculator` is guarded only by a character whitelist — fine for a demo, not production-safe against arbitrary LLM-generated strings.
- Critically: `bind_tools` only makes the LLM **emit** `tool_calls`; it does not execute them. Cell 33's final loop is where actual execution happens — locally, in your process, driven by your `for` loop, not inside the LLM.
- Tip (Cell 34): the split (LLM decides → your code executes) is what gives you a chance to validate/log/rate-limit before any side effect runs.

### Dry Run — `search_docs`, `search_math`, `calculator` (Cell 29)

```
search_docs("What is the upstream service that Atlas depends on?")
  retrieve(k=4) top-4 (unfiltered): [d2, d1, m3, d5]
  filter domain=='docs', keep 3   → [d2, d1, d5]
  OUT: "[d2] Atlas depends on Helios... [d1] Project Atlas is... [d5] Priya Raman leads..."

search_math("How much does one Snowflake credit cost?")
  retrieve(k=4) top-4 (unfiltered): [m1, d4, m2, d3]
  filter domain=='math', keep 3   → [m1, m2]   (only 2 survive)
  OUT: "[m1] One Snowflake credit costs 3 USD... [m2] 1024 MB in a GB..."

calculator("400 * 3")
  char-whitelist filter → "400 * 3" (unchanged)
  eval("400 * 3") → 1200
  OUT: "1200"
```

### Dry Run — Cell 33 full flow (`Q_NUM`)

**🔵 LLM Call — `tool_llm.invoke(Q_NUM)`**
```
OUT: response.content = ""  (empty; model chose to act, not talk)
     response.tool_calls =
       [ {"name": "search_math", "args": {"query": "cost of one Snowflake credit in US dollars"}},
         {"name": "calculator",  "args": {"expression": "400 * 3"}} ]
```

**🔧 TOOL CALLS — manual execution loop (your Python code):**
```
---- search_math ----
[m1] One Snowflake credit currently costs 3 US dollars on the standard tier.

---- calculator ----
1200
```
Note: the cell stops here — it never feeds `m1`'s text and `1200` back to the LLM as `ToolMessage`s for a final natural-language answer ("$1200"). A complete agent loop would add that synthesis round-trip.

---

## Unit 6 — Routing with `RouteDecision` 🚦 (Cells 35–41)

> **Marked as: DISPATCH pattern** — the LLM only picks a category *label*; your hardcoded `if/elif/else` decides which function to call next. Contrast with Unit 5, where the LLM itself picks the tool + arguments.

```python
class RouteDecision(BaseModel):
    """Where should this question be answered? One of three destinations.
    The Literal[...] type keeps branching stable across runs — the LLM cannot
    invent a fourth route and crash the dispatch."""
    route: Literal['docs', 'calc', 'general'] = Field(
        description="'docs' for company-ops wiki questions, 'calc' for numeric / arithmetic questions, 'general' otherwise."
    )
    reason: str = Field(description='One short sentence justifying the route.')
```
```python
ROUTER_PROMPT = """You are a router. Read the QUESTION and choose ONE route:
- 'docs'    : the answer is in the company-ops wiki (people, services, ownership, quotas).
- 'calc'    : the question requires arithmetic on numeric facts (multiplications, conversions).
- 'general' : neither of the above — answer from your own knowledge.
QUESTION: {q}"""

router = llm.with_structured_output(RouteDecision)

def route_query(question: str) -> RouteDecision:
    return router.invoke(ROUTER_PROMPT.format(q=question))   # 🔵 LLM call — outputs ONLY a label + reason

# 🚦 DISPATCH — hardcoded Python if/elif, NOT an LLM decision:
def dispatch(question: str) -> dict:
    decision = route_query(question)
    if decision.route == 'docs':
        answer = search_docs.invoke({'query': question})          # plain function call on a Tool object
    elif decision.route == 'calc':
        answer = tool_llm.invoke(question).content or '(see tool_calls)'   # 🔵 LLM call (see Unit 5 pattern)
    else:
        answer = llm.invoke(question).content                     # 🔵 bare LLM call, no retrieval
    return {'question': question, 'route': decision.route, 'reason': decision.reason, 'answer': answer}
```

**Explanation:**
- `RouteDecision`'s `Literal['docs','calc','general']` is a hard structural constraint — the branching in `dispatch()` is exhaustive and crash-proof by construction.
- `reason` exists purely for auditability/logging, to build an offline eval dataset for retuning the router prompt.
- **Key architectural contrast:** in `dispatch()`, `search_docs.invoke(...)` is called because **your** `if/elif` mapped `route=='docs'` to it — the router LLM never saw `search_docs` as an option and never chose to invoke it. This is different from `tool_llm.invoke(Q_NUM)` in Unit 5, where the LLM itself names the tool and supplies arguments. Both call `.invoke()` (the shared LangChain Runnable interface), but only one is an LLM-driven tool call.
- Tip (Cell 41): version the router prompt like code, keep `temperature=0`, trace regressions to specific prompt edits.

### Dry Run — `dispatch()` across 3 examples

**1. `dispatch(Q_HOP)`**
```
🔵 route_query(Q_HOP) → RouteDecision(route='docs', reason='...warehouse quota, company-ops wiki content.')
🚦 dispatch branch: route=='docs' → search_docs.invoke({'query': Q_HOP})   (no LLM here, just filtered retrieve())
OUT answer: "[d4] 400 credits... [d3] Helios streams... [d2] Atlas depends on Helios..."
```

**2. `dispatch(Q_NUM)`**
```
🔵 route_query(Q_NUM) → RouteDecision(route='calc', reason='...requires converting credits to dollars via arithmetic.')
🚦 dispatch branch: route=='calc' → tool_llm.invoke(Q_NUM).content
🔵 tool_llm.invoke(Q_NUM) → response.content = ""  (LLM emitted tool_calls instead, see Unit 5)
OUT answer: "(see tool_calls)"   ⚠️ dispatch() never executes tool_calls, so no numeric answer is produced here
```

**3. `dispatch("In one sentence, what is retrieval-augmented generation?")`**
```
🔵 route_query(...) → RouteDecision(route='general', reason='Not about company docs or arithmetic.')
🚦 dispatch branch: route=='general' → llm.invoke(question).content
🔵 llm.invoke(...) → "RAG is a technique where a language model retrieves relevant external
                      documents and uses them as context to generate a grounded response."
```

| Example | route_query() | Follow-up call | LLM calls total |
|---|---|---|---|
| Q_HOP | 1 | `search_docs` (no LLM) | 1 |
| Q_NUM | 1 | `tool_llm.invoke()` (🔧 tool-call pattern) | 2 |
| general Q | 1 | `llm.invoke()` (bare) | 2 |

The router itself is always exactly **one cheap, typed LLM call**; the cost of the second call varies entirely by which branch it dispatches to.

---

## Unit 7 — Tips & Pitfalls (Cell 42, markdown-only)

### Adopting reformulation and routing in production
- Run reformulation strategies in **parallel**, not in series; merge by id with rank fusion (RRF).
- Cap sub-questions in the decomposition schema — `max_length=3` is a teaching value; pick a number that bounds worst-case cost per query.
- Always log **router decision + reason + final tool calls** — that log is the offline-eval dataset for retuning the router prompt.
- Keep `temperature=0` on every reformulation/decomposition/routing call.

### Common pitfalls in tool-augmented retrieval
- LLMs sometimes call tools with badly-typed arguments — write explicit Pydantic argument schemas for non-trivial tool signatures.
- `bind_tools` only declares tools; forgetting to feed results back as a `ToolMessage` is the #1 reason agents "silently give up" after one call (exactly the gap seen in `dispatch()`'s `calc` branch above).
- Tool docstrings **are** the tool descriptions the LLM sees — vague docstrings produce vague routing.
- Watch for **route collapse** (same route picked regardless of content) — hold out a balanced eval set per route and re-check after every prompt change.

**Why this cell matters:** it's the bridge from "toy demo" (sequential, isolated techniques) to production reality (parallel reformulation, logged/audited routing, and the specific brittleness points — like the unexecuted `tool_calls` in the `calc` route — that this walkthrough surfaced directly.
