# Named Entity Recognition (NER)

A **semantic** task that identifies and classifies **named entities** in text — people, places, organisations, dates, etc.

```
"Apple Inc. was founded by Steve Jobs in Cupertino in 1976."

NER output:
   Apple Inc.    → ORGANIZATION
   Steve Jobs    → PERSON
   Cupertino     → LOCATION
   1976          → DATE
```

---

## What Counts as a "Named Entity"?

Standard entity types in most NER systems:

| Type | Examples |
|------|----------|
| **PERSON** | "Alice", "Barack Obama", "Dr. Smith" |
| **ORGANIZATION (ORG)** | "Google", "United Nations", "MIT" |
| **LOCATION (LOC)** | "Paris", "Mount Everest", "Asia" |
| **DATE** | "January 5", "2024-03-15", "next Tuesday" |
| **TIME** | "3:00 PM", "noon" |
| **MONEY** | "$5.99", "100 euros" |
| **PERCENT** | "20%", "two-thirds" |
| **GPE** | Geo-political entities — "Germany", "Tokyo" |
| **PRODUCT** | "iPhone", "Tesla Model 3" |
| **EVENT** | "World Cup", "WWII" |

Different systems use slightly different tag sets. Domain-specific NER adds custom entity types (drugs, genes, legal terms, etc.).

---

## How NER Works — IOB Tagging

NER is a **sequence labelling task** — each token gets a tag:

```
B-PER  → Beginning of a person entity
I-PER  → Inside a person entity
B-ORG  → Beginning of an organization
I-ORG  → Inside an organization
O      → Outside any entity (regular word)
```

Example:

```
Token       Tag
Elon        B-PER
Musk        I-PER
is          O
the         O
CEO         O
of          O
Tesla       B-ORG
,           O
based       O
in          O
Austin      B-LOC
,           O
Texas       B-LOC
.           O
```

Same machinery as chunking — just with **entity types** instead of phrase types.

---

## Approaches

### 1. Rule-Based / Regex

```
Email pattern:     \w+@\w+\.\w+         → EMAIL
Date pattern:      \d{4}-\d{2}-\d{2}    → DATE
Phone pattern:     \(\d{3}\) \d{3}-\d{4} → PHONE
```

Works for structured patterns; doesn't scale to flexible entities like names.

### 2. Statistical / Classical ML

Train a sequence labeller (HMM, CRF) on annotated corpora:

```
Features used:
   - Word itself
   - POS tag
   - Capitalisation
   - Previous/next words
   - Suffix patterns ("-corp" suggests ORG)
```

**Conditional Random Fields (CRF)** was the gold standard before neural methods.

### 3. Neural / Deep Learning

BiLSTM-CRF, BERT-based taggers — current state-of-the-art:

```python
import spacy
nlp = spacy.load('en_core_web_sm')

doc = nlp("Apple Inc. was founded by Steve Jobs in Cupertino.")
for ent in doc.ents:
    print(ent.text, ent.label_)
# Apple Inc.    ORG
# Steve Jobs    PERSON
# Cupertino     GPE
```

---

## Why NER Matters

| Use case | What NER provides |
|----------|------------------|
| Information extraction | Pull structured data from unstructured text |
| Search | "movies starring Tom Hanks" → resolve Tom Hanks as PERSON |
| Question answering | "Who founded Apple?" → identify PERSON candidates |
| Knowledge graphs | Build (entity, relation, entity) triples |
| Customer support | Extract names, products from tickets |
| Healthcare | Extract drug names, diseases, dosages |
| Legal | Identify parties, dates, monetary amounts |
| Finance | Extract company names, tickers, amounts |

NER is one of the **most practically useful** NLP tasks — turns text into structured data.

---

## Challenges

```
✗ Ambiguity
   "Apple"  → company OR fruit?
   "Jordan" → person OR country?
   → needs context

✗ Out-of-vocabulary entities
   Brand new companies, people, places not in training data

✗ Domain shift
   Medical NER ≠ legal NER ≠ news NER
   → domain-specific models often needed

✗ Cross-lingual
   Named entities behave differently across languages

✗ Nested entities
   "Bank of America" → ORG containing LOC ("America")
   Most systems handle this poorly
```

---

## NER vs Chunking

Both are sequence labelling tasks using IOB tags — but they target **different things**:

```
Chunking → grammatical PHRASES (NP, VP, PP)
            → SYNTACTIC structure
            → "what kind of phrase?"
            
NER     → semantic ENTITIES (PERSON, ORG, LOC)
            → SEMANTIC content
            → "what is this referring to in the real world?"
```

A noun phrase chunk and a PERSON entity often overlap, but not always:

```
"The president visited Paris"
   Chunking: [The president]NP visited [Paris]NP
   NER:      The president visited [Paris]LOC
              ↑ generic NP — not a named entity
```

Many NER systems use chunking output as a feature — chunks define **candidate spans**, NER assigns **entity types** to those that are real-world references.

---

## spaCy Example

```python
import spacy
nlp = spacy.load('en_core_web_sm')

text = "Apple Inc. was founded by Steve Jobs in Cupertino in 1976."
doc = nlp(text)

for ent in doc.ents:
    print(f"{ent.text:20} → {ent.label_:10} ({spacy.explain(ent.label_)})")

# Apple Inc.            → ORG       (Companies, agencies, institutions)
# Steve Jobs            → PERSON    (People, including fictional)
# Cupertino             → GPE       (Countries, cities, states)
# 1976                  → DATE      (Absolute or relative dates)
```

Visualise:

```python
spacy.displacy.serve(doc, style='ent')
```

---

## NER Is Semantic, Not Syntactic

This is worth emphasising:

```
"Apple"
   Syntactic view  → noun (NN)         ← POS tag, grammatical category
   Chunking view   → noun phrase (NP)  ← grammatical structure
   NER view        → ORGANIZATION       ← real-world referent

POS / chunking → "what role does this word play in the sentence?"
NER            → "what does this word refer to in the world?"
```

NER cares about **meaning** (which entity is being mentioned), not just **structure** (which category of word it is).

---

## Summary

```
NER = identify and classify named entities in text
    = SEMANTIC task (cares about real-world referents)
    = sequence labelling with IOB tags
    = recognise PERSON, ORG, LOC, DATE, etc.

Approaches:
   Rule-based   → regex for emails, dates
   Statistical  → CRF on annotated corpora
   Neural       → BERT, spaCy (modern state-of-the-art)

Used everywhere: search, knowledge graphs, healthcare,
                 finance, legal, customer support.
```

> NER is the bridge from syntax to semantics — it links surface text to actual real-world entities. One of the most practical NLP tasks for building structured knowledge from text.
