# Hidden Markov Models (HMM) for POS Tagging

An HMM models a sequence as **observable symbols (words) emitted by hidden states (tags)**.

```
Hidden states (tags):    DT → NN → VBD → IN → DT → NN
Observed words:          the  cat  sat   on   the  mat
```

We observe the words. The tags are hidden — we want to **infer** them.

---

## The Two Probabilities

### 1. Transition probability — `P(tag_i | tag_{i-1})`

How likely one tag follows another:

```
P(NN | DT)  = 0.7   ← noun often follows determiner
P(VB | DT)  = 0.0   ← verb rarely follows determiner
P(VBD | NN) = 0.4   ← past verb often follows noun
```

Learned from a tagged corpus by counting.

### 2. Emission probability — `P(word | tag)`

How likely a word is given a tag:

```
P("cat" | NN)  = 0.005
P("cat" | VB)  = 0.0001
P("sat" | VBD) = 0.01
P("the" | DT)  = 0.3
```

Also learned by counting from the corpus.

---

## The Markov Assumption

```
Current tag depends ONLY on the previous tag (not the whole history).
Current word depends ONLY on its tag.
```

That's why it's "Markov" — limited memory. Makes the math tractable.

---

## Tiny Worked Example

**Toy corpus to learn probabilities from:**

```
"the/DT cat/NN sat/VBD"
"the/DT dog/NN ran/VBD"
"a/DT cat/NN ran/VBD"
```

### Transition probabilities (from corpus counts)

```
P(DT | START) = 3/3 = 1.0    (every sentence starts with DT)
P(NN | DT)    = 3/3 = 1.0    (always NN after DT)
P(VBD | NN)   = 3/3 = 1.0    (always VBD after NN)
P(END | VBD)  = 3/3 = 1.0
```

### Emission probabilities

```
P("the" | DT) = 2/3 ≈ 0.67
P("a" | DT)   = 1/3 ≈ 0.33

P("cat" | NN) = 2/3 ≈ 0.67
P("dog" | NN) = 1/3 ≈ 0.33

P("sat" | VBD) = 1/3 ≈ 0.33
P("ran" | VBD) = 2/3 ≈ 0.67
```

---

## Now Tag a New Sentence

Sentence: **"the dog sat"**

We need to find the most likely tag sequence (t₁, t₂, t₃) given the words.

### The math

For any candidate tag sequence:

```
P(tags | words) ∝ ∏ P(word_i | tag_i) × P(tag_i | tag_{i-1})
                 i
```

Try the candidate **DT NN VBD**:

```
P(DT | START)   × P("the" | DT)   = 1.0  × 0.67 = 0.67
P(NN | DT)      × P("dog" | NN)   = 1.0  × 0.33 = 0.33
P(VBD | NN)     × P("sat" | VBD)  = 1.0  × 0.33 = 0.33

Combined probability = 0.67 × 0.33 × 0.33 = 0.073
```

Now try an alternative, **DT NN NN**:

```
P(DT | START)   × P("the" | DT)   = 1.0 × 0.67 = 0.67
P(NN | DT)      × P("dog" | NN)   = 1.0 × 0.33 = 0.33
P(NN | NN)      × P("sat" | NN)   = 0.0 × 0.0  = 0.0    ← unseen in training

Combined = 0
```

Try **VBD NN VBD**:

```
P(VBD | START) × P("the" | VBD)  = 0 × 0      = 0      ← sentence never starts with VBD
```

The model picks **DT NN VBD** — the only sequence with non-zero probability.

```
Predicted tags:  the/DT  dog/NN  sat/VBD ✓
```

---

## The Viterbi Algorithm

Trying all tag combinations explicitly is exponential — there are |T|ⁿ combinations for `n` words and `|T|` possible tags.

For a 10-word sentence with 45 tags: 45^10 ≈ 3.4 × 10^16 combinations.

The **Viterbi algorithm** solves this with **dynamic programming** in O(n × |T|²) — way faster.

### Viterbi intuition

```
For each position i and tag t:
   V[i][t] = max over previous tag t':
                V[i-1][t'] × P(t | t') × P(word_i | t)

   = "best probability of any tag sequence ending in tag t at position i"
```

Build a table from left to right, keeping the best path at each cell. At the end, read off the most likely full sequence.

### Tiny Viterbi table for "the dog sat"

Possible tags: DT, NN, VBD

```
          word 1 (the)    word 2 (dog)         word 3 (sat)

DT        1.0 × 0.67      0 × 0 × 0            0 × 0 × 0
          = 0.67          = 0                  = 0

NN        0 × 0.0         0.67 × 1.0 × 0.33    ...
          = 0             = 0.22

VBD       0 × 0           0 × ...              0.22 × 1.0 × 0.33
                                               = 0.073   ← best path ends here
```

Backtrack from the highest cell at position 3 → reveals: **DT → NN → VBD**.

---

## Why HMMs Work for POS Tagging

```
✓ Capture sequential context (one tag before)
✓ Probabilistic — handle ambiguity naturally
✓ Efficient inference via Viterbi
✓ Easy to train (just count)
✓ Interpretable parameters
```

---

## Handling Ambiguity — Concrete Example

```
"I saw the book"

"saw" could be:
   VBD (past tense of see)
   NN  (a saw, tool)

Use HMM probabilities:

VBD path:  P(VBD | PRP) × P("saw" | VBD)
        = 0.4 × 0.005 = 0.002

NN path:   P(NN | PRP) × P("saw" | NN)
        = 0.01 × 0.0001 = 0.000001

VBD wins → "saw" tagged as VBD ✓
```

The context (previous tag was PRP for "I") combined with emission stats correctly resolves the ambiguity.

---

## The Full HMM Definition

An HMM is defined by:

| Component | Symbol | Meaning |
|-----------|--------|---------|
| States | `S = {s₁, s₂, ...}` | Hidden tags |
| Observations | `O = {o₁, o₂, ...}` | Observed words |
| Initial probabilities | `π_i = P(s_i | START)` | Probability of starting with each tag |
| Transition matrix | `A[i][j] = P(s_j | s_i)` | Tag-to-tag probabilities |
| Emission matrix | `B[i][k] = P(o_k | s_i)` | Word probabilities given tag |

Training: learn `π`, `A`, `B` from a tagged corpus.
Inference: use Viterbi to find best tag sequence for a new sentence.

---

## Limitations

```
✗ Only sees one previous tag (limited context)
✗ Independence assumption: each word independent given its tag
✗ Suffers with unknown words (zero emission probability)
✗ Outperformed by neural taggers (BiLSTM, BERT) on accuracy
```

Modern alternatives: CRFs, LSTMs, Transformers. But HMMs remain the canonical example of probabilistic sequence models.

---

## HMMs Beyond POS Tagging

HMMs apply anywhere you have **hidden states emitting observations**:

```
Speech recognition       → hidden phonemes emit acoustic features
Named Entity Recognition → hidden entity types emit words
Gene prediction          → hidden coding/non-coding states emit DNA bases
Activity recognition     → hidden activities emit sensor readings
Stock market modelling   → hidden market regimes emit prices
```

The HMM framework is **task-agnostic** — the same math handles all of these.

---

## Summary

```
HMM = sequence model where:
   - Observed words come from hidden tags
   - Each tag depends only on the previous (Markov assumption)
   - Each word depends only on its tag

Two probability sets:
   Transition  P(tag_i | tag_{i-1})
   Emission    P(word | tag)

For tagging:
   Find tag sequence maximising  ∏ P(word | tag) × P(tag | prev_tag)
   Use Viterbi algorithm (dynamic programming)

Classic, foundational sequence model in NLP.
```

> HMMs are the "Hello World" of probabilistic sequence models — and they capture the core idea behind every modern sequence model: **use context to resolve ambiguity probabilistically**.
