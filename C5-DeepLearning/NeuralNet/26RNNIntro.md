# RNN — Recurrent Neural Networks

The next family of neural networks. While CNNs handle **spatial** data (images), RNNs handle **sequential / temporal** data — text, audio, time series, anything where **order matters**.

```
MLP   →  for tabular data (independent features)
CNN   →  for spatial data (images, with neighbouring pixels)
RNN   →  for SEQUENTIAL data (where ORDER and HISTORY matter)
```

---

## What RNNs Are

```
A neural network with MEMORY.

Each step processes one input AND a hidden state carried from the previous step.
   → "remembers" what it has seen so far
   → can model dependencies across time
```

Architecture in one picture:

```
   x_1       x_2       x_3       ...      x_t
    │          │          │                  │
    ▼          ▼          ▼                  ▼
  ┌───┐ ──► ┌───┐ ──► ┌───┐ ──► ...  ──► ┌───┐
  │ h │     │ h │     │ h │              │ h │
  └───┘     └───┘     └───┘              └───┘
    │          │          │                  │
    ▼          ▼          ▼                  ▼
   y_1       y_2       y_3                 y_t

   Hidden state h carries information FORWARD through time.
```

Each cell takes:
- The current input `x_t`
- The hidden state from the previous step `h_{t-1}`

And produces:
- A new hidden state `h_t`
- (Optionally) an output `y_t`

**That hidden state is the network's memory.**

---

## Why RNNs Exist — Why MLPs and CNNs Fail on Sequences

### MLPs fail because they need fixed-size input

```
MLP expects: input shape = (n_features,)
Sequence:    "I love NLP"  →  3 words
             "I love deep learning a lot"  →  6 words

Different lengths → MLP can't handle them naturally.

Padding to max length helps but wastes capacity.
```

Also: MLP has **no concept of order**. "Cat ate fish" and "Fish ate cat" look identical to an MLP if you bag-of-words encode them.

### CNNs partially fix this but...

```
CNNs CAN process variable-length 1D sequences (text as a sequence of word vectors).
CNNs detect LOCAL patterns ("not good" — a 2-word negation pattern).

BUT:
✗ CNNs have a FIXED receptive field (e.g., 3 words at a time)
✗ Long-range dependencies are hard
   "The cat that I saw yesterday in the park ... was beautiful"
   → "cat" and "was" are far apart, but related
✗ No persistent memory across the sequence
```

### RNNs solve this with the hidden state

```
RNN processes elements ONE AT A TIME.
The hidden state ACCUMULATES information across the sequence.
   → captures both short and long-range dependencies
   → handles variable-length input naturally
   → has TRUE memory
```

---

## A Concrete Comparison

Task: **predict the next word**.

```
Input: "The cat sat on the ___"
Target: "mat"
```

### MLP approach

```
Convert sentence to bag of words → ignore order
Or one-hot encode last 5 words → only sees 5 words

Problem: limited context, ignores order
```

### CNN approach

```
Apply 1D convolutions over word embeddings
Detect short patterns ("sat on the ___")

Problem: fixed window, can't use the whole sentence
```

### RNN approach

```
Read words ONE BY ONE:
   "The" → h_1
   "cat" → h_2 (knows about "The")
   "sat" → h_3 (knows about "The cat")
   "on"  → h_4 (knows about "The cat sat")
   "the" → h_5 (knows about "The cat sat on")
   
At each step, hidden state CARRIES history forward.
Predict next word from h_5 → "mat"
```

The RNN has **all the context** because the hidden state carries it.

---

## The Three Families Side by Side

| | MLP | CNN | RNN |
|-|-----|-----|-----|
| **Best for** | Tabular features | Spatial / images | Sequential / temporal |
| **Input shape** | Fixed-size vector | Fixed-size grid (image) | Variable-length sequence |
| **Captures** | Direct feature relationships | Local spatial patterns | Temporal dependencies |
| **Has memory?** | No | No | **YES (hidden state)** |
| **Order matters?** | Doesn't help | Doesn't help much | **YES — defines RNNs** |
| **Weight sharing** | No | Yes (across positions) | Yes (across time steps) |
| **Examples** | Credit scoring, churn | Image classification, detection | Translation, speech, time series |

---

## What Tasks RNNs Excel At

```
Natural Language Processing:
   - Language modelling (next-word prediction)
   - Machine translation
   - Sentiment analysis
   - Text generation
   - Named entity recognition

Speech:
   - Speech recognition (audio → text)
   - Speech synthesis (text → audio)
   - Speaker identification

Time Series:
   - Stock price forecasting
   - Weather prediction
   - Sensor / IoT data analysis
   - Energy load forecasting

Other sequences:
   - Music generation
   - Video classification (sequence of frames)
   - Anomaly detection in logs
   - DNA / protein sequences
```

Anything with **time or order** is RNN territory.

---

## How the Hidden State Works

At each time step:

```
h_t = activation(W_x · x_t + W_h · h_{t-1} + b)
                       ↑              ↑
                  current input    previous state
                  weight matrix    weight matrix

y_t = W_y · h_t + b_y     (optional output at each step)
```

Same weights `W_x`, `W_h`, `W_y` used at **every time step**. This is weight sharing across **time** — analogous to CNN's weight sharing across **space**.

---

## Training RNNs — Backpropagation Through Time (BPTT)

Backprop in RNNs has to traverse the time axis:

```
Forward:  x_1 → h_1 → x_2 → h_2 → ... → h_T → y_T → loss
Backward: gradient flows BACK through ALL time steps

The same weights get gradient contributions from EVERY time step.
```

This is called **BPTT** (Backpropagation Through Time) — conceptually identical to standard backprop, just unrolled across the sequence.

Full details in `27BPTT.md`.

---

## The Big Problem with Vanilla RNNs

```
Vanishing / Exploding Gradients

When gradients flow back through many time steps:
   - They're multiplied at each step
   - If multiplier < 1 → gradients VANISH (long-range info lost)
   - If multiplier > 1 → gradients EXPLODE (unstable training)
```

Result: vanilla RNNs struggle with **long sequences** (> ~20 steps).

### The Solution — LSTM and GRU

```
LSTM (Long Short-Term Memory):
   adds GATES that explicitly control what to remember / forget
   → can preserve gradient flow over hundreds of time steps

GRU (Gated Recurrent Unit):
   simpler version of LSTM with fewer parameters
   → similar performance, slightly faster
```

Almost all modern "RNN" code actually uses LSTM or GRU. Vanilla RNNs are teaching tools.

---

## Common RNN Architectures (Sequence Types)

```
One-to-one:        single input → single output
                   (this is just an MLP — not really an RNN use case)

One-to-many:       single input → sequence output
                   e.g., image → caption ("a dog is running")

Many-to-one:       sequence input → single output
                   e.g., sentence → sentiment ("positive")

Many-to-many (sync):  sequence → sequence (aligned)
                       e.g., POS tagging — one tag per word

Many-to-many (async): sequence → sequence (different lengths)
                       e.g., translation — sentence to sentence
                       (encoder-decoder architecture)
```

---

## How RNNs "Graduate From" MLP / CNN

```
MLP:
   ✓ baseline neural network
   ✓ each input independent
   ✗ no spatial structure
   ✗ no temporal structure
   
CNN: builds on MLP by adding WEIGHT SHARING ACROSS SPACE
   ✓ exploits spatial locality
   ✓ translation invariant
   ✓ hierarchical features
   ✗ still doesn't model sequences well
   
RNN: builds on MLP by adding WEIGHT SHARING ACROSS TIME
   ✓ exploits temporal context
   ✓ variable-length inputs
   ✓ has MEMORY (hidden state)
   ✗ vanishing gradients (solved by LSTM/GRU)
   ✗ sequential by nature → hard to parallelise
```

Each family takes the **MLP and adds a structural prior** that matches its data type:

```
MLP    →  generic
CNN    →  spatial prior (images)
RNN    →  temporal prior (sequences)
```

---

## What Followed RNNs — Transformers

Modern NLP has largely **replaced RNNs with Transformers** (BERT, GPT, T5). Why?

```
RNN limitations:
   ✗ Sequential processing → can't parallelise within a sequence
   ✗ Long-range dependencies still tricky even with LSTM
   ✗ Training is slow

Transformers:
   ✓ Use ATTENTION instead of recurrence
   ✓ Fully parallelisable
   ✓ Better at long-range dependencies
   ✓ State-of-the-art on language, vision, speech, code
```

But RNNs still matter:
- LSTMs are excellent for time series
- Resource-constrained devices (smaller models)
- Streaming inference (process tokens as they arrive)
- Educationally — understanding RNNs makes Transformers easier

---

## What You'll Learn Next

A typical RNN module covers:

```
1. The recurrent cell (basic RNN)
2. Forward and backward through time (BPTT)
3. Vanishing/exploding gradients problem
4. LSTM — gated memory cells
5. GRU — simplified gates
6. Bidirectional RNNs
7. Sequence-to-sequence (encoder-decoder)
8. Applications (language modelling, translation, etc.)
9. (Optional) Attention mechanism → bridge to Transformers
```

---

## Summary

```
RNN = Recurrent Neural Network = neural network WITH MEMORY

Why exist:
   MLP can't handle variable-length sequences
   CNN sees only local patterns
   RNN models TEMPORAL DEPENDENCIES via a HIDDEN STATE

How it works:
   Process sequence one step at a time
   Carry hidden state forward as memory
   Same weights reused at every time step (weight sharing in TIME)

Strengths:
   ✓ Variable-length input
   ✓ Captures temporal order
   ✓ Persistent memory across steps

Weaknesses:
   ✗ Vanishing / exploding gradients (vanilla RNN)
   ✗ Sequential — hard to parallelise
   → solved by LSTM, GRU, and ultimately TRANSFORMERS

Use cases:
   NLP, speech, time series, anything with a temporal dimension.
```

> RNNs are the third pillar of classical deep learning: **MLP for tabular, CNN for spatial, RNN for temporal**. Each one adds the right inductive bias for its data type. After RNNs, the next leap is **Transformers** — which use attention to handle sequences better than recurrence ever could.
