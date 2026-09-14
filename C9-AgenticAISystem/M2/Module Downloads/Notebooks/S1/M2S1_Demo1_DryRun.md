Dry Run: `retrieve → reason → should_continue` Loop
Initial State (before any node runs)
```python
state = {
    'question': "When was the Eiffel Tower built and who designed it?",
    'evidence': [],
    'seen_ids': [],
    'iteration': 0,
    'next_query': "When was the Eiffel Tower built and who designed it?",  # starts = question
    'status': 'start',
    'answer': '',
    'trace': [],
}
```
---
Step 1 — `retrieve` node runs first (entry point)
Input: `state['next_query']` = `"When was the Eiffel Tower built and who designed it?"`
Calls: a retriever (vector search, not an LLM) with that query.
Say it returns 2 chunks. Output merged into state:
```python
evidence = [
    Document(id='d1', content="The Eiffel Tower was completed in 1889..."),
    Document(id='d2', content="It was built for the 1889 World's Fair..."),
]
seen_ids = ['d1', 'd2']
```
---
Step 2 — `reason` node runs (LLM call happens here)
```python
it = 0 + 1  # = 1
ctx = "[d1] The Eiffel Tower was completed in 1889...\n[d2] It was built for the 1889 World's Fair..."
```
Since `it (1) < MAX_ITERS (3)`, we take the normal branch:
```python
decision = structured_llm.invoke(REASON_PROMPT.format(q=state['question'], ctx=ctx))
```
What the LLM actually receives (filled prompt)
```
You are an agentic retriever. Given the question and the evidence gathered so far, 
decide: do you have enough to answer? 
- If yes, set status='answer' and fill `answer`. 
- If not, set status='need_more' and propose ONE targeted follow-up query...

Question: When was the Eiffel Tower built and who designed it?

Evidence so far:
[d1] The Eiffel Tower was completed in 1889...
[d2] It was built for the 1889 World's Fair...
```
What comes back — `decision` is a `ReasonDecision` object
```python
ReasonDecision(
    status='need_more',
    next_query='who was the engineer or architect who designed the Eiffel Tower',
    answer=None
)
```
(The evidence has the date, but not the designer — so the model reasonably decides it needs more.)
The code unpacks it
```python
status = decision.status        # 'need_more'
nq = decision.next_query        # 'who was the engineer...'
ans = decision.answer or ''     # '' (was None)

trace = [] + [{'iter': 1, 'decision': 'need_more', 'next_query': 'who was the engineer...'}]

return {
    'iteration': 1,
    'status': 'need_more',
    'next_query': 'who was the engineer or architect who designed the Eiffel Tower',
    'answer': '',
    'trace': [{'iter': 1, 'decision': 'need_more', 'next_query': '...'}],
}
```
---
Step 3 — `should_continue` routes
```python
return END if state['status'] == 'answer' else 'retrieve'
# status == 'need_more' → returns 'retrieve'
```
→ Loops back to `retrieve`, this time using the new `next_query` about the designer.
---
Iteration 2 — same shape, but now finds the answer
`retrieve` fetches new docs about Gustave Eiffel, appends to `evidence`/`seen_ids` (now 4 documents total).
`reason` runs again:
```python
decision = ReasonDecision(
    status='answer',
    next_query=None,
    answer="The Eiffel Tower was completed in 1889 and designed by engineer Gustave Eiffel's company."
)
```
```python
status = 'answer'
nq = None
ans = "The Eiffel Tower was completed in 1889 and designed by engineer Gustave Eiffel's company."

trace = trace_so_far + [{'iter': 2, 'decision': 'answer', 'next_query': None}]

return {'iteration': 2, 'status': 'answer', 'next_query': '', 'answer': ans, 'trace': trace}
```
`should_continue` sees `status == 'answer'` → returns `END`. Loop stops.
---
Final State
```python
{
    'answer': "The Eiffel Tower was completed in 1889 and designed by engineer Gustave Eiffel's company.",
    'iteration': 2,
    'trace': [
        {'iter': 1, 'decision': 'need_more', 'next_query': 'who was the engineer or architect...'},
        {'iter': 2, 'decision': 'answer', 'next_query': None},
    ],
    ...
}
```
---
Key Takeaway
Every `structured_llm.invoke(...)` call returns one `ReasonDecision` object — not raw text, not a JSON string. You access `.status`, `.next_query`, `.answer` as real Python attributes, already validated against the schema's `Literal` types. The node's job each time is just to unpack that object into the flat dict shape `LoopState` expects, plus manually append to `trace` (since there's no reducer doing that automatically for plain `TypedDict` fields, unlike `MessagesState`'s `add_messages`).