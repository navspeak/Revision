# Context-Free Grammars (CFG)

A **formal system** for describing the syntactic structure of a language.

```
A CFG is a set of production rules that say how to build valid sentences.

S  → NP VP
NP → DT N
VP → V NP
```

Reads as: "A sentence S consists of a noun phrase NP followed by a verb phrase VP".

---

## Components of a CFG

| Symbol | Meaning | Example |
|--------|---------|---------|
| **Terminal** | Actual words | "the", "cat", "ran" |
| **Non-terminal** | Phrase categories | NP, VP, S, DT, N, V |
| **Production rule** | How to expand non-terminals | NP → DT N |
| **Start symbol** | Root of the parse | usually S (sentence) |

---

## Example Grammar

```
S  → NP VP                ← sentence = NP + VP
NP → DT N | DT JJ N | NP PP   ← NP variants
VP → V NP | V NP PP       ← VP variants
PP → P NP                  ← prepositional phrase
DT → "the" | "a"
N  → "cat" | "dog" | "mat" | "telescope"
JJ → "big" | "red"
V  → "saw" | "chased" | "sat"
P  → "on" | "with"
```

This grammar can generate sentences like:

```
"The cat sat on the mat"
"A big dog chased the cat"
"The cat saw the dog with the telescope"
```

---

## Parse Tree Representation

For "The cat sat on the mat":

```
                  S
                /   \
              NP     VP
             /  \   /  \
            DT   N  V   PP
            |    |  |   /  \
           the  cat sat P   NP
                         |  /  \
                         on DT  N
                            |   |
                           the  mat
```

Each branch shows how a rule was applied. Reading bottom-up gives the original sentence.

---

## Symbol Types

| Type | Represents | Example |
|------|-----------|---------|
| **Non-terminal** | Categories (can be expanded further) | S, NP, VP |
| **Terminal** | Actual words (cannot be expanded) | "cat", "the" |
| **Start symbol** | Root of derivation | S |
| **Production** | A rule | NP → DT N |

---

## Why CFGs Matter in NLP

```
✓ Formal foundation of syntax — explains how sentences are built
✓ Enables parsing — can check if a sentence is grammatical
✓ Captures phrase structure — useful for downstream tasks
✓ Foundation for constituency parsing
✓ Used in compilers, query parsers, machine translation
```

---

## Generating vs Parsing

CFGs can be used in two directions:

### Generating (top-down)

Start with S and apply rules to produce a sentence.

```
S
→ NP VP
→ DT N VP
→ the N VP
→ the cat VP
→ the cat V NP
→ the cat sat NP    (wait — "sat" doesn't take NP — adjust rule)
```

### Parsing (bottom-up or top-down)

Given a sentence, find the rule sequence that produced it.

```
"the cat sat on the mat"
↓
the/DT cat/N sat/V on/P the/DT mat/N
↓
DT N  → NP    (the cat)
DT N  → NP    (the mat)
P NP  → PP    (on the mat)
V PP  → VP    (sat on the mat)
NP VP → S
```

Parsing is the harder direction and is what most NLP applications need.

---

## Ambiguity

A grammar is **ambiguous** if the same sentence has multiple valid parse trees:

```
"I saw the man with the telescope"

Parse 1: I [saw [the man] [with the telescope]]
         (I used the telescope to see the man)

Parse 2: I [saw [the man with the telescope]]
         (I saw a man who had a telescope)
```

Both are syntactically valid under the same grammar. Resolving ambiguity requires:
- Semantic knowledge
- Statistical preferences (which parse is more common)
- Context

---

## Applications

| Application | Role of CFG |
|-------------|-------------|
| Constituency parsing | Identify phrase structure |
| Grammar checking | Verify grammatical validity |
| Programming language compilers | Parse code (CFGs are everywhere here) |
| Query parsing | Interpret structured search queries |
| Machine translation | Map syntactic structure between languages |
| Speech recognition | Constrain output to grammatical sentences |

---

## Advantages

```
✓ Formal and well-understood
✓ Captures recursive structure of language
✓ Foundation for parsing algorithms (CYK, Earley, Chart)
✓ Generalises to programming languages too
```

---

## Limitations

```
✗ Coverage: real language has many exceptions
✗ Ambiguity is rampant in natural language
✗ Doesn't capture meaning or context
✗ Doesn't handle long-distance dependencies well
✗ Manually-crafted grammars don't scale
✗ Cross-lingual coverage requires separate grammars
```

This is why modern NLP often uses **probabilistic CFGs (PCFGs)** or **neural parsers** that learn structure from data instead of relying on hand-crafted rules.

---

## Probabilistic CFG (PCFG)

Add probabilities to each production rule:

```
S  → NP VP    (1.0)
NP → DT N     (0.6)
NP → DT JJ N  (0.3)
NP → NP PP    (0.1)
```

Now ambiguous sentences can be resolved by picking the **most likely** parse:

```
"I saw the man with the telescope"
   Parse 1 probability = 0.0023
   Parse 2 probability = 0.0008
   → choose Parse 1
```

PCFGs combine CFGs with statistical inference. The basis of much of classical parsing.

---

## Summary

```
CFG = production rules that describe sentence structure

Components:
   Terminals     → actual words
   Non-terminals → phrase categories (S, NP, VP)
   Rules         → how categories expand
   Start symbol  → usually S

Used for:
   Parsing (find structure of a sentence)
   Generation (produce valid sentences)

Limitations:
   Ambiguity, coverage, no semantics
   → modern NLP uses PCFGs or neural parsers
```

> CFGs are the formal backbone of syntax. They feel old-school but remain the conceptual foundation for parsing — whether you're using a classical CYK algorithm or a modern Transformer.
