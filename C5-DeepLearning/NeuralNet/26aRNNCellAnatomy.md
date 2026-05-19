# Anatomy of an RNN Cell, Weight Sharing, and Unfolding

Three foundational ideas that explain HOW an RNN actually works:

```
1. The RNN CELL          →  the building block that carries information through time
2. WEIGHT SHARING         →  same cell, same weights, every time step (symmetry)
3. UNFOLDING             →  visualising the RNN as a deep network through time
```

Understand these three and you understand RNNs.

---

## 1. Anatomy of an RNN Cell

The RNN cell is the **fundamental building block**. It takes one input, combines it with memory, and produces a new memory state.

### The Cell

```
                    h_{t-1}  (previous hidden state — memory)
                        │
                        ▼
        ┌────────────────────────────┐
        │                            │
   x_t ──►            CELL            ──► h_t  (new hidden state)
        │                            │
        │      h_t = f(W_x·x_t        │
        │              + W_h·h_{t-1}  │
        │              + b)           │
        │                            │
        └────────────────────────────┘
                        │
                        ▼
                       y_t  (optional output)
```

### Three Things Inside the Cell

```
1. INPUT TRANSFORMATION:    W_x · x_t
   → transforms current input into a feature representation

2. HIDDEN STATE TRANSFORMATION:    W_h · h_{t-1}
   → incorporates the memory carried from previous time step

3. ACTIVATION:    h_t = tanh(W_x · x_t + W_h · h_{t-1} + b)
   → non-linearity (typically tanh or ReLU)
```

```
Optional output:    y_t = W_y · h_t + b_y
   → produces an output at this time step (e.g., next-word prediction)
```

### Full Mathematical Form

```
h_t = tanh(W_x · x_t + W_h · h_{t-1} + b_h)
y_t = W_y · h_t + b_y

Where:
   x_t      → input at time t                (shape: input_dim)
   h_{t-1}  → hidden state from t-1          (shape: hidden_dim)
   h_t      → new hidden state at time t     (shape: hidden_dim)
   y_t      → output at time t               (shape: output_dim)
   W_x      → input-to-hidden weights        (shape: hidden_dim × input_dim)
   W_h      → hidden-to-hidden weights        (shape: hidden_dim × hidden_dim)
   W_y      → hidden-to-output weights        (shape: output_dim × hidden_dim)
   b_h, b_y → biases
```

### The Hidden State — The Cell's "Memory"

```
h_t carries forward EVERYTHING the network has seen so far.
   → not just what's at this time step
   → but a SUMMARY of all previous inputs
   
The cell decides how to UPDATE this summary at each step.
```

This persistent state is what makes RNNs special. A regular MLP has no equivalent.

---

## 2. Weight Sharing — The Symmetry of RNN Processing

This is the **most important RNN insight after the hidden state**.

```
SAME WEIGHTS at every time step.
   → W_x, W_h, W_y are LEARNED ONCE
   → APPLIED IDENTICALLY at every time step
```

### Why "Symmetry"

```
At time t=1:  h_1 = tanh(W_x · x_1 + W_h · h_0 + b)
At time t=2:  h_2 = tanh(W_x · x_2 + W_h · h_1 + b)
At time t=3:  h_3 = tanh(W_x · x_3 + W_h · h_2 + b)
              ...
At time t=T:  h_T = tanh(W_x · x_T + W_h · h_{T-1} + b)
                          ↑
                Same W_x, W_h, b for ALL steps.
```

**Each time step uses identical weights.** That symmetry is the defining feature of RNNs.

### Why This Matters

```
✓ HANDLES VARIABLE-LENGTH SEQUENCES
   - "Hi" (length 2) and "Hello world" (length 11) both work
   - because the SAME cell processes any length
   - no need to add new parameters for longer inputs

✓ DRAMATICALLY FEWER PARAMETERS
   - One cell's worth of weights, regardless of sequence length
   - 100-step sequence ≠ 100× the parameters
   - same 3 weight matrices: W_x, W_h, W_y

✓ TRANSFER OF KNOWLEDGE ACROSS POSITIONS
   - what the cell learns at step 1 applies at step 100
   - "the cat" recognised whether at the start or end of a sentence

✓ CONSISTENT TRANSFORMATION AT EVERY STEP
   - Same logic applied uniformly regardless of position
   - The network's "rule" for processing a token doesn't change
     halfway through the sequence
   - Learning is CONSISTENT — every gradient update refines ONE
     transformation rule used everywhere
   - No "early step" vs "late step" weights to coordinate
```

### Analogy to CNN's Weight Sharing

```
CNN weight sharing:    same filter applied at every POSITION in space
RNN weight sharing:    same cell applied at every POSITION in time

Same idea, different axis:
   CNN  →  spatial weight sharing  →  translation invariance
   RNN  →  temporal weight sharing  →  time-step invariance
```

This is why "RNN is to time what CNN is to space" is a common saying.

### Parameter Count Example

```
Vanilla RNN cell:
   W_x: hidden_dim × input_dim
   W_h: hidden_dim × hidden_dim
   W_y: output_dim × hidden_dim
   biases

For input_dim=100, hidden_dim=128, output_dim=10:
   W_x: 128 × 100 = 12,800
   W_h: 128 × 128 = 16,384
   W_y: 10 × 128 = 1,280
   biases: ~266
   Total: ~30,730 parameters

Sequence of length 5:    30,730 params (SAME!)
Sequence of length 100:   30,730 params (SAME!)
Sequence of length 1000:  30,730 params (SAME!)

→ parameter count is INDEPENDENT of sequence length
→ same cell applied 1000 times
```

This is the magic of weight sharing — handles any length without growing the model.

---

## 3. Unfolding — Visualising RNNs Through Time

The RNN cell is drawn as a **compact loop**:

```
        ┌──────┐
   x ──►│ RNN  │──► y
        │ cell │
        │  h   │
        └──┬───┘
           │ (feedback loop)
           └───────────┐
                       │
                       ▼
                (back to itself)
```

This is concise but hides what really happens during training. So we **unfold** it across time.

### Unfolded View

```
   x_1       x_2       x_3        x_4         (input at each time step)
    │          │          │          │
    ▼          ▼          ▼          ▼
  ┌─────┐ ──► ┌─────┐ ──► ┌─────┐ ──► ┌─────┐
  │ h_1 │     │ h_2 │     │ h_3 │     │ h_4 │   (hidden state)
  └─────┘     └─────┘     └─────┘     └─────┘
    │          │          │          │
    ▼          ▼          ▼          ▼
   y_1       y_2       y_3        y_4         (output at each time step)
```

Now it looks like a **deep feedforward network** — one cell stacked T times for a sequence of length T.

### What "Unfolding" Means

```
The CELL is one piece of code.
At RUNTIME, it's applied REPEATEDLY for each time step.

Folded:    one cell with a feedback loop (compact, conceptual)
Unfolded:  T copies of the same cell laid out side by side (explicit, for training)

   Both represent the SAME network — just visualised differently.
```

The unfolded view is essential because it makes the gradient flow visible — which is needed for BPTT (see `27BPTT.md`).

### Concrete Unfolding Example

Sentence: "The cat sat" (3 words = 3 time steps)

```
Folded RNN:
   h_0 = zeros (initial state, all zeros usually)

Unfolded:
                      Step 1                 Step 2                Step 3
                      ──────                  ──────                ──────
   x_t:               "The"                   "cat"                 "sat"
                        │                       │                     │
                        ▼                       ▼                     ▼
   Cell:    ┌───────────┴────────┐   ┌──────────┴────────┐   ┌────────┴────────┐
            │ h_1 = tanh(           │ │ h_2 = tanh(         │ │ h_3 = tanh(       │
            │  W_x·"The" + W_h·h_0)│→│  W_x·"cat" + W_h·h_1)→│  W_x·"sat" + W_h·h_2)│
            └───────────┬────────┘   └──────────┬────────┘   └────────┬────────┘
                        ▼                       ▼                     ▼
                       h_1                     h_2                   h_3
```

```
Same W_x, W_h, b used at every step.
h_3 contains information about ALL three words.
```

### Why Unfolding Matters

```
1. CLARIFIES the computation
   - what flows where at each time step is visible

2. ENABLES BACKPROP
   - gradient must flow backwards through every cell
   - unfolded view = visible chain rule path

3. MAKES WEIGHT SHARING EXPLICIT
   - you can see the SAME W_x, W_h, b in every cell

4. EXPOSES PROBLEMS
   - vanishing/exploding gradients become obvious
     when you see the depth of the chain

5. EQUIVALENT TO A DEEP MLP (with weight sharing)
   - sequence length T = an MLP with T layers
   - but with identical weights at every layer
```

### Comparing Folded and Unfolded

| Folded | Unfolded |
|--------|----------|
| Compact diagram | Spans many cells across the page |
| Hides time-step computation | Shows every step explicitly |
| Easy to describe in words | Easy to follow gradient flow |
| Used in slides / papers | Used for training mathematics |
| **Same network** | **Same network** |

---

## How These Three Connect

```
ANATOMY of the cell:
   defines WHAT happens at each step
   (input + previous state → new state)

WEIGHT SHARING:
   ensures the SAME computation happens at every step
   (one set of weights, applied many times)

UNFOLDING:
   visualises the full sequence as a chain of identical cells
   (showing the depth of the temporal computation)

Together:
   one cell × weight sharing × unfolding = an RNN
```

The cell is the **molecule**. Weight sharing is the **rule** for stacking it. Unfolding is the **visualisation** showing how it spans time.

---

## In PyTorch

```python
import torch
import torch.nn as nn

# Define an RNN cell (or use the built-in)
rnn_cell = nn.RNNCell(input_size=100, hidden_size=128)

# Initial hidden state (zeros)
batch_size = 32
h = torch.zeros(batch_size, 128)

# Process a sequence of 10 time steps
sequence = torch.randn(10, batch_size, 100)   # (T, batch, input_dim)

for t in range(10):
    h = rnn_cell(sequence[t], h)              # SAME cell every time step

# Or use the full RNN layer (handles the loop internally)
rnn = nn.RNN(input_size=100, hidden_size=128, batch_first=True)
sequence = torch.randn(batch_size, 10, 100)   # (batch, T, input_dim)
output, h_final = rnn(sequence)               # output: (batch, T, 128)
                                                # h_final: (1, batch, 128)
```

`nn.RNNCell` exposes the cell; `nn.RNN` handles the unrolling for you internally.

---

## Common Misconceptions

```
✗ "RNN has many cells"
   → NO, it has ONE cell applied many times.
   → Weight sharing is THE feature of RNNs.

✗ "Each time step has its own weights"
   → NO, every step uses identical weights.

✗ "Unfolding adds parameters"
   → NO, unfolding is just a VISUALISATION.
   → Parameter count stays the same regardless of sequence length.

✗ "The hidden state is reset each time step"
   → NO, it's CARRIED FORWARD.
   → It's reset only between sequences (between training examples).
```

---

## Why Model Size Doesn't Grow with Sequence Length

The most important consequence of weight sharing:

```
RNN size = the cell's weights (W_x, W_h, W_y, b)
         = FIXED — doesn't grow with sequence length

   Sequence of 5    → same model size
   Sequence of 100  → same model size  
   Sequence of 1000 → SAME model size
```

### The Key Insight

When you unfold the RNN, the diagram **looks** like T separate networks. But they're **not**:

```
The same W_x, W_h, W_y, b appear in EVERY box.
   → only ONE set of weights exists in memory
   → the cell is REUSED at each time step
   → unfolding is just a VISUALISATION, not duplication
```

### Concrete Math

```
For input_dim=100, hidden_dim=128, output_dim=10:
   W_x:    128 × 100 = 12,800
   W_h:    128 × 128 = 16,384
   W_y:    10 × 128  = 1,280
   biases: ~266
   Total: ~30,730 params

Sequence of 5:    30,730 params, 5 cell applications
Sequence of 1000: 30,730 params, 1000 cell applications

→ Length grows. Parameters don't.
```

### Compare to MLP (which CAN'T do this)

```
MLP on sequence of length T:
   First layer: T × input_dim features (concatenated)
   Need separate weights from EACH position to hidden layer.

Length 5:    5 × 100 × 128 = 64,000 params
Length 100:  100 × 100 × 128 = 1.28M params  
Length 1000: 100M+ params

Worse: changing sequence length requires REBUILDING THE MODEL.
```

This is exactly the problem RNNs solve.

### What DOES Grow with Sequence Length

| | Grows with length? |
|-|--------------------|
| Model parameters | ❌ NO — fixed |
| Forward computation time | ✅ YES — T steps |
| Memory during training (activations) | ✅ YES — store all h_t for backprop |
| Inference time | ✅ YES — sequential processing |

So:
- The **model** is small and constant
- The **work** (compute, activation memory) scales with length

This is why RNNs are slow on long sequences — not because of parameters, but because of **sequential processing**.

### Verify in PyTorch

```python
import torch.nn as nn
import torch

rnn = nn.RNN(input_size=100, hidden_size=128, batch_first=True)
total = sum(p.numel() for p in rnn.parameters())
print(f"Total parameters: {total}")
# ~29,440 — REGARDLESS of sequence length

# Try with different sequence lengths
x_short = torch.randn(1, 5, 100)     # length 5
x_long  = torch.randn(1, 1000, 100)  # length 1000

out_short, _ = rnn(x_short)
out_long, _  = rnn(x_long)
# Same model, different inputs, SAME parameter count.
```

---

## Advantages and Disadvantages of RNN

### Advantages

```
✓ HANDLES VARIABLE-LENGTH INPUT
   - Same cell processes 5-word or 5000-word sequences
   - No need for fixed-size padding

✓ FIXED MODEL SIZE
   - Parameter count independent of sequence length
   - Tiny model can process huge sequences
   - Easy to deploy on memory-constrained devices

✓ CAPTURES TEMPORAL DEPENDENCIES
   - Hidden state carries history forward
   - Context-aware predictions at each step

✓ WEIGHT SHARING ACROSS TIME
   - Patterns learned at one position apply at all others
   - Transfer of knowledge across time steps
   - Translation-in-time invariance (similar to CNN's space invariance)

✓ NATURAL FIT for sequential tasks
   - NLP, speech, time series, music
   - Anything where order matters

✓ STREAMING INFERENCE
   - Can process one token at a time
   - Good for real-time applications (predictive text, online speech recognition)

✓ INTUITIVE
   - Mirrors how humans process sequences (one element at a time)
```

### Disadvantages

```
✗ VANISHING / EXPLODING GRADIENTS
   - Long sequences → repeated multiplication of gradients
   - Vanilla RNNs fail beyond ~20 time steps
   - Fix: LSTM / GRU / gradient clipping

✗ SEQUENTIAL PROCESSING (NOT PARALLELISABLE)
   - Step t needs h_{t-1} → can't compute steps in parallel
   - GPU utilisation is poor compared to CNNs / Transformers
   - Training and inference are SLOW

✗ DIFFICULTY WITH LONG-RANGE DEPENDENCIES
   - "The cat that I saw in the park yesterday ... was beautiful"
   - Information at start of sentence has to travel through many cells
   - Often lost or distorted by the time it reaches relevant later position
   - Even LSTM struggles with > ~100 time steps

✗ MEMORY DURING TRAINING
   - BPTT requires storing all hidden states for backprop
   - Memory grows linearly with sequence length
   - Truncated BPTT helps but introduces approximation

✗ EXPENSIVE INFERENCE FOR LONG SEQUENCES
   - Can't skip ahead — must process every step
   - Latency = sum of all step times

✗ HARDER TO INTERPRET
   - Hidden state mixes everything that's happened
   - Hard to see "what the model is remembering"
   - Less interpretable than attention-based models

✗ NOT EASILY EXTENDABLE
   - Hard to add hierarchical / multi-scale processing
   - Transformers handle this better via attention heads

✗ LARGELY REPLACED BY TRANSFORMERS
   - Modern NLP / speech uses Transformers (BERT, GPT, Whisper)
   - RNNs remain only in niche areas (small models, streaming, time series)
```

### When to Use RNN vs Alternatives

| Situation | Best choice |
|-----------|-------------|
| Variable-length sequences, modest scale | LSTM / GRU |
| Long-range dependencies, lots of data | Transformer |
| Time series forecasting | LSTM (still competitive) |
| Streaming / online inference | RNN / LSTM |
| Small-data scenarios | LSTM (fewer params than Transformer) |
| Resource-constrained device | LSTM (smaller than Transformer) |
| State-of-the-art NLP / speech | Transformer (always) |

```
Rule of thumb:
   - Use Transformer when you can afford the compute and data
   - Use LSTM when you need a smaller, simpler model
   - Vanilla RNN: only for teaching / understanding
```

---

## Summary

```
RNN CELL ANATOMY:
   h_t = activation(W_x·x_t + W_h·h_{t-1} + b)
   → takes input + previous state → produces new state
   → optional output y_t = W_y·h_t + b_y

WEIGHT SHARING (the "symmetry"):
   Same W_x, W_h, W_y, b used at EVERY time step.
   → enables variable-length sequences
   → keeps parameter count independent of length
   → analogous to CNN weight sharing across space

UNFOLDING:
   The recurrent loop visualised as T separate cells.
   → reveals the depth of computation
   → enables backprop (BPTT)
   → makes weight sharing visible
   → the same network — just drawn differently
```

> The RNN cell is **one cell with a loop**, applied at every time step with the **same weights**. Unfolding makes that explicit. Master these three concepts and the rest of RNNs (BPTT, LSTM, GRU) follows naturally.
