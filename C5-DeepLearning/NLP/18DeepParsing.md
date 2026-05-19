# Deep Parsing

**Deep parsing** combines syntactic structure with **semantic** and **morphological** information to produce a richer linguistic analysis than shallow parsing or constituency parsing alone.

```
Shallow parsing:       identify phrases (NP, VP, PP)
Constituency parsing:  build full phrase-structure trees
Deep parsing:          add semantic roles, morphology, agreement
```

Deep parsing tries to **understand**, not just **structure**.

---

## Core Concept

A deep parser extracts:

```
Syntactic structure  → who is the subject, object, etc.
Morphological info    → tense, number, person, case
Semantic roles        → agent, patient, instrument, location
Logical form          → underlying meaning representation
```

It's the bridge between **syntax** and **semantics**.

---

## Example

```
"The boy gave the girl a book in the library"

Shallow parser:
   [The boy]NP [gave]VP [the girl]NP [a book]NP [in the library]PP

Constituency parser:
   Full phrase-structure tree with NP, VP, PP nodes

Deep parser:
   Subject (agent):     The boy
   Verb:                gave (past tense)
   Recipient (goal):    the girl
   Object (theme):      a book
   Location:            in the library

   Semantic frame: GIVING(agent=boy, recipient=girl, theme=book, location=library)
```

The deep parse gives you **semantic roles** — what each phrase actually means in the action.

---

## What Deep Parsing Captures

| Aspect | Example |
|--------|---------|
| Syntactic role | "John" is subject, "the book" is object |
| Semantic role | "John" is the AGENT, "the book" is the THEME |
| Morphology | "gave" is past tense, "books" is plural |
| Agreement | "He runs" — "he" is third-person singular, agrees with verb form |
| Reference | "He gave it" — "it" refers to "the book" |
| Quantification | "All students passed" — universal quantifier |
| Negation | "He did not see her" — negation scope |

---

## Comparison with Other Parsing Levels

| Parsing Level | Output | Detail |
|---------------|--------|--------|
| Chunking | NP, VP, PP tags | Limited — phrases only |
| Constituency | Parse tree | Intermediate — structure but no semantics |
| Dependency | Head-dependent arcs | Word-level relations |
| Deep Parsing | Full semantic + syntactic representation | Most comprehensive |

---

## How Deep Parsing Works

```
1. POS Tagging          → assign categories to each word
2. Constituency/Dependency Parsing  → identify structure
3. Morphological Analysis  → identify tense, number, person
4. Semantic Role Labelling → assign semantic roles to phrases
5. Coreference Resolution  → link pronouns to referents
6. Compose Logical Form     → produce final meaning representation
```

Each step requires sophisticated models — deep parsing is computationally expensive.

---

## Output Representation

Deep parsing might output something like:

```
SENTENCE: "The boy gave the girl a book"

LOGICAL FORM:
   ∃e ∃b ∃g ∃k.
      EVENT(e, GIVING) ∧
      AGENT(e, b) ∧ BOY(b) ∧
      RECIPIENT(e, g) ∧ GIRL(g) ∧
      THEME(e, k) ∧ BOOK(k) ∧
      PAST(e)
```

Or in a feature-based representation:

```
{
   "predicate": "give",
   "tense": "past",
   "agent": {"text": "the boy", "definite": True, "number": "singular"},
   "recipient": {"text": "the girl", "definite": True, "number": "singular"},
   "theme": {"text": "a book", "definite": False, "number": "singular"}
}
```

---

## Advantages

```
✓ Captures meaning, not just structure
✓ Enables semantic search ("find sentences about giving books")
✓ Foundation for question answering, dialogue understanding
✓ Connects syntax to logical reasoning
✓ Useful for high-stakes domains (legal, medical) where precision matters
```

---

## Limitations

```
✗ Computationally expensive
✗ Hard to scale to large corpora
✗ Requires deep linguistic knowledge to build / tune
✗ Outperformed in practice by neural end-to-end systems for many tasks
✗ Each layer of analysis adds error propagation
```

---

## Applications

```
Question answering         → understand intent, identify answer phrases
Dialogue systems           → maintain semantic state across turns
Machine translation        → map meaning (not just words) across languages
Knowledge graph extraction → build structured knowledge from text
Legal document analysis    → precise interpretation needed
Semantic search            → match meaning, not just keywords
Logical inference          → derive new facts from text
```

---

## Modern Practice

Classical deep parsing was a major focus of pre-neural NLP. Modern approaches:

```
Neural language models (BERT, GPT):
   - Implicitly capture much of what deep parsers explicitly compute
   - Don't always produce explicit semantic structures
   - But can be probed for syntactic/semantic information

Semantic Role Labelling (SRL):
   - Modern neural systems do this well
   - Often a single step in a pipeline

Logic-based approaches:
   - Used in formal reasoning, less common in modern ML pipelines
   - Still relevant for high-precision domains
```

Deep parsing concepts inform modern systems even when they're not explicitly used.

---

## Why Deep Parsing Still Matters

```
1. Foundation: understanding deep parsing teaches you what NLP systems
              are actually trying to compute.

2. Diagnostics: when modern models fail, understanding semantic structure
              helps diagnose why.

3. Hybrid systems: production systems sometimes use deep parsing components
              for precision-critical tasks.

4. Interpretability: explicit structures are auditable, neural outputs are not.
```

---

## Summary

```
Deep parsing = full linguistic analysis combining
   syntax + morphology + semantic roles + (sometimes) logical form

Goes beyond constituency / dependency parsing
   to produce a meaning representation.

Slow, expensive, hard to scale
   but the conceptual foundation of "language understanding".

Modern neural models implicitly capture much of this,
   but explicit deep parsing remains useful for
   precision tasks and interpretability.
```

> Deep parsing is the most ambitious form of syntactic-semantic analysis. It's been largely displaced by neural models in everyday NLP, but it's where the field's understanding of language was forged.
