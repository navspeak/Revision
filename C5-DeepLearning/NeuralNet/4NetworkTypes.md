# Neural Network Architecture Types

Different problems need different network designs. Three foundational families:

```
Feedforward (FNN)    →  general-purpose, classification / regression
Convolutional (CNN)  →  images, video, spatial data
Recurrent (RNN)       →  sequences, text, time-series
```

Plus modern specialisations: Transformers, GANs, GNNs, etc.

---

## Feedforward Network (FNN / MLP)

**The baseline neural network.** Information flows **one direction only** — input to output, no cycles.

```
Input → Hidden 1 → Hidden 2 → ... → Output
```

Also called:
- Fully connected network (every neuron in layer L connects to every neuron in layer L+1)
- Multi-Layer Perceptron (MLP)
- Dense network

### Key Feature

```
Unidirectional flow
Every neuron in each layer connected to every neuron in next
```

### Use Cases

- Tabular data classification / regression
- Simple binary or multiclass prediction
- Baseline for any structured-data problem
- Last layers of more complex networks (CNN, Transformer)

### Limitations

```
✗ Doesn't exploit spatial structure (treats image pixels as independent)
✗ Doesn't handle sequences naturally (no memory)
✗ Parameter count explodes for high-dimensional input
```

For a 256×256 RGB image:

```
Input dimension: 256 × 256 × 3 = 196,608 values
First hidden layer with 1000 neurons: 196,608 × 1000 ≈ 200 million parameters
```

That's just the first layer — clearly inefficient for images. Hence CNNs.

---

## Convolutional Neural Network (CNN)

Specialised for **spatial data** — images, video, audio spectrograms.

### Key Idea

Instead of connecting every input pixel to every neuron, use **convolutional filters** that scan local regions:

```
Filter (kernel) of size 3×3 slides over the image
Each filter detects a LOCAL pattern (edge, corner, texture)
Filters share weights across positions → far fewer parameters
```

### Key Features

```
✓ Captures LOCAL patterns (an edge looks the same anywhere in the image)
✓ Translation invariant — a cat is a cat wherever it appears
✓ Weight sharing — millions of pixel inputs, only thousands of parameters
✓ Hierarchical features — early layers detect edges, later layers detect objects
```

### Typical CNN Structure

```
Input image
   ↓
Convolutional layer → applies many filters
   ↓
Pooling layer → reduces spatial size
   ↓
Convolutional layer
   ↓
Pooling layer
   ...
   ↓
Flatten → Fully-connected layers
   ↓
Output (class probabilities)
```

### Use Cases

```
Image classification    (cat vs dog, digit recognition)
Object detection         (where are the cars in this image?)
Semantic segmentation    (which pixels are road / sky / building?)
Medical imaging          (tumour detection in X-rays)
Face recognition
Style transfer
```

### Famous CNN Architectures

```
LeNet (1998)      → digits — the original CNN
AlexNet (2012)    → ImageNet breakthrough
VGG, ResNet       → deeper and more accurate
Inception         → wider receptive fields
EfficientNet      → scaled balance
Vision Transformers (ViT) → eventually superseded CNNs in some tasks
```

---

## Recurrent Neural Network (RNN)

Specialised for **sequential data** — text, speech, time-series.

### Key Idea

A neuron's output is fed back as input for the **next time step**, giving the network **memory** of past inputs:

```
Time t-1:  input → [hidden state h_{t-1}] → output
                          ↓
Time t:    input → [hidden state h_t] → output
                          ↓
Time t+1:  input → [hidden state h_{t+1}] → output
```

The hidden state acts as the network's memory — it "remembers" what happened earlier.

### Key Features

```
✓ Handles VARIABLE-LENGTH sequences
✓ Maintains internal state (memory)
✓ Captures temporal patterns
```

### Limitations

```
✗ Vanishing / exploding gradients on long sequences
✗ Sequential processing — hard to parallelise
✗ Long-range dependencies are hard
```

These limitations led to **LSTM** and **GRU** (gated variants of RNN), and ultimately to **Transformers** (which replaced RNNs for most NLP tasks).

### Use Cases

```
Text (NLP)               → translation, generation, classification
Speech recognition       → audio → text
Time-series forecasting  → stock prices, weather, sensor data
Sequence labelling       → POS tagging, named entity recognition
Music generation         → notes / waveforms
```

---

## Side-by-Side Comparison

| | Feedforward | CNN | RNN |
|-|-------------|-----|-----|
| **Best for** | Tabular / structured | Spatial (images, audio) | Sequential (text, time) |
| **Key operation** | Matrix multiply | Convolution | Recurrent state update |
| **Captures** | Direct relationships | Local spatial patterns | Temporal dependencies |
| **Weight sharing** | No | Yes (across positions) | Yes (across time) |
| **Handles variable input?** | Fixed | Fixed | Variable |
| **Memory** | None | None | Yes — internal state |
| **Parallelisable** | Yes | Yes | No (sequential by nature) |

---

## Modern Architectures

| Type | Built on | Best for |
|------|----------|----------|
| **Transformer** | Attention mechanism | NLP (GPT, BERT) and now images (ViT) |
| **GAN** | Two competing FNNs/CNNs | Generative modelling (images, audio) |
| **Autoencoder** | Encoder + Decoder | Unsupervised learning, denoising |
| **Graph Neural Network (GNN)** | Message passing over graphs | Social networks, molecules |
| **U-Net** | Encoder-decoder with skips | Image segmentation, medical imaging |
| **Diffusion Models** | Iterative denoising | Image generation (Stable Diffusion) |

Most state-of-the-art systems today are **Transformer-based** — for both language and increasingly vision.

---

## Choosing the Right Architecture

```
Tabular data with mixed features  → Feedforward (or gradient boosting often wins)
Images / video                     → CNN or Vision Transformer
Text / sequences                   → Transformer (was RNN/LSTM)
Time-series                        → LSTM, Transformer, or even feedforward
Graph data                         → GNN
Generative tasks                   → GAN, VAE, Diffusion, autoregressive LMs
```

For most modern problems, **start with a pretrained Transformer** and fine-tune. CNN if vision, RNN/LSTM if you need a simpler baseline on sequences.

---

## Summary

```
Feedforward (FNN/MLP)  → all-to-all connections, baseline
CNN                     → spatial / image data via convolutions
RNN                     → sequential / text data via recurrence

Each exploits structure in its data type:
   FNN  → assumes no structure
   CNN  → exploits spatial / local structure
   RNN  → exploits temporal / sequential structure

Modern AI mostly uses Transformers (which combine ideas from all three).
```

> Choose the architecture that **matches the structure of your data**. Images → CNN. Sequences → RNN/Transformer. Tables → FNN.
