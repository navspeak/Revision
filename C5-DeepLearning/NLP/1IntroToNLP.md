# Introduction to NLP

**Natural Language Processing** is a subfield of AI focused on the **computational modelling and analysis of human language**.

Goal: enable computers to **understand, interpret, and generate** natural language in a way that's meaningful and useful.

```
NLP = bridge between human communication and machine understanding
     = linguistics + computer science + machine learning
```

---

## Why NLP Is Hard

Human language is **ambiguous, context-dependent, and dynamic**.

### Lexical ambiguity

```
"bank" → financial institution OR side of a river
"light" → illumination OR not heavy
```

### Syntactic ambiguity

```
"I saw the man with the telescope"
   - I used the telescope to see the man
   - I saw the man who had the telescope
```

### Idiomatic expressions

```
"break the ice" → not literal — means starting a conversation
"piece of cake" → easy task
```

Humans resolve these effortlessly using **context and prior knowledge**. Computers need **explicit models** to do the same — that's the central challenge of NLP.

---

## Objectives of NLP

1. **Language Understanding** — extract and represent the meaning of linguistic input
2. **Language Generation** — produce coherent natural-language output from data
3. **Human–Computer Interaction** — communicate in everyday language, not programming commands

---

## The NLP Pipeline (Overview)

```
Raw Text
   ↓
Data Acquisition  → collect text/speech from sources
   ↓
Data Cleaning     → remove HTML, emojis, typos
   ↓
Preprocessing     → tokenise, normalise, stem/lemmatise
   ↓
Feature Extraction → BoW, TF-IDF, word embeddings
   ↓
Model Building    → logistic regression, neural networks
   ↓
Evaluation        → metrics, error analysis
   ↓
Deployment        → chatbots, translation, search
```

Detailed in `4NLPPipeline.md`.

---

## Two Paradigms

### Rule-Based Systems (early NLP)

```
Manually crafted grammatical and lexical rules
   → High precision in restricted domains
   → Limited scalability and adaptability
```

### Statistical / Data-Driven Systems (modern NLP)

```
Learn patterns from large corpora
   → Flexible, adapts to diverse contexts
   → Requires lots of data and compute
```

Modern NLP **combines both** — rules for interpretability, learning for robustness.

---

## Challenges

| Challenge | Example |
|-----------|---------|
| **Ambiguity** | Multiple interpretations at lexical / syntactic / semantic levels |
| **Context sensitivity** | Meaning depends on situation and discourse |
| **Idiomatic language** | Non-literal expressions resist rules |
| **Resource scarcity** | Few annotated corpora for low-resource languages |
| **Domain adaptation** | Models trained on news fail on medical text |

These motivate ongoing research in computational linguistics and machine learning.

---

## Summary

```
NLP enables computers to handle human language at scale.
Hard because language is ambiguous and context-dependent.
Modern NLP combines rule-based + statistical approaches.
Forms the backbone of search, translation, chatbots, voice assistants.
```

> The rest of this module is about how each stage of NLP works — from cleaning raw text to parsing complete sentences.
