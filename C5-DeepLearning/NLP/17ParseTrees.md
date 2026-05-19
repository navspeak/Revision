# Parse Trees vs Syntax Trees

Two related — but **not identical** — tree representations of sentence structure.

```
Parse Tree    → derivation tree showing rules applied (CFG-based)
Syntax Tree   → abstract structure showing grammatical roles
```

In casual NLP usage they're often conflated. Strictly, they serve different purposes.

---

## Parse Tree

A **parse tree** (or derivation tree) is the literal output of applying CFG rules to derive a sentence.

```
Sentence:  "The cat sat"

Rules applied:
   S → NP VP
   NP → DT N
   DT → 'The'
   N → 'cat'
   VP → V
   V → 'sat'

Parse tree:
                S
              /   \
            NP     VP
           /  \    |
          DT   N   V
          |    |   |
         The  cat sat
```

Every node represents either a non-terminal (S, NP, VP) or a terminal (the words). Reading bottom-up gives the original sentence.

### Purpose

```
Show HOW grammar rules generated the sentence.
Trace each rule application explicitly.
```

Used for:
- Verifying grammar correctness
- Parsing algorithm output
- Linguistic analysis at the rule level

---

## Syntax Tree

A **syntax tree** is a more **abstract** representation showing grammatical structure and roles — often without including all intermediate non-terminals.

```
Sentence:  "The cat sat"

Syntax tree (simplified):
                S
              /   \
           SUBJ   PRED
            |      |
           cat    sat
            |
          (det)
            |
           the
```

Some intermediate categories (like DT or NP) may be omitted in favour of grammatical roles (subject, predicate).

### Purpose

```
Show WHAT the grammatical roles are.
Highlight meaning-relevant structure.
```

Used for:
- Linguistic discussion
- Semantic mapping
- Visualisation that emphasises roles over rules

---

## Comparison

| Aspect | Parse Tree | Syntax Tree |
|--------|------------|-------------|
| **Source** | Rule application from CFG | Linguistic / semantic abstraction |
| **Structure** | Includes ALL intermediate non-terminals | May omit purely structural nodes |
| **Purpose** | Trace how grammar generates sentence | Show grammatical / semantic roles |
| **Used in** | Parsing algorithms, CFG validation | Linguistic analysis, visualisation |
| **Detail** | More verbose | Cleaner, more interpretive |

---

## Same Sentence — Both Views

```
"She gave the boy a book"

Parse tree (CFG-derived):
                  S
                /   \
              NP     VP
              |    / | \
              N   V  NP  NP
              |   |  |   |
              She gave DT N
                     /\
                    the boy
                            DT N
                            |  |
                            a book

Syntax tree (role-focused):
                  S
                / | \
              SUBJ V  OBJ-1   OBJ-2
              She  gave the boy a book
```

Same sentence, different representations — choose based on what you want to show.

---

## Relation Between the Two

The parse tree is more **rule-bound** and **mechanical**. The syntax tree is more **interpretive** — it's what a linguist would draw to explain meaning.

In practice for NLP:
- **Parser outputs** are usually parse trees
- **Downstream tasks** often use syntax trees or convert to dependency representations
- **Visualisations** prefer syntax trees for clarity

---

## Visualisation in NLTK

```python
import nltk

grammar = nltk.CFG.fromstring("""
    S -> NP VP
    NP -> Det N
    VP -> V NP
    Det -> 'the'
    N -> 'cat' | 'mouse'
    V -> 'chased'
""")

parser = nltk.ChartParser(grammar)
sent = "the cat chased the mouse".split()
for tree in parser.parse(sent):
    tree.pretty_print()
```

The output is a parse tree showing every rule application.

---

## Applications

| Tree Type | Used in |
|-----------|---------|
| Parse Tree | Algorithmic parsing, formal grammar validation, compiler design |
| Syntax Tree | Linguistic analysis, NLP textbook diagrams, semantic mapping |
| Dependency Tree | Modern NLP — most production systems prefer this |

---

## Advantages

```
✓ Both make sentence structure visible
✓ Useful for teaching and analysis
✓ Foundation for downstream syntactic features
```

## Limitations

```
✗ Hard to read for long sentences
✗ Ambiguity → multiple valid trees per sentence
✗ Difficult to display for complex sentences
✗ Modern deep learning models don't always produce explicit trees
```

---

## Modern Practice

In contemporary NLP:

```
Classical parsers (CYK, Earley, Chart):
   → output explicit parse trees

Modern neural parsers (transformer-based):
   → output dependency arcs or constituency trees as needed
   → trees can be derived but aren't the primary representation

LLMs (GPT, Claude):
   → don't explicitly compute trees but implicitly use syntactic knowledge
```

Trees remain useful conceptually — for understanding language structure — even if production systems don't always materialise them.

---

## Summary

```
Parse Tree   → derivation according to CFG rules
                shows HOW grammar built the sentence
                detailed, mechanical

Syntax Tree  → abstract structure showing grammatical roles
                shows WHAT the structure is
                cleaner, more interpretive

Both reveal sentence structure — pick based on whether you want
rule-by-rule derivation or grammatical role view.
```

> Parse tree = "the trail of rules used". Syntax tree = "the grammatical picture". Often used interchangeably in casual NLP, but the distinction matters in formal linguistics and parsing theory.
