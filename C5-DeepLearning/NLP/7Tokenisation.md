# Tokenisation

Splitting a text string into **tokens** — the basic units of analysis.

```
"Natural Language Processing is fascinating."
   ↓
['Natural', 'Language', 'Processing', 'is', 'fascinating', '.']
```

Tokens are usually **words**, but can also be **sentences**, **subwords**, or **characters**.

---

## Why It's Not Trivial

Looks simple — split on whitespace. But there are edge cases everywhere:

```
"don't"          → ['don', "'t"]  or  ["do", "n't"]  or  ["don't"] ?
"U.S.A."         → ['U.S.A.']  or  ['U', '.', 'S', '.', 'A', '.'] ?
"$3.14"          → ['$', '3.14']  or  ['$3.14'] ?
"New York"       → ['New', 'York']  or  ['New_York'] ?
"weren't"        → ['were', "n't"]
"https://x.com"  → keep as one token? or split?
"😀"             → one token? or skip?
```

How you handle these affects everything downstream.

---

## Levels of Tokenisation

### Word-level (most common)

```
"The quick brown fox" → ['The', 'quick', 'brown', 'fox']
```

Standard for most NLP tasks. Issue: rare and out-of-vocabulary (OOV) words get treated as unknown.

### Subword-level (modern)

Break unknown words into known subword units:

```
"unhappiness" → ['un', 'happi', 'ness']
"playing"     → ['play', 'ing']
```

Used by BPE, WordPiece (BERT), SentencePiece (T5). Handles OOV gracefully.

### Sentence-level

```
Paragraph: "I love NLP. It's amazing! What about you?"
   ↓
['I love NLP.', "It's amazing!", 'What about you?']
```

Used for document segmentation, sentence-level classification, sentence embeddings.

### Character-level

```
"hello" → ['h', 'e', 'l', 'l', 'o']
```

Useful for:
- Languages without clear word boundaries (Chinese, Japanese)
- Morphologically rich languages (Turkish, Finnish)
- Robustness to misspellings

But loses semantic structure — characters alone don't carry much meaning.

---

## Approaches to Tokenisation

### 1. Rule-based (whitespace + punctuation)

```python
text = "Hello, world!"
tokens = text.split()       # ['Hello,', 'world!']
# Strip punctuation
tokens = [t.strip(",.!?") for t in tokens]
# ['Hello', 'world']
```

Simple but breaks on contractions, hyphens, etc.

### 2. Regex-based

More precise control:

```python
import re
tokens = re.findall(r"\b\w+\b", text)
```

Still rule-based, but handles common patterns better.

### 3. Library-based (NLTK, spaCy)

```python
from nltk.tokenize import word_tokenize
word_tokenize("Don't go to the U.S.A.")
# ['Do', "n't", 'go', 'to', 'the', 'U.S.A.', '.']
```

Handles contractions, abbreviations, dates, URLs.

### 4. Learned / statistical (BPE, WordPiece)

For deep learning models:

```python
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
tokenizer.tokenize("unhappiness")
# ['un', '##happiness']
```

Subword tokenisation that handles any input without OOV issues.

---

## Challenges

### Contractions

```
"don't"   → "do" + "n't"  OR  "don" + "'t"
"I'll"    → "I" + "'ll"   OR  "I'll" as one
```

Different tokenisers make different choices — be consistent within your pipeline.

### Multi-word expressions

```
"New York"     → ['New', 'York']   loses the meaning
"kick the bucket" → idiomatic — tokenising loses idiom
```

Some tokenisers handle these as single tokens; others rely on later processing.

### Hyphens

```
"state-of-the-art" → ['state', 'of', 'the', 'art']  or  ['state-of-the-art']
"well-known"       → ditto
```

### Punctuation inside words

```
"U.S.A."   → ['U.S.A.']  or  ['U', 'S', 'A', '.']
"3.14"     → ['3.14']    or  ['3', '.', '14']
"twitter.com" → as a URL or as components?
```

### Languages without word boundaries

```
Chinese: 我喜欢自然语言处理   no spaces — need segmentation
Japanese: same — uses character-aware tokenisers
```

Word-level tokenisation doesn't apply here without specialised segmenters.

---

## Examples Across Tokenisers

Input: `"I can't go to New York; it's raining!"`

```
NLTK word_tokenize:
   ['I', 'ca', "n't", 'go', 'to', 'New', 'York', ';', 'it', "'s", 'raining', '!']

spaCy:
   ['I', 'ca', "n't", 'go', 'to', 'New', 'York', ';', 'it', "'s", 'raining', '!']

BERT WordPiece:
   ['i', 'can', "'", 't', 'go', 'to', 'new', 'york', ';', 'it', "'", 's', 'raining', '!']

Simple split + strip:
   ['I', "can't", 'go', 'to', 'New', 'York', "it's", 'raining']
```

Each makes different trade-offs — there's no single correct answer.

---

## Why Tokenisation Matters

```
Tokenisation defines what the model sees as a "word":
   - vocabulary size
   - OOV handling
   - sensitivity to surface variation
   - downstream features (n-grams, POS, parse)

A bad tokeniser → cascading errors throughout the pipeline.
```

Choose your tokeniser based on:
- Language
- Domain (medical, legal, social media)
- Downstream task
- Whether you're using a pretrained model (use its tokeniser!)

---

## Summary

```
Tokenisation = split text into analysable units

Levels:
   Word        → most common, standard
   Subword     → modern, handles OOV (BPE, WordPiece)
   Sentence    → segmenting paragraphs
   Character   → for some languages or robustness

Approaches:
   Rule-based  → whitespace, regex
   Library     → NLTK, spaCy
   Learned     → BPE, WordPiece (used by BERT, GPT)
```

> Tokenisation feels trivial but isn't. It's the foundation of everything that follows.
