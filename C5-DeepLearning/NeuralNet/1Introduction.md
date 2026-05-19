# Introduction to Neural Networks

A **Neural Network** is a computational model inspired by how the human brain processes information — interconnected "neurons" (nodes) organised in layers that learn from data.

```
Input → Layers of neurons → Output

Each neuron computes a weighted sum + non-linearity
Each layer transforms its input into a richer representation
The final layer produces a prediction
```

---

## In Simple Terms

```
Linear regression:    output = w₁x₁ + w₂x₂ + ... + b   (one linear formula)

Neural network:       MANY such linear units stacked,
                      each followed by a non-linearity,
                      organised in LAYERS,
                      learning HIERARCHICAL representations.
```

A single neuron is like logistic regression. A network is **many neurons combined** — and that combination unlocks the ability to learn anything from images to language to game strategy.

---

## Motivation

Why neural networks instead of simpler models?

```
✓ Learn from MASSIVE data
✓ Capture complex, NON-LINEAR patterns automatically
✓ Discover features without manual engineering
✓ Adapt across domains: vision, speech, language, time-series
✓ Scale with hardware (GPUs, TPUs)
```

Simple models (linear/logistic regression, trees) hit a ceiling on tasks where the input is high-dimensional and structured (images, audio, text). Neural networks **break through** that ceiling.

---

## Core Components

```
Input layer        → receives raw data
Hidden layer(s)    → compute weighted transformations
Output layer       → produces prediction
Weights and biases → parameters the network LEARNS
Activation function → adds non-linearity (without it, the network is just linear)
Loss function       → measures how wrong predictions are
Optimizer           → updates weights to reduce loss
```

---

## Layered Decision Process — Analogy

Think of a neural network as a layered decision process:

```
Layer 1: "is this a curve or a line?"     ← detects edges
Layer 2: "is this an eye or an ear?"      ← combines edges into parts
Layer 3: "is this a face?"                 ← combines parts into objects
Layer 4: "whose face is this?"             ← higher-level reasoning
```

Each layer builds on the previous one's output. Shallow features → mid-level features → high-level concepts.

---

## NLP Task Example

```
Input:  "I loved the movie"
        ↓ (tokenization, embedding)
   [vectors of numbers]
        ↓ (hidden layers extract features)
   [sentiment-related features]
        ↓ (output layer)
   "positive" with 92% confidence
```

The network learns what "positive" looks like in feature space without you defining the rules.

---

## Mathematical Perspective

### For a single neuron

```
z = (w₁·x₁ + w₂·x₂ + ... + w_n·x_n) + b

a = activation(z)
```

- `xᵢ` = inputs from previous layer
- `wᵢ` = learnable weights
- `b` = learnable bias
- `activation` = non-linear function (ReLU, sigmoid, etc.)
- `a` = output of this neuron

### For a full network

```
Layer 1:  a^(1) = activation( W^(1) · x  + b^(1) )
Layer 2:  a^(2) = activation( W^(2) · a^(1) + b^(2) )
...
Layer L:  ŷ    = activation( W^(L) · a^(L−1) + b^(L) )
```

Each layer is a matrix multiplication followed by element-wise non-linearity.

---

## Why Neural Networks Are Powerful

```
✓ Universal approximators
   → with enough layers/neurons, can approximate any function

✓ Automatic feature extraction
   → no need for hand-crafted features (unlike classical ML)

✓ Hierarchical learning
   → simple → complex representations naturally

✓ Same architecture handles diverse modalities
   → image, text, speech, structured data
```

The **Universal Approximation Theorem** says: a network with a single hidden layer (with enough neurons) and a non-linear activation can approximate any continuous function. Deep networks are more **efficient** at this than shallow ones.

---

## Applications

```
Computer Vision        → image classification, object detection, segmentation
Natural Language       → translation, sentiment, summarization, chatbots
Speech                  → recognition, synthesis (text-to-speech)
Recommendation         → Netflix, Amazon, YouTube
Healthcare              → diagnostic imaging, drug discovery
Finance                 → fraud detection, algorithmic trading
Robotics                → control, perception
Games                   → AlphaGo, AlphaStar, OpenAI Five
```

Neural networks are the **default tool** for any AI problem with rich input data and enough labelled examples.

---

## Limitations

| Aspect | Challenge |
|--------|-----------|
| **Data hungry** | Need large volumes of training data |
| **Compute expensive** | GPUs / TPUs needed for training |
| **Black box** | Hard to interpret internal workings |
| **Overfitting** | Memorise training data without regularisation |
| **Brittle** | Small input changes can flip output (adversarial examples) |
| **Energy cost** | Training large models consumes significant electricity |

These motivate research in interpretability, sample-efficient learning, and model compression.

---

## Simple Example — One Neuron

Imagine a binary classifier with 2 features:

```
Inputs:  x₁ = 0.5,  x₂ = 1.0
Weights: w₁ = 0.4,  w₂ = 0.6
Bias:    b = -0.2

z = 0.5 × 0.4 + 1.0 × 0.6 + (-0.2)
  = 0.2 + 0.6 - 0.2
  = 0.6

Apply sigmoid: a = 1 / (1 + e^(-0.6)) ≈ 0.646

Predict: "positive class" (since 0.646 > 0.5)
```

A network is just **thousands or millions of such computations** chained together.

---

## Summary

```
Neural Network = layered system of artificial neurons
   → each neuron: weighted sum + non-linear activation
   → each layer: transforms input into a richer representation
   → final layer: produces prediction

Components: weights, biases, activations, loss, optimizer

Strengths: universal approximation, auto feature extraction, scales with data
Limitations: data-hungry, compute-expensive, hard to interpret
```

> Neural networks are the engine of modern AI. They look complex but reduce to repeated matrix multiplications and non-linear activations — the rest is just clever organisation and training.
