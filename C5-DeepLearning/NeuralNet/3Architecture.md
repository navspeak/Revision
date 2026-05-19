# Neural Network Architecture

The **architecture** is the structural blueprint of a network — number of layers, neurons per layer, how they're connected.

```
Input Layer  →  Hidden Layer(s)  →  Output Layer
                       ↑
              this is where the magic happens
```

---

## Basic Components

| Component | Description | Role |
|-----------|-------------|------|
| **Input layer** | Receives raw data | Entry point — one neuron per feature |
| **Hidden layer(s)** | Intermediate computations | Extract features, learn patterns |
| **Output layer** | Produces final prediction | Class probabilities, regression values, etc. |
| **Connections (weights)** | Links between neurons | Learnable parameters that capture relationships |
| **Bias** | Constant added per neuron | Shifts activation independently of inputs |
| **Activation function** | Non-linear transformation | Gives the network its expressive power |

---

## Typical Feedforward Architecture

In a **fully connected** (dense) layer, EVERY input connects to EVERY neuron in the next layer.

```
        [Input]               [Hidden 1]            [Output]

        x₁  ⬢ ─┬───┬───┬──►  ⬢ ─┬───┬──►  ŷ₁  ⬢
               │   │   │       │   │
        x₂  ⬢ ─┼───┼───┼──►  ⬢ ─┼───┼──►  ŷ₂  ⬢
               │   │   │       │   │
        x₃  ⬢ ─┼───┼───┼──►  ⬢ ─┘   │
               │   │   │           
        x₄  ⬢ ─┴───┴───┴──►        

        4 inputs ───────► 3 hidden neurons ───────► 2 outputs

   Every x connects to ALL 3 hidden neurons (4 × 3 = 12 weights)
   Every hidden neuron connects to ALL 2 output neurons (3 × 2 = 6 weights)
```

Equivalent diagram in matrix form — every connection is one weight:

```
        x₁    x₂    x₃    x₄
        │     │     │     │
  ┌─────┴─────┴─────┴─────┴─────┐
  │  Hidden neuron 1            │   ← combines ALL inputs:
  │  z₁ = w₁₁x₁ + w₁₂x₂ + w₁₃x₃ + w₁₄x₄ + b₁
  └─────────────────────────────┘
  ┌─────────────────────────────┐
  │  Hidden neuron 2            │   ← also combines ALL inputs
  │  z₂ = w₂₁x₁ + w₂₂x₂ + w₂₃x₃ + w₂₄x₄ + b₂
  └─────────────────────────────┘
  ┌─────────────────────────────┐
  │  Hidden neuron 3            │
  │  z₃ = w₃₁x₁ + w₃₂x₂ + w₃₃x₃ + w₃₄x₄ + b₃
  └─────────────────────────────┘
```

Each of the 3 hidden neurons gets **all 4 inputs** — that's the meaning of "fully connected".

Information flows **left to right** only (feedforward — no cycles).

---

## Mathematical Flow

For a given layer `l`:

```
z⁽ˡ⁾ = W⁽ˡ⁾ · a⁽ˡ⁻¹⁾ + b⁽ˡ⁾
a⁽ˡ⁾ = σ(z⁽ˡ⁾)
```

Where:
- `W⁽ˡ⁾` = weight matrix for layer `l`
- `a⁽ˡ⁻¹⁾` = activation from previous layer (input from previous layer's output)
- `b⁽ˡ⁾` = bias vector for layer `l`
- `σ` = activation function (ReLU, sigmoid, etc.)
- `a⁽ˡ⁾` = output of layer `l` — fed into layer `l+1`

The network computes layer by layer until reaching the output.

---

## Size Computation

Number of parameters in a fully-connected layer:

```
For a layer with n_in inputs and n_out outputs:

  Weights:  n_in × n_out
  Biases:   n_out
  
  Total:    n_in × n_out + n_out
        =   n_out × (n_in + 1)
```

### Example

A 4 → 3 → 2 network has:

```
Layer 1 (4 → 3):  4×3 + 3 = 15 params
Layer 2 (3 → 2):  3×2 + 2 = 8 params
Total: 23 parameters
```

Deep networks have **millions to billions** of parameters.

---

## Information Flow

```
Input  → x = [x₁, x₂, x₃, x₄]
         ↓ (multiply by W⁽¹⁾, add b⁽¹⁾, apply σ)
Hidden 1 = a⁽¹⁾ = [a₁, a₂, a₃]
         ↓
Hidden 2 = a⁽²⁾ = [a₁, a₂, a₃]
         ↓
Output   = a⁽³⁾ = ŷ = [ŷ₁, ŷ₂]
```

Each layer transforms the data into a **new representation** — features become more abstract as we go deeper.

---

## Hyperparameters Defining Architecture

| Hyperparameter | Purpose |
|----------------|---------|
| **Number of layers** | Determines depth and learning capacity |
| **Neurons per layer** | Controls representational power |
| **Activation function** | Governs non-linearity |
| **Initialisation strategy** | Affects convergence (e.g., Xavier, He) |
| **Loss function** | What the network optimises |
| **Optimizer** | How weights are updated |

These are **set by you** before training, not learned by the network.

---

## Architectural Intuition

Depth vs width — they capture different things:

```
Wider  (more neurons per layer)     → more capacity for parallel features
Deeper (more layers)                → more abstraction levels

Same number of parameters:
   wide+shallow → memorises specific patterns
   narrow+deep → learns hierarchical features (generally preferred)
```

For most tasks, **depth wins** — that's why "deep learning" is "deep".

---

## Example: Image Model

```
Input        → 28×28 grayscale image (784 pixel values)
Hidden 1     → 128 neurons (detects edges)
Hidden 2     → 64 neurons (detects shapes)
Hidden 3     → 32 neurons (detects digits / parts)
Output       → 10 neurons (one per digit 0–9)
```

Each layer builds on the previous one's features. Output is a probability distribution over 10 classes.

---

## Deep Architectures: Advantages

| Aspect | Benefit |
|--------|---------|
| **Hierarchical learning** | Captures simple and complex patterns |
| **Generalisation power** | Adapts to diverse input types |
| **Automatic feature extraction** | Reduces need for manual engineering |
| **Composability** | Building blocks (layers) can be reused / combined |
| **State-of-the-art accuracy** | On vision, language, speech tasks |

Deep architectures dominate the AI landscape — from ResNets in vision to Transformers in NLP.

---

## What Layers Learn

Image classification example:

```
Layer 1:  edges, lines, basic textures
Layer 2:  shapes, corners, simple patterns
Layer 3:  object parts (eyes, wheels, leaves)
Layer 4:  whole objects (faces, cars, plants)
Layer 5:  scenes and context
```

NLP example (sentiment analysis):

```
Layer 1:  individual word embeddings
Layer 2:  short phrases ("not good", "very much")
Layer 3:  clauses and modifiers
Layer 4:  overall sentiment
```

**Each layer abstracts away from the surface and toward meaning.** This is why deep learning generalises so well — the network discovers natural hierarchies in the data.

---

## Choosing Architecture

| Task complexity | Suggested depth |
|----------------|-----------------|
| Simple (linear-ish patterns) | 1–2 hidden layers |
| Moderate (some non-linearity) | 3–5 layers |
| Complex (images, language) | 10+ layers (often 50+) |
| State-of-the-art | Hundreds to thousands of layers (with skip connections) |

---

## Effect of Hidden Layer Size

| Size | Impact |
|------|--------|
| **Too small** | Underfits — can't capture complex patterns |
| **Balanced** | Good generalisation |
| **Too large** | Overfits — memorises training data |

Both depth and width matter. Together, they define the network's **capacity**.

---

## Summary

```
Architecture = blueprint of the network:
   - Number of layers
   - Number of neurons per layer
   - How neurons are connected (fully connected, convolutional, recurrent)
   - Activation functions per layer

Information flows:
   z⁽ˡ⁾ = W⁽ˡ⁾ · a⁽ˡ⁻¹⁾ + b⁽ˡ⁾
   a⁽ˡ⁾ = σ(z⁽ˡ⁾)

Depth provides hierarchical learning;
width provides parallel feature capacity.

Choosing architecture is part art, part empirical experimentation.
```

> The architecture is the network's "shape". The weights are the network's "soul" — learned during training.
