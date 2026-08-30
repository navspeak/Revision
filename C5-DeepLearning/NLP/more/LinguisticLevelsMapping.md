# Mapping NLP Tasks to Linguistic Levels

The notebook `NLP_basics.ipynb` demonstrates **Tokenization**, **POS tagging**, **NER**, and **WSD**.
Here is how those four tasks line up against the classical linguistic levels
(see `../3LinguisticLevels.md`).

## The five linguistic levels

```
Phonology    → sound patterns
Morphology   → word structure
Syntax       → sentence structure
Semantics    → meaning
Pragmatics   → context and intent
```

## Where each task lives

| Level         | What it studies                                | Our task(s)                                                                 |
|---------------|------------------------------------------------|-----------------------------------------------------------------------------|
| Phonology     | Sound patterns                                 | none — we work with text, not audio                                         |
| Morphology    | Word structure (prefixes, suffixes, inflection) | **Tokenization** (word boundaries); **Lemmatization** (`apples → apple`)    |
| Syntax        | Sentence structure, grammar                    | **POS tagging** (each token's grammatical role)                             |
| Semantics     | Meaning of words and phrases                   | **NER** (what does this word refer to?); **WSD** (which meaning is active?) |
| Pragmatics    | Context, intent, speaker beliefs               | none — WSD only touches the edge of this                                    |

## Visual: where each task sits on the stack

```
Phonology      (sound)         — skipped (text input)
   │
Morphology     (word form)     ← Tokenization, Lemmatization
   │
Syntax         (grammar)       ← POS tagging
   │
Semantics      (meaning)       ← NER, WSD
   │
Pragmatics     (intent)        — skipped
```

## Why each task sits where it does

- **Tokenization → Morphology.**
  Deciding *"don't"* is one token or two (`do` + `n't`) is a morphology question — it's
  about how words are constructed and where their boundaries are.

- **POS tagging → Syntax** (with morphology hints).
  The tagger uses morphological clues like `-ing`, `-ed`, `-ly` to make a syntactic
  decision: *what is this word's grammatical role in the sentence?*

- **NER → Semantics.**
  "Monday" is a `DATE` because of what it *means*, not how it's spelled or where it
  sits grammatically. NER is referential meaning.

- **WSD → Semantics** (leaning toward Pragmatics).
  Picking *bank-river* vs *bank-financial* is a meaning choice driven by surrounding
  context. Lesk operates over definitions (semantic content) but uses context — which
  is the entryway to pragmatics.

## What we did *not* cover

If you wanted to fill in the gaps:

- **Phonology** → speech-to-text, phoneme recognition, rhyme/syllable analysis
- **Pragmatics** → sentiment + sarcasm detection, coreference resolution,
  dialogue act classification, implicature, intent classification
  ("book me a flight" → `BookFlight` intent)

## TL;DR

> **Tokenization** lives in Morphology, **POS** in Syntax, **NER** and **WSD** in
> Semantics. The notebook climbs the first three layers of the linguistic stack —
> it skips Phonology (text, not sound) and Pragmatics (no intent modelling).
