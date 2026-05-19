# Constituency Parsing

Constituency parsing identifies **phrase-level structure** — groups words into nested phrases like NP, VP, PP — using a CFG.

```
"The cat chased the mouse"

S
├── NP (The cat)
│   ├── DT (The)
│   └── N (cat)
└── VP (chased the mouse)
    ├── V (chased)
    └── NP (the mouse)
        ├── DT (the)
        └── N (mouse)
```

Each **constituent** is a phrase that can be treated as a syntactic unit.

---

## Core Idea

```
A sentence is recursively composed of phrases.
Constituency parsing finds this composition.

Each subtree = one syntactic constituent.
```

This is the **phrase-structure** view of grammar, based on CFGs.

---

## Example

```
"The cat saw the dog with the telescope"

S
├── NP
│   ├── DT (The)
│   └── N (cat)
└── VP
    ├── V (saw)
    ├── NP
    │   ├── DT (the)
    │   └── N (dog)
    └── PP
        ├── P (with)
        └── NP
            ├── DT (the)
            └── N (telescope)
```

This is one valid parse — there's also another with PP attached to NP "the dog with the telescope" (ambiguity).

---

## Common Constituent Types

| Constituent | Meaning | Example |
|-------------|---------|---------|
| S | Sentence | "She runs fast" |
| NP | Noun Phrase | "the big cat" |
| VP | Verb Phrase | "ran quickly" |
| PP | Prepositional Phrase | "with a telescope" |
| ADJP | Adjective Phrase | "very tall" |
| ADVP | Adverb Phrase | "quickly enough" |

---

## How Constituency Parsing Works

```
1. Apply CFG rules to find rule sequences that derive the sentence.
2. Build a tree where each internal node is a non-terminal (NP, VP, etc.).
3. Output the tree.

Classical algorithms:
   CYK (Cocke-Younger-Kasami)   → dynamic programming
   Earley parser                  → incremental top-down
   Chart parser                  → bottom-up with caching
```

Modern parsers use **probabilistic CFGs (PCFGs)** or **neural networks**.

---

## Ambiguity in Constituency Parsing

Many sentences have multiple valid parse trees:

```
"I saw the man with the telescope"

Parse A:                          Parse B:
    NP attaches to VP                NP "the man with the telescope" is one NP
    (I used the telescope)           (the man had the telescope)
```

This is called **attachment ambiguity** — does the PP attach to the NP or the VP?

Resolving:
- Use statistical preferences (PCFG)
- Use semantic context
- Use modern neural parsers

---

## Advantages

```
✓ Captures hierarchical phrase structure
✓ Foundational concept in linguistics and NLP
✓ Useful for tasks needing phrase-level analysis:
   - Translation (match phrases across languages)
   - Information extraction (identify subject NPs)
   - Question answering (find answer phrases)
```

---

## Limitations

| Aspect | Challenge |
|--------|-----------|
| Coverage | Real language has constructions CFG can't easily handle |
| Ambiguity | Multiple valid parses for the same sentence |
| Long sentences | Tree depth grows; algorithms get slow |
| Discontinuous constituents | "He picked the book up" — "up" belongs to the verb but appears later |
| Cross-lingual | Different languages have very different phrase structures |

---

## Constituency Parsing in Practice

### NLTK (with rule-based grammar)

```python
import nltk

grammar = nltk.CFG.fromstring("""
    S -> NP VP
    NP -> Det N | Det N PP
    VP -> V NP | V NP PP
    PP -> P NP
    Det -> 'the' | 'a'
    N -> 'cat' | 'dog' | 'telescope' | 'park'
    V -> 'saw' | 'chased'
    P -> 'with' | 'in'
""")

sent = "the cat saw the dog with the telescope".split()
parser = nltk.ChartParser(grammar)
for tree in parser.parse(sent):
    print(tree)
    tree.pretty_print()
```

### spaCy (neural parser)

```python
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp("The cat chased the mouse")
# Note: spaCy primarily uses dependency parsing, but extensions provide constituency
```

### Stanford CoreNLP / Berkeley parser

Industrial-strength constituency parsers using neural models.

---

## Applications

| Application | How constituency parsing helps |
|-------------|--------------------------------|
| Machine translation | Map NPs and VPs between languages |
| Grammar checking | Verify well-formed phrase structure |
| Information extraction | Identify entity NPs |
| Question answering | Locate candidate answer phrases |
| Summarisation | Compress at phrase level |
| Sentiment | Analyse opinion-bearing phrases |

---

## Constituency vs Dependency

Two different views of syntax:

```
Constituency: focuses on PHRASES
   "[The big cat] [chased [the mouse]]"

Dependency:   focuses on WORD-TO-WORD RELATIONS
   "chased" → subject: "cat", object: "mouse", modifier: "big"
```

Constituency is detailed in this file. Dependency is in `16DependencyParsing.md`.

---

## Summary

```
Constituency parsing = build phrase-structure tree from a sentence

Based on Context-Free Grammars (CFGs).
Captures hierarchical phrase structure: NP, VP, PP, etc.

Strengths:    interpretable, foundational, phrase-level analysis
Weaknesses:   ambiguity, coverage, computationally expensive

Modern approach: probabilistic / neural constituency parsers.
```

> Constituency parsing reveals the syntactic skeleton of a sentence — phrases nested inside phrases. It's the foundation of much of classical NLP.
