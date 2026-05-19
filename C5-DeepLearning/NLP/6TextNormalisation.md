# Text Normalisation

Standardising text so that **superficial variations don't affect downstream analysis**.

```
"Apple"  vs  "apple"   → same word, different cases
"don't"  vs  "do not"  → same meaning, different forms
"colour" vs  "color"   → same word, different spellings

Normalisation puts them all in a consistent form.
```

---

## Why It Matters

```
Without normalisation:
   "Apple", "apple", "APPLE" → treated as 3 different words
   → vocabulary explodes
   → statistical models miss patterns

With normalisation:
   All three → "apple"
   → cleaner, smaller vocabulary
   → models work better with less data
```

It's a foundational preprocessing step — almost every NLP pipeline includes it.

---

## Key Operations

### 1. Case Conversion

```
"Apple is great" → "apple is great"
```

✓ Reduces vocabulary size
⚠ But sometimes case matters:
- "US" (United States) ≠ "us" (pronoun)
- "Apple" (company) ≠ "apple" (fruit)

Solution: lowercase **selectively**, or use case-aware models.

### 2. Symbol Handling

Remove or normalise punctuation:

```
"Hello, world!" → "hello world"
```

When to keep punctuation:
- Sentence boundary detection
- Sentiment ("!!!" or "?!" carry meaning)
- URLs, emails

When to drop:
- Bag-of-words style features
- Stemming

### 3. Number Standardisation

Bring numeric mentions to a consistent form:

```
"twenty-five", "25", "twenty five"   → all → "25" or all → "twenty-five"
```

Useful for entity recognition and search.

### 4. Contraction Expansion

```
"don't"   → "do not"
"won't"   → "will not"
"I'll"    → "I will"
"they're" → "they are"
```

Especially important for:
- Sentiment analysis (negations matter)
- Search and retrieval
- Statistical features

### 5. Stopword Removal

Remove common low-information words like "the", "is", "at":

```
"The cat is on the mat" → "cat mat"
```

Covered separately in `8StopwordRemoval.md`.

### 6. Encoding and Whitespace Fixes

```
Multiple spaces        → single space
Tabs and newlines      → standardised
UTF-8 corruption       → cleaned (e.g. "café" not "cafÃ©")
Trailing spaces        → stripped
```

These are mundane but essential — most data has them.

---

## Advanced Normalisation Tasks

### Diacritic and accent removal

```
"café"   → "cafe"
"naïve"  → "naive"
```

Useful for matching across cultural variants but loses some information.

### Slang and abbreviation expansion

```
"u r"   → "you are"
"asap"  → "as soon as possible"
"lol"   → "laughing out loud" or removed depending on context
```

Critical for social media analysis.

### Spelling correction

```
"recieve"  → "receive"
"definately" → "definitely"
```

Covered in `10SpellingCorrection.md`.

---

## Illustrative Example

Raw input:

```
"OMG!! The cafe was AWESOME!!! 🎉 Loved it... I'll definitely visit again."
```

After normalisation:

```
"omg the cafe was awesome loved it i will definitely visit again"
```

What happened:
- Lowercased
- Removed punctuation and emoji
- Expanded "I'll" → "I will"
- Diacritic removed from "café"

Now ready for tokenisation and downstream processing.

---

## Why It Matters

```
Reduces vocabulary size:
   Without normalisation: 50,000 unique tokens
   After normalisation:   30,000 unique tokens
   → smaller models, faster training

Reduces sparsity:
   Without: "Apple", "apple", "APPLE" each appear rarely
   With:    "apple" appears 3× more often
   → statistical models work better

Catches lexical variation:
   "color" / "colour" / "colour-co-ordinated" → all map to "colour"
```

---

## Things to Watch Out For

```
✗ Don't lowercase when case matters (entities, codes)
✗ Don't strip punctuation when it carries sentiment
✗ Don't remove negations during stopword removal
✗ Don't over-normalise domain-specific terms (medical, legal)
✗ Be careful with non-English text — diacritics may carry meaning
```

Normalisation isn't free — it's a trade-off between coverage and fidelity.

---

## Summary

```
Normalisation = remove superficial variation
                so that downstream models see consistent text

Operations:
   Case conversion         → "Apple" → "apple"
   Punctuation handling    → "Hi!" → "Hi"
   Contraction expansion   → "don't" → "do not"
   Number standardisation  → "25" / "twenty-five" → unified
   Encoding / whitespace   → strip noise
   Slang / typos           → "u r" → "you are"
```

> Normalisation is mundane but foundational. Skipping it → vocabulary explosion and worse models.
