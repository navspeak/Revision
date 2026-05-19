# Linguistic Levels in NLP

Human language operates on **five interdependent levels**. A comprehensive NLP system must address all of them.

```
Phonology    → sound patterns
Morphology   → word structure
Syntax       → sentence structure
Semantics    → meaning
Pragmatics   → context and intent
```

---

## 1. Phonology — Sound Patterns

How sounds form words. Concerned with **pronunciation**.

```
"Knight" and "night" → phonologically identical (both /naɪt/)
                       but morphologically and semantically different
```

### Relevance in NLP

- Speech recognition (sound → text)
- Text-to-speech synthesis (text → sound)
- Pronunciation in voice assistants

For pure text NLP, phonology matters less — but it's central for speech systems.

---

## 2. Morphology — Word Structure

How words are formed from **morphemes** (smallest meaning-bearing units).

```
un + happy + ness → unhappiness
prefix + root + suffix
```

### Types of morphemes

| Type | Example |
|------|---------|
| Free | "happy" (can stand alone) |
| Bound | "un-", "-ness" (must attach to another morpheme) |
| Inflectional | "-s" (plural), "-ed" (past tense) — doesn't change part of speech |
| Derivational | "-ness", "-er" — often changes part of speech |

### Why it matters in NLP

```
"run", "running", "ran"  → same lemma "run"
Without morphology       → treats them as 3 unrelated words
With morphology          → recognises shared root
```

Covered in detail in `9MorphologicalAnalysis.md`.

---

## 3. Syntax — Sentence Structure

How words combine into grammatical sentences. Order matters.

```
"The cat chased the dog"  → cat is subject, dog is object
"The dog chased the cat"  → dog is subject, cat is object

Same words, different meaning — syntax determines who-did-what.
```

### Tools in NLP

- **POS tagging** — assign part of speech to each word
- **Parsing** — extract sentence structure (constituency or dependency)
- **Grammar checking**

Covered in `12POSTagging.md`, `14CFG.md`, `15ConstituencyParsing.md`, `16DependencyParsing.md`.

---

## 4. Semantics — Meaning

The meaning of words and sentences.

```
"light" → illumination OR not heavy   (word-level ambiguity)

"I saw the man with the telescope"
   → I used a telescope to see him   OR
   → I saw a man holding a telescope  (sentence-level ambiguity)
```

### NLP tasks at semantic level

- Word sense disambiguation
- Semantic role labelling ("who did what to whom")
- Named entity recognition
- Sentiment analysis
- Question answering

Modern word embeddings (Word2Vec, GloVe, BERT) capture semantic similarity numerically.

---

## 5. Pragmatics — Context and Intent

Meaning beyond literal interpretation — what the speaker **intends**, not just what they **said**.

```
"Can you pass the salt?"
   Literal meaning  → asking about ability
   Intended meaning → polite request to pass the salt
```

Pragmatics covers:
- Implicature (what's implied but not said)
- Speech acts (requests, commands, questions)
- Discourse (how sentences connect across a conversation)
- Cultural and social context

### NLP tasks

- Conversational AI (chatbots, virtual assistants)
- Dialogue systems
- Sarcasm and intent detection

Pragmatics is the **hardest** level — humans use immense background knowledge that's difficult to encode.

---

## Interdependence

```
Lower levels feed upper levels:

Phonology   ↑
Morphology  ↑   → semantics depends on knowing which words are present
Syntax      ↑   → meaning depends on grammatical structure
Semantics   ↑   → pragmatic interpretation depends on literal meaning
Pragmatics      → highest level uses all of the above + context
```

A POS tagger needs morphology (suffixes signal part of speech).
A parser needs POS tags.
Sentiment analysis needs parsing to handle "not happy" vs "happy".
A chatbot needs all of the above to figure out user intent.

---

## Summary Table

| Level | Focus | Example |
|-------|-------|---------|
| Phonology | Sound | "knight" = "night" |
| Morphology | Word structure | un + happy + ness |
| Syntax | Sentence structure | Cat chases dog ≠ dog chases cat |
| Semantics | Meaning | "light" = lamp / not heavy |
| Pragmatics | Intent | "Can you pass the salt?" is a request |

> A robust NLP system must process all five levels — each contributes essential information.
