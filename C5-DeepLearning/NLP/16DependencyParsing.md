# Dependency Parsing

Dependency parsing identifies **direct relationships between words** in a sentence. Each word (except the root) has a single **head** (the word it depends on).

```
"The cat chased the mouse"

chased (root)
   ├── cat (subject)
   │     └── The (determiner)
   └── mouse (object)
         └── the (determiner)
```

Each arrow shows: this word **depends on** that head.

---

## Core Idea

```
A sentence is a network of word-to-word dependencies.
Each word has one head (parent) and possibly multiple dependents.
The root (typically the main verb) has no head.
```

This is the **dependency** view of grammar — alternative to constituency (phrase-structure).

---

## Visual Representation

```
                 chased
                /      \
            (subj)    (obj)
              /          \
            cat          mouse
            |              |
          (det)          (det)
            |              |
           The            the
```

Or as a flat list of (head, dependent, relation) triples:

```
chased → cat    nsubj   (nominal subject)
cat    → The   det     (determiner)
chased → mouse  dobj    (direct object)
mouse  → the   det     (determiner)
```

---

## Common Dependency Relations

| Relation | Meaning | Example |
|----------|---------|---------|
| `nsubj` | Nominal subject | "cat" is subject of "chased" |
| `dobj` | Direct object | "mouse" is object of "chased" |
| `det` | Determiner | "the" depends on "cat" |
| `amod` | Adjective modifier | "big" depends on "cat" |
| `prep` | Preposition | "with" depends on "saw" |
| `pobj` | Object of preposition | "telescope" depends on "with" |
| `aux` | Auxiliary verb | "is" depends on "running" |
| `ROOT` | Root of the tree | usually the main verb |
| `conj` | Conjunction | "and" connects two NPs |

---

## Constituency vs Dependency

| Aspect | Constituency | Dependency |
|--------|--------------|------------|
| **Focus** | Phrase structure | Word-to-word relations |
| **Output** | Tree with phrase nodes | Tree with words as nodes |
| **Captures** | Hierarchical grouping | Grammatical roles |
| **Grammar basis** | CFG / PCFG | Dependency grammar |
| **Best for** | Phrase-level analysis | Relation extraction, multilingual NLP |
| **Visualisation** | Brackets, trees | Arrows between words |

Example same sentence:

```
"The cat chased the mouse"

Constituency:               Dependency:
S                            chased (ROOT)
├── NP (The cat)             ├── cat (nsubj)
│   ├── DT (The)             │   └── The (det)
│   └── N (cat)              └── mouse (dobj)
└── VP                           └── the (det)
    ├── V (chased)
    └── NP (the mouse)
        ├── DT (the)
        └── N (mouse)
```

Both describe the same sentence, just differently.

---

## How Dependency Parsing Works

### Two main approaches

```
Transition-based:
   - Process the sentence left-to-right
   - At each step, decide: SHIFT or REDUCE
   - Build dependencies incrementally
   - Fast, used in real-time parsers (spaCy, Stanford)

Graph-based:
   - Score every possible (head, dependent) pair
   - Find the maximum-spanning tree
   - More accurate, slower
```

Modern parsers use **neural networks** for the scoring/decision steps.

---

## Types of Dependency Parsers

| Type | Approach | Tools |
|------|----------|-------|
| Rule-based | Hand-written rules | Old-school, limited coverage |
| Transition-based | Greedy decisions, action sequence | spaCy, Stanford |
| Graph-based | Score and search for best tree | Maximum spanning tree algorithms |
| Neural | Deep learning | Almost all modern parsers |

---

## Advantages

```
✓ Compact representation — one node per word
✓ Captures grammatical roles directly (subject, object, modifier)
✓ Naturally handles long-distance dependencies
✓ Easier to use for downstream tasks like relation extraction
✓ Works well across languages with different syntactic structures
✓ Doesn't depend on assumed phrase categories
```

---

## Limitations

```
✗ Interpretability requires linguistic expertise to read fine relations
✗ Some constructions don't fit naturally (coordination, gaps)
✗ Choice of dependency labels can vary across frameworks
✗ Cross-lingual: dependency conventions differ between languages
```

---

## spaCy Example

```python
import spacy
nlp = spacy.load('en_core_web_sm')

doc = nlp("The cat chased the mouse")

for token in doc:
    print(f"{token.text:>10}  →  head: {token.head.text:<10} relation: {token.dep_}")
```

Output:

```
       The  →  head: cat        relation: det
       cat  →  head: chased     relation: nsubj
    chased  →  head: chased     relation: ROOT
       the  →  head: mouse      relation: det
     mouse  →  head: chased     relation: dobj
```

To visualise:

```python
spacy.displacy.serve(doc, style='dep')
```

---

## Applications

| Application | How dependency parsing helps |
|-------------|------------------------------|
| Information extraction | Find (subject, verb, object) triples |
| Question answering | Identify which word is the question subject |
| Relation extraction | "A → relation → B" matches dependency arcs |
| Sentiment analysis | Link opinions to specific aspects |
| Machine translation | Cross-lingual structure mapping |
| Summarisation | Identify key word relationships |

Example: relation extraction

```
"Apple acquired Beats for $3 billion"

Dependency arcs:
   acquired → Apple   (nsubj — subject)
   acquired → Beats   (dobj — object)
   acquired → for $3 billion  (preposition)

→ Triple: (Apple, acquired, Beats)
```

This is much harder with constituency parsing alone.

---

## When to Use Constituency vs Dependency

```
Use Constituency when:
   ✓ Need phrase-level analysis (NP, VP, PP)
   ✓ Working with CFGs / formal grammar
   ✓ Compiler / structured text parsing

Use Dependency when:
   ✓ Need word-level relations (subject, object, modifier)
   ✓ Information extraction
   ✓ Cross-lingual NLP
   ✓ Want compact representation
```

In practice, **dependency parsing has become the more common choice** in modern NLP because of its compactness and direct usefulness for downstream tasks.

---

## Summary

```
Dependency parsing = identify head-dependent relations between words

Each word has one head; arcs labelled with relations (nsubj, dobj, det, ...).

Approaches:
   Transition-based  → greedy, fast (spaCy, Stanford)
   Graph-based       → accurate, slower
   Neural            → state-of-the-art today

Strengths:    compact, captures grammatical roles, works cross-lingually
Weaknesses:   needs expertise to interpret, labels vary by framework
```

> Dependency parsing is the modern NLP workhorse for syntactic analysis. It captures who-did-what-to-whom directly — making it the go-to tool for relation extraction and many downstream tasks.
