# Morphological Analysis

The study of **word structure** — how words are formed from smaller meaning-bearing units called **morphemes**.

```
"unhappiness" = un + happy + ness
                 (prefix) (root) (suffix)
```

Morphological analysis helps NLP systems recognise that related word forms share meaning.

---

## Why It Matters

Without morphology:

```
"run", "runs", "ran", "running"  → treated as 4 unrelated words
```

With morphology:

```
All four → same root "run"
   → smaller vocabulary, better generalisation
```

This is the foundation for stemming, lemmatisation, and modern subword tokenisation.

---

## Morphemes

The **smallest meaningful units** in language. Two main types:

### Free morphemes

Can stand alone as words.

```
"happy"      → free morpheme
"book"       → free morpheme
"run"        → free morpheme
```

### Bound morphemes

Must attach to another morpheme.

```
"-ness"   → bound (must attach: happi+ness)
"un-"     → bound (must attach: un+happy)
"-ed"     → bound (past tense suffix)
"-ing"    → bound (gerund / present participle)
"-s"      → bound (plural)
```

---

## Types of Bound Morphemes

### Inflectional morphemes

Modify a word's grammatical form **without** changing its core meaning or part of speech:

```
"cat" → "cats"       (singular → plural, still a noun)
"walk" → "walked"    (present → past, still a verb)
"big" → "bigger"     (positive → comparative, still an adjective)
```

English has only ~8 inflectional morphemes — limited inventory.

### Derivational morphemes

Create **new words**, often changing the part of speech:

```
"happy" (adj) → "happiness" (noun)       suffix "-ness"
"teach" (verb) → "teacher" (noun)        suffix "-er"
"act" (verb) → "active" (adj)            suffix "-ive"
"pre" + "view" → "preview" (verb)        prefix "pre-"
```

English has many derivational morphemes — much more productive.

---

## Examples of Word Formation

| Word | Breakdown | Meaning |
|------|-----------|---------|
| unhappiness | un + happy + ness | state of not being happy |
| disagreement | dis + agree + ment | state of not agreeing |
| readable | read + able | capable of being read |
| nationalisation | nation + al + ise + ation | act of making into a nation's property |
| preview | pre + view | view beforehand |

---

## Functions in NLP

Morphological analysis helps with:

```
1. Reduce vocabulary
   "run", "runs", "ran", "running" → all map to "run"

2. Handle out-of-vocabulary words
   Unknown word "preview" → recognise "pre" + "view"

3. Inflection-aware tasks
   Tense matters for translation, summarisation, question answering

4. Cross-lingual NLP
   Morphologically rich languages (Turkish, Finnish, Arabic)
   one word may encode tense, person, number, case → need analysis

5. Better embeddings
   Words sharing roots get related vector representations
```

---

## Computational Perspective

A morphological analyser produces:

```
Input:   "running"
Output:  { root: "run", inflection: "-ing", POS: verb, tense: present_participle }

Input:   "unhappiness"
Output:  { root: "happy", prefix: "un-", suffix: "-ness",
           POS: noun, sentiment_polarity: negated }
```

Two main computational approaches:

### Rule-based morphology

Use known affix patterns:

```
If word ends in "-ing" → strip "-ing", remaining is verb stem
If word ends in "-ness" → strip "-ness", remaining is adjective
```

Used by stemmers like Porter.

### Statistical / Neural morphology

Learn affix patterns from data:

```
BPE / WordPiece tokenisers learn subword units
   that correspond to morphemes for many words
```

Used by modern transformers.

---

## Example Workflow

Input: "unhappiness"

```
1. Recognise possible boundaries
   un|happi|ness
   un|happiness
   unhappy|ness

2. Match against known morphemes
   un-       (negation prefix)        ✓
   happi-   (related to "happy")      ✓
   -ness     (state-of suffix)        ✓

3. Output morphological structure
   Root: happy
   Affixes: un- (prefix), -ness (suffix)
   POS: noun
   Sentiment: derived from "happy" but negated
```

---

## Applications

| Application | How morphology helps |
|-------------|---------------------|
| Machine translation | Preserve tense and agreement across languages |
| Text-to-speech | Pronounce derived forms correctly |
| Information retrieval | Match "runs", "running" to query "run" |
| Sentiment analysis | Recognise "unhappy" as negation of "happy" |
| Stemming / Lemmatisation | Reduce inflected forms to base form |
| Cross-lingual transfer | Compare related forms in different languages |

---

## Languages Vary Greatly

```
English:        moderate morphology — small inflection set
                "cat" / "cats"

Turkish:        agglutinative — many morphemes per word
                "evlerimizdeydiler" = "they were in our houses"
                (ev + ler + imiz + de + ydi + ler)

Chinese:        isolating — almost no inflection
                each word stands alone

Arabic:         templatic — non-concatenative morphology
                root k-t-b → kataba (he wrote), kitab (book)
```

NLP for morphologically rich languages needs specialised tools.

---

## Summary

```
Morphemes = smallest meaning-bearing units
   Free:    stand alone (cat, happy, run)
   Bound:   must attach (un-, -ness, -ed, -ing)

Types:
   Inflectional → grammatical form, same POS (cats, walked)
   Derivational → new word, often new POS (happiness, teacher)

Morphological analysis in NLP:
   Reduces vocabulary, handles OOV, improves translation,
   essential for morphologically rich languages.
```

> Morphology connects related word forms. It's the foundation of stemming, lemmatisation, and modern subword tokenisers.
