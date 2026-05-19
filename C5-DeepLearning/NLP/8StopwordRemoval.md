# Stopword Removal

Removing **common, low-information words** like "the", "is", "and" to focus on meaningful content.

```
"The cat is sitting on the mat"
   → ['The', 'cat', 'is', 'sitting', 'on', 'the', 'mat']
   → remove stopwords
   → ['cat', 'sitting', 'mat']
```

---

## What Are Stopwords?

Words that appear **very frequently** but carry **little distinctive meaning**:

```
English: the, is, at, on, and, or, but, with, to, of, a, an, this, that
         I, you, he, she, it, they, we, was, were, has, have
```

They're essential for grammar but don't help much for tasks like:
- Document classification
- Sentiment analysis (most of the time)
- Topic modelling
- Search indexing

Removing them reduces vocabulary size and noise.

---

## Examples

| Original sentence | After stopword removal |
|-------------------|------------------------|
| "The cat is on the mat" | "cat mat" |
| "I am going to the store" | "going store" |
| "She is the best teacher" | "best teacher" |

The retained words usually carry the main information.

---

## Why Remove Stopwords?

```
✓ Smaller vocabulary       → faster, less memory
✓ Less noise               → models focus on content words
✓ Higher TF-IDF signal     → stopwords would dominate raw counts otherwise
✓ Better for topic modelling → topics defined by content words
```

---

## When NOT to Remove Stopwords

Removing stopwords blindly can **destroy meaning**:

### 1. Negation matters

```
"I am NOT happy"
   → after stopword removal → "happy"
   → sentiment flipped from negative to positive 

Keep "not", "never", "no" if doing sentiment analysis.
```

### 2. Phrases and idioms

```
"to be or not to be"
   → after removal → empty
   → famous phrase destroyed
```

### 3. Modern language models

```
BERT, GPT, and other contextual models USE stopwords
   to learn context. Removing them hurts performance.
```

### 4. Some tasks need exact words

```
Question answering:
   "Who is the president of the USA?"
   → can't remove "who", "is", "the" — they shape the question
```

### 5. Search queries

```
"How to bake a cake"
   → remove "to", "a" → "How bake cake"
   → may miss the original intent
```

---

## Standard Stopword Lists

### NLTK

```python
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

stop_words = stopwords.words('english')
print(stop_words[:10])
# ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're"]
```

NLTK has stopwords for 20+ languages.

### spaCy

```python
import spacy
nlp = spacy.load('en_core_web_sm')
stop_words = nlp.Defaults.stop_words
```

### sklearn

```python
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
```

Different libraries have **different stopword lists**. NLTK has ~180 English stopwords; spaCy has ~300; sklearn has ~318.

---

## Custom Stopword Lists

The standard lists are starting points — customise them for your domain:

```python
custom_stopwords = set(stopwords.words('english'))

# Remove negations from stopwords (don't strip them!)
custom_stopwords -= {'not', 'no', 'never', 'nor'}

# Add domain-specific filler words
custom_stopwords |= {'patient', 'said', 'reported'}   # for medical notes
```

For specialised domains (medical, legal, scientific), build your own list.

---

## Implementation

```python
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

text = "The cat is sitting on the mat."
tokens = word_tokenize(text.lower())
stop_words = set(stopwords.words('english'))
filtered = [t for t in tokens if t not in stop_words]
print(filtered)
# ['cat', 'sitting', 'mat', '.']
```

---

## Decision Guide

```
✓ Use stopword removal when:
   - Bag-of-words / TF-IDF features
   - Topic modelling
   - Document classification on simple ML models
   - Search indexing (with caveats)

✗ Skip stopword removal when:
   - Sentiment analysis with negations
   - Question answering
   - Using modern language models (BERT, GPT)
   - Phrase / idiom preservation matters
   - Translation tasks
```

---

## Stopword Removal vs Other Preprocessing

```
Normalisation     → standardise form ("APPLE" → "apple")
Tokenisation      → split into words
Stopword removal  → drop common low-information words
Stemming/Lemma    → reduce to root form
```

Each is independent but typically applied in this order.

---

## Summary

```
Stopwords = common words with low information content
            (the, is, and, of, to, ...)

Removing them:
   ✓ Reduces vocabulary and noise
   ✓ Helps simple ML models focus on content
   ✗ Can destroy sentiment, questions, and phrases
   ✗ Hurts modern language models

Standard lists: NLTK, spaCy, sklearn
Always customise for your domain — especially keep "not", "no", "never" for sentiment.
```

> Stopword removal is a simple but **opinionated** preprocessing step. Always question whether your task actually needs it.
