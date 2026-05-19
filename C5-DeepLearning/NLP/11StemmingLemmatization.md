# Stemming and Lemmatisation

Two ways to **reduce inflected words to a common base form**.

```
"running", "runs", "ran"  →  "run"   (some common base)
```

Used to **collapse vocabulary** so the model sees related forms as the same word.

```
Stemming        → fast, crude truncation
Lemmatisation   → slow, linguistic — gives real dictionary words
```

---

## Stemming

Reduces words by **cutting off suffixes** (and sometimes prefixes) following rules.

```
"running"   → "run"
"happiness" → "happi"     ← not a real word
"running"   → "run"
"flies"     → "fli"       ← not a real word
"easily"    → "easili"    ← not a real word
```

### Porter Stemmer (classic algorithm)

A series of rule sequences:

```
Step 1a: SSES → SS    ("classes" → "class")
Step 1a: IES  → I     ("flies"  → "fli")
Step 1b: ED   → ""    ("walked" → "walk")
Step 1b: ING  → ""    ("running" → "runn" — then handled by step 1c)
Step 2:  ATIONAL → ATE ("national" → "natate"? — only on long enough stems)
```

Multiple steps applied in sequence. Fast but unsophisticated.

### Implementation in NLTK

```python
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
print(stemmer.stem('running'))    # 'run'
print(stemmer.stem('happiness'))  # 'happi'
print(stemmer.stem('flies'))      # 'fli'
```

### Advantages

```
✓ Very fast
✓ No vocabulary or POS lookup needed
✓ Reduces vocabulary aggressively
✓ Good for tasks where exact word doesn't matter (search, retrieval)
```

### Limitations

```
✗ Output may not be a real word
✗ Sometimes too aggressive (over-stemming)
   "university" → "univers"
   "universe" → "univers"
   → distinct meanings collapsed
✗ Sometimes too cautious (under-stemming)
✗ Language-specific (Porter is English-only)
```

---

## Lemmatisation

Linguistically informed — uses **dictionary lookup and POS tagging** to find the true base form (the **lemma**).

```
"better"   → "good"      (adjective, comparative form)
"running"  → "run"        (verb form)
"ate"      → "eat"        (irregular verb)
"mice"     → "mouse"      (irregular plural)
```

Always returns a **real word**.

### Why POS matters

```
"running" as a verb     → "run"
"running" as a noun     → "running"   (the activity)

Lemmatisation needs POS to handle these correctly.
```

### Implementation in NLTK

```python
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

print(lemmatizer.lemmatize('running', pos='v'))   # 'run'
print(lemmatizer.lemmatize('better', pos='a'))     # 'good'
print(lemmatizer.lemmatize('mice'))                # 'mouse'  (pos defaults to noun)
```

### Implementation in spaCy

```python
import spacy
nlp = spacy.load('en_core_web_sm')

doc = nlp("running better")
for token in doc:
    print(token.text, '→', token.lemma_)
# running → run
# better → well
```

spaCy automatically handles POS tagging during processing — no need to specify.

### Advantages

```
✓ Always real words → interpretable
✓ Handles irregular forms (mice → mouse, ate → eat)
✓ Context-aware (with POS)
✓ Better for downstream linguistic tasks
```

### Limitations

```
✗ Slower than stemming
✗ Requires a dictionary (WordNet, lexicons)
✗ Quality depends on POS tagger accuracy
✗ Limited to languages with available lexicons
```

---

## Comparison

| Aspect | Stemming | Lemmatisation |
|--------|----------|---------------|
| Approach | Rule-based truncation | Dictionary + POS lookup |
| Speed | Fast | Slower |
| Output validity | Often non-word | Always valid word |
| Context awareness | None | High (uses POS) |
| Accuracy | Moderate | High |
| Use case | Search, IR, classical ML | NLP that cares about correctness |

### Side-by-side

| Word | Stemmed (Porter) | Lemmatised |
|------|------------------|-----------|
| running | run | run |
| ran | ran | run |
| better | better | good (with POS=adjective) |
| children | children | child |
| was | wa | be (with POS=verb) |
| studies | studi | study |
| caring | care | care |
| flies | fli | fly |

Lemmatisation generally produces cleaner, more interpretable output. Stemming may be "good enough" for tasks like search where exact word doesn't matter.

---

## When to Use Which

```
Use STEMMING when:
   ✓ Speed matters more than precision
   ✓ Output need not be a real word
   ✓ Classical IR / search systems
   ✓ Tight memory or compute constraints

Use LEMMATISATION when:
   ✓ Output must be a valid word
   ✓ Downstream tasks need linguistic correctness
   ✓ Sentiment analysis, summarisation, translation
   ✓ Building interpretable features

Use NEITHER when:
   ✓ Using modern language models (BERT, GPT) — they handle morphology themselves
   ✓ Words like "running" vs "ran" carry meaning you don't want to lose
```

---

## Applications

```
Information retrieval    → stemming reduces query vocabulary
   Query "running shoes" matches "run shoes" → broader recall

Topic modelling          → group related forms under one stem/lemma
   "ate", "eats", "eating" → all about food

Sentiment analysis        → lemmatisation preserves meaning
   "better" → "good" connects to positive vocabulary

Text classification       → reduces feature space significantly
   often increases accuracy with less data
```

---

## In Practice

```python
# Stemming pipeline
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
stems = [stemmer.stem(t) for t in tokens]

# Lemmatisation pipeline (with POS tagging)
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'): return 'a'
    if treebank_tag.startswith('V'): return 'v'
    if treebank_tag.startswith('N'): return 'n'
    if treebank_tag.startswith('R'): return 'r'
    return 'n'

lemmatizer = WordNetLemmatizer()
tagged = pos_tag(tokens)
lemmas = [lemmatizer.lemmatize(t, get_wordnet_pos(pos)) for t, pos in tagged]
```

---

## Summary

```
Stemming      → fast, rule-based truncation, may not give real words
Lemmatisation → linguistic, dictionary-based, always gives real words

Both reduce vocabulary by mapping inflected forms to a common base.
Use stemming for speed (IR, classical ML).
Use lemmatisation for correctness (linguistic tasks).
Modern LLMs handle morphology natively — neither may be needed.
```

> Stemming and lemmatisation are classic preprocessing steps. They're declining in importance as deep learning models learn morphology automatically — but still common in traditional NLP pipelines.
