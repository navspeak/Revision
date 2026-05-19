# Part-of-Speech (POS) Tagging

Assigning a **grammatical category** (noun, verb, adjective, etc.) to each token.

```
"The cat sat on the mat"
   ↓
[The/DT, cat/NN, sat/VBD, on/IN, the/DT, mat/NN]
```

Foundation for syntactic analysis, parsing, named entity recognition, translation.

---

## Why POS Tagging Matters

```
✓ Resolves ambiguity:
   "book" → noun (a book) OR verb (to book a flight)
   POS context disambiguates.

✓ Enables downstream tasks:
   - Parsing needs POS to build syntactic trees
   - Machine translation needs POS to map grammar
   - Named entity recognition uses POS as features
   - Question answering uses POS to find subjects/objects

✓ Linguistic feature engineering for classical ML.
```

---

## Common Tag Sets

### Penn Treebank (English standard)

```
NN   noun, singular        (cat, dog)
NNS  noun, plural          (cats, dogs)
NNP  proper noun, singular (London, Alice)
VB   verb, base form       (run)
VBD  verb, past tense      (ran)
VBG  verb, gerund          (running)
JJ   adjective             (big, red)
RB   adverb                (quickly)
IN   preposition           (in, on, to)
DT   determiner            (the, a, this)
PRP  pronoun               (he, she, it)
CC   conjunction           (and, but)
```

~45 tags total. Detailed, English-specific.

### Universal POS Tags

Simplified, cross-lingual:

```
NOUN, VERB, ADJ, ADV, PRON, DET, ADP, CCONJ, NUM, PART, INTJ, PUNCT
```

~17 tags. Standard for multilingual NLP.

---

## Three Main Approaches

```
1. Rule-Based POS Tagging        → hand-written rules
2. Statistical POS Tagging       → learn probabilities from data
3. Brill (Transformation-Based)  → learn rules automatically
```

Modern systems use neural taggers (LSTM, Transformer) — but the foundations are these three.

---

## 1. Rule-Based POS Tagging

Apply manually crafted linguistic rules.

### Example heuristics

```
If word ends in "-ed" → likely VBD (past tense verb)
If word ends in "-ly" → likely RB (adverb)
If word is capitalised mid-sentence → NNP (proper noun)
If preceded by "the" → likely noun or adjective
```

### Workflow

```
1. Look up word in dictionary → get all possible tags
2. Apply rules to pick the right tag in context
```

### Example

```
"The cat ran"

The   → DT (determiner)              ← dictionary
cat   → NN or VB                       ← ambiguous
        → DT before it → likely noun
        → NN
ran   → VBD                            ← dictionary
```

### Strengths

```
✓ No training data needed
✓ Interpretable
✓ Good for low-resource languages with linguistic experts
```

### Limitations

```
✗ Brittle — fails on unseen patterns
✗ Hard to maintain as rules grow
✗ Can't handle ambiguity probabilistically
✗ Manual effort doesn't scale
```

---

## 2. Statistical POS Tagging

Learn from a **tagged corpus** which tag is most likely in a given context.

### Core idea

```
For each word w, find the most likely tag t given:
   - The word itself
   - The surrounding context (previous tag, next tag)
```

### Two probabilities to learn

```
Emission probability:    P(word | tag)
   How likely is this word given this tag?
   P("cat" | NN)   = 0.005
   P("cat" | VB)   = 0.0001

Transition probability:  P(tag_i | tag_{i-1})
   How likely is one tag to follow another?
   P(NN | DT)  = 0.7    (noun often follows determiner)
   P(VB | DT)  = 0.0    (verb rarely follows determiner)
```

### Combining

For a sequence of words, find the tag sequence that maximises:

```
∏ P(word_i | tag_i) × P(tag_i | tag_{i-1})
```

This is exactly what a **Hidden Markov Model (HMM)** does.

### Why it works better than rule-based

```
Aspect              Rule-Based       Statistical
Basis               Fixed rules      Probabilities from data
Learning            Manual           Automatic
Adaptability        Limited          Improves with more data
Ambiguity           Deterministic    Picks most likely
Scalability         Hard             Suits big datasets
```

---

## Hidden Markov Models (HMM)

The classic probabilistic model for POS tagging. **HMM is the textbook example of statistical POS tagging** — when people say "statistical POS tagger" they usually mean HMM.

### What "Hidden" and "Markov" Mean

The name decomposes into three parts:

```
Hidden  →  the states (POS tags) are NOT directly observed
            We see the WORDS, but the TAGS are hidden.
            The model infers them.

Markov  →  the Markov assumption (named after Andrei Markov):
            "the next state depends only on the CURRENT state,
             not on the full history."
            i.e. only one previous tag is considered as context.

Model   →  a probabilistic system with learned parameters
            (transition + emission + initial probabilities)
```

In POS tagging:

```
Words   (observed)  : the   cat   sat   on   the   mat
Tags    (hidden)    : DT    NN    VBD   IN   DT    NN

The tagger sees only the top row.
The bottom row is what we want to recover.
```

### Where HMM Fits Among Statistical Taggers

```
Statistical POS taggers (data-driven, learn from corpora):
   ├── HMM       ← classic, generative, simple, uses Viterbi
   ├── MEMM      (Maximum Entropy Markov Model)
   ├── CRF       (Conditional Random Fields — better for sequences)
   └── Neural    (BiLSTM, Transformer, BERT — state-of-the-art)
```

HMM is the **simplest and oldest** statistical tagger — others improve on it but the core idea (probabilistic context-aware tagging) comes from HMM.

### Components

```
Hidden states (POS tags):    DT, NN, VB, ...
Observations (words):         the, cat, ran, ...

Transition probabilities:    P(tag_i | tag_{i-1})
Emission probabilities:       P(word_i | tag_i)
Initial probabilities:        P(start_tag)
```

### Example

```
Sentence: "The cat ran"

Most likely tag sequence (computed via Viterbi algorithm):
   DT NN VBD

Why?
   P(DT|start) high
   P(the|DT) high
   P(NN|DT) high           → "cat" likely a noun after determiner
   P(cat|NN) high
   P(VBD|NN) high          → past verb often follows noun
   P(ran|VBD) very high
```

### Advantages

```
✓ Handles ambiguity probabilistically
✓ Captures sequential context (one tag before/after)
✓ Well-understood algorithm (Viterbi for decoding)
✓ Fast inference
```

### Limitations

```
✗ Only considers immediate previous tag (limited context)
✗ Independent observations assumption is unrealistic
✗ Requires labelled training data
✗ Outperformed by neural models on accuracy
```

---

## 3. Brill (Transformation-Based) Tagger

A hybrid — **starts with a baseline tagging** and then **learns correction rules** from data.

### Core idea

```
1. Initialise: assign each word its most common tag (from training data)
2. Iteratively find rules that fix tagging errors:
      Example: "if tag = NN but previous word is 'to', change tag to VB"
3. Apply the best rule, repeat
```

### Example

```
Before: "I want to/IN run/NN"
                              ← "run" tagged as NN (most common)
Rule:   "if tag=NN and previous word='to', change to VB"
After:  "I want to/IN run/VB"
                              ← correction applied
```

### Characteristics

```
✓ Combines data-driven learning with interpretable rules
✓ Human-readable output rules
✓ Competitive accuracy on medium data
```

### Limitations

```
✗ Slower to train (lots of rule candidates to try)
✗ Less accurate than modern neural taggers
```

---

## Modern Approaches

```
Classical:   Rule-based, HMM, Brill, CRF
Modern:      LSTM-based taggers, Transformer-based (BERT)

State of the art:
   BERT achieves 97%+ accuracy on standard benchmarks
   spaCy uses neural taggers in production
```

---

## sklearn / Library API

```python
import nltk
nltk.download('averaged_perceptron_tagger')

text = "The cat ran quickly"
tokens = nltk.word_tokenize(text)
tags = nltk.pos_tag(tokens)
print(tags)
# [('The', 'DT'), ('cat', 'NN'), ('ran', 'VBD'), ('quickly', 'RB')]
```

In spaCy:

```python
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp("The cat ran quickly")
for token in doc:
    print(token.text, token.pos_, token.tag_)
```

---

## Challenges in POS Tagging

```
✗ Ambiguity:
   "book" → NN or VB?
   "running" → VBG (verb) or NN (noun, the activity)?

✗ Unknown words:
   Names, technical terms, slang

✗ Cross-domain shift:
   Tagger trained on news may fail on tweets

✗ Cross-lingual:
   Tag sets differ across languages
```

---

## Summary

```
POS tagging = assign grammatical category to each token

Approaches:
   Rule-based   → handcrafted rules, deterministic
   Statistical (HMM)  → probabilistic, learned from data
   Brill        → learn correction rules
   Neural       → state-of-the-art (BERT, spaCy)

Foundation for syntax, parsing, NER, translation.
```

> POS tagging is one of the oldest NLP tasks — now near-solved by modern neural systems. But understanding the classical approaches teaches the fundamentals of sequence labelling.
