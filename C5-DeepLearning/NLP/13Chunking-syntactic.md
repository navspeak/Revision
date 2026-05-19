# Chunking — Shallow Parsing

Group adjacent tokens into **phrases** (chunks) — without building full parse trees.

```
"The big cat jumped over the fence"

POS tags:
   The/DT  big/JJ  cat/NN  jumped/VBD  over/IN  the/DT  fence/NN

Chunks:
   [The big cat]NP   [jumped]VP   [over the fence]PP
```

NP = noun phrase, VP = verb phrase, PP = prepositional phrase.

---

## What Chunking Does

```
Take a POS-tagged sentence
   → identify phrase boundaries
   → tag spans like NP, VP, PP

It's MORE than POS tagging but LESS than full parsing.
"Shallow" = stops at phrase level, doesn't go deeper.
```

---

## Why Use Chunking?

```
✓ Identify key information units
   "[The big cat]NP did [something]VP"  → who and what

✓ Foundation for information extraction
   NPs often correspond to entities or topics

✓ Faster than full parsing
   Don't need a complete tree to be useful

✓ Good for downstream tasks
   - Named Entity Recognition
   - Relation extraction
   - Question answering
```

---

## Chunk Representation — IOB Tagging

Tokens are tagged with **chunk membership** using IOB (Inside, Outside, Beginning) notation:

```
B-NP   Beginning of a Noun Phrase
I-NP   Inside a Noun Phrase
B-VP   Beginning of a Verb Phrase
I-VP   Inside a Verb Phrase
B-PP   Beginning of a Prepositional Phrase
I-PP   Inside a Prepositional Phrase
O      Outside any chunk
```

### Example

```
Token       POS    Chunk
The         DT     B-NP
big         JJ     I-NP
cat         NN     I-NP
jumped      VBD    B-VP
over        IN     B-PP
the         DT     I-PP
fence       NN     I-PP
.           .      O
```

This is a sequence-labelling task — every token gets a chunk tag.

---

## How Chunking Works

### Rule-based

Use POS patterns to identify phrases:

```
NP rule: DT? JJ* NN+
   → optional determiner, zero or more adjectives, one or more nouns
   → matches: "the cat", "the big cat", "big cats", "cat"

VP rule: VB+ (RB)*
   → one or more verbs, optional adverbs

PP rule: IN NP
   → preposition followed by a noun phrase
```

### Statistical / Neural

Train a sequence labeller (HMM, CRF, LSTM, Transformer) on a corpus where chunks are pre-annotated.

---

## NLTK Example

```python
import nltk

sentence = "The big cat jumped over the fence."
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)

# Define a chunk grammar
chunk_grammar = r"""
    NP: {<DT>?<JJ>*<NN>+}        # noun phrase
    VP: {<VB.*><RB>?}            # verb phrase
    PP: {<IN><NP>}                # prepositional phrase
"""

chunk_parser = nltk.RegexpParser(chunk_grammar)
tree = chunk_parser.parse(tagged)
print(tree)
```

Output (tree representation):

```
(S
  (NP The/DT big/JJ cat/NN)
  (VP jumped/VBD)
  over/IN
  (NP the/DT fence/NN)
  ./.)
```

---

## Advantages of Chunking

```
✓ Captures local structure without expensive full parsing
✓ Fast — usually a single pass over tokens
✓ Easy to interpret — chunks have clear boundaries
✓ Bridges gap between POS tagging and full parsing
✓ Useful for many downstream tasks
```

---

## Limitations

```
✗ Doesn't capture deep grammatical relations
   "[John]NP [saw]VP [the man]NP [with the telescope]PP
   → ambiguous: who has the telescope?
   → chunking can't resolve — needs full parsing

✗ Phrase boundary errors propagate to downstream tasks

✗ Some constructions are hard to chunk
   - Coordinated phrases: "the [cats and dogs]"
   - Embedded clauses
   - Long-distance dependencies
```

---

## Applications

```
Named Entity Recognition (NER)
   → entities often appear as NPs

Information extraction
   → "[Company]NP [acquired]VP [Company]NP"

Question answering
   → identify candidate answer phrases

Relation extraction
   → find subject-verb-object triples

Sentence summarisation
   → extract key NPs and VPs

Coreference resolution
   → group NP mentions that refer to the same entity
```

---

## Chunking vs Parsing

| | Chunking (shallow) | Parsing (deep) |
|-|-------------------|----------------|
| Output | Flat phrase tags | Hierarchical tree |
| Detail | Phrase level | Full grammatical structure |
| Speed | Fast | Slower |
| Complexity | Easier | Harder |
| Use | Quick info extraction | Detailed analysis |
| Algorithm | Regex / sequence labelling | CFG / dependency parsers |

---

## Summary

```
Chunking = group tokens into phrases (NP, VP, PP)
         = sequence labelling problem (IOB tags)
         = "shallow parsing"

Useful for:
   - Information extraction
   - Named entity recognition
   - Quick syntactic features

Limitations:
   - No hierarchy
   - Doesn't resolve attachment ambiguity
   - Errors compound downstream

Sits between POS tagging and full parsing.
```

> Chunking is the practical middle ground: more structure than POS tagging, less complexity than full parsing.
