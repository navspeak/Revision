# Spelling Correction

Detecting and fixing misspellings — essential for processing real-world text (typos, OCR errors, transcription mistakes).

```
"recieve" → "receive"
"definately" → "definitely"
"thier" → "their"
```

Two foundational techniques:

```
Edit Distance       → measure similarity between strings
Noisy Channel Model → probabilistic correction using a language model
```

---

## Edit Distance — Measuring Similarity

The **Levenshtein distance** is the minimum number of single-character operations (insert, delete, substitute) to transform one string into another.

```
"kitten" → "sitting"
   k → s   (substitution)
   t → t
   t → t
   e → i   (substitution)
   n → n
   insert 'g'
Edit distance = 3
```

### Operations

| Operation | Example |
|-----------|---------|
| Insert | "cat" → "cart" (insert 'r') |
| Delete | "cart" → "cat" (delete 'r') |
| Substitute | "cat" → "bat" (swap 'c' → 'b') |
| (Transpose) | "form" → "from" (swap adjacent) — Damerau-Levenshtein only |

### Calculation example

```
"form" → "from"
   f → f
   o → r   substitution
   r → o   substitution
   m → m
Distance = 2

Damerau-Levenshtein (allows transposition):
   "form" → "from" by transposing 'o' and 'r'
Distance = 1
```

---

## Using Edit Distance for Correction

Find dictionary words within edit distance ≤ k of the misspelled word:

```
"recieve" → candidates within edit distance 1:
   "receive"  ✓ (transpose i and e)
   "reckive"  (not a real word)
   "racieve"  (not a real word)
```

The valid candidate becomes the correction.

### Limitation

Many misspellings have **multiple plausible corrections**:

```
"acress" → "actress"? "across"? "access"? "cress"?
```

Pure edit distance can't decide. We need **context** — enter the noisy channel model.

---

## Noisy Channel Model

Treats spelling errors as **noise** introduced into the original (correct) word during transmission.

```
Intended word w  →  noisy channel  →  observed (misspelled) word x
```

Goal: recover the most likely original `w` given the observation `x`.

### Bayes' theorem

```
P(w | x) ∝ P(x | w) × P(w)

P(x | w)  → probability of mistyping w as x          (channel model)
P(w)      → probability of word w in language          (language model)
```

We pick the `w` that maximises this product.

---

## The Two Components

### Language Model — P(w)

How likely is the candidate word in general English?

```
Built from a large text corpus.
Common words → higher probability
Rare words   → lower probability

P("receive")  = 0.0001
P("recyclate") = 0.0000001
```

This prefers **common, real words**.

### Channel Model — P(x | w)

How likely is `x` to be a typo for `w`?

```
Built from typo data (confusion matrices).
Common confusions:
   "ie" ↔ "ei"   (common transposition)
   "tion" ↔ "shun" (phonetic confusion)
   adjacent-key typos (q/w, a/s)

P("recieve" | "receive") = high (common ie/ei swap)
P("recieve" | "renounce") = low  (unrelated)
```

This captures **typical human typing errors**.

---

## Putting It Together

```
Observed:  "acress"

Candidates (edit distance 1):
   actress   P(x|w) high  × P(w) medium = 0.001
   across    P(x|w) high  × P(w) high   = 0.005   ← winner
   access    P(x|w) low   × P(w) high   = 0.0008
   cress     P(x|w) low   × P(w) low    = 0.00001

Correction: "across"
```

The combination of error likelihood AND word likelihood resolves the ambiguity.

---

## Implementation Intuition

```
1. Build a vocabulary with word frequencies (language model)
2. Build a confusion matrix from typo data (channel model)
3. For each misspelled word x:
      a. Find all candidates w within edit distance ≤ 2
      b. Compute P(x|w) × P(w) for each
      c. Return the candidate with highest score
```

Modern systems (Google Search, autocomplete) use much more sophisticated models — neural networks trained on millions of correction pairs.

---

## Example

```
"thier"  → typo

Candidates within edit distance ≤ 2:
   "their"  P(x|w) = 0.3 (common ie/ei swap)  × P(w) = 0.01  = 0.003
   "thier"  not a word — skip
   "tier"   P(x|w) = 0.05 (h-removal)         × P(w) = 0.001 = 0.00005
   "thier"  exact match — but not a real word

Best correction: "their"
```

---

## Relationship to Edit Distance

```
Edit distance alone   → "all candidates within ≤ k operations"
Noisy channel         → "rank candidates by error probability × word probability"

Edit distance is the candidate generator.
Noisy channel is the ranker.

Together: effective spelling correction.
```

---

## Advantages

```
✓ Handles both real typos and OCR errors
✓ Probabilistic — gives confidence scores
✓ Combines lexicon and statistical knowledge
✓ Generalises to other "noise → original" tasks (speech recognition, OCR)
```

---

## Limitations

```
✗ Real-word errors not caught
   "I went to bare hands" — "bare" is a real word, but should be "bear"
   → needs CONTEXTUAL spell-checking, not just word-level

✗ Limited to short edit distances
   Larger distances → exponentially more candidates

✗ Doesn't handle word boundaries
   "thequick" → should be "the quick" — needs segmentation
```

Modern spell-checkers use **context** (surrounding words) and **neural models** to handle these.

---

## Modern Approaches

```
Traditional:    edit distance + noisy channel + dictionary
Contextual:     n-gram language models that consider neighbouring words
Neural:         deep learning models trained on (correct, incorrect) pairs
LLM-based:      GPT-style models can correct in context naturally
```

But the foundations are still **edit distance + probability** — the noisy channel principle remains.

---

## Summary

```
Spelling correction =
   Find candidates within edit distance
   Rank them by P(x|w) × P(w)
        = channel model × language model
   Pick the highest

Edit distance generates candidates.
Noisy channel model selects the best one.

Context and neural models extend this for state-of-the-art systems.
```

> Spelling correction was one of the earliest NLP applications — and the foundations of edit distance + Bayes still underpin modern systems.
