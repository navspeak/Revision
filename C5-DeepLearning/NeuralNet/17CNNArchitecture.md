# CNN Architecture — Feature Extractor + Classifier

A typical CNN has two parts that work together:

```
INPUT IMAGE → [FEATURE EXTRACTOR] → [CLASSIFIER] → PREDICTION
              (conv + pool layers)    (FC layers)
              "base" / "body"          "head"
```

Understanding this split is the key to understanding any CNN, from LeNet (1998) to ResNet (2015) to Vision Transformers (2020s).

---

## The VGG16 Example

VGG16 — published in 2014, named for its **16 layers** — is the canonical CNN architecture for teaching:

```
Input: 224 × 224 × 3 (RGB image)
   ↓
   [Conv + ReLU] × 2  → 224 × 224 × 64
   [Pool]              → 112 × 112 × 64
   ↓
   [Conv + ReLU] × 2  → 112 × 112 × 128
   [Pool]              → 56 × 56 × 128
   ↓
   [Conv + ReLU] × 3  → 56 × 56 × 256
   [Pool]              → 28 × 28 × 256
   ↓
   [Conv + ReLU] × 3  → 28 × 28 × 512
   [Pool]              → 14 × 14 × 512
   ↓
   [Conv + ReLU] × 3  → 14 × 14 × 512
   [Pool]              → 7 × 7 × 512
   ↓
   [Flatten] → 25088
   [Fully Connected] → 4096
   [Fully Connected] → 4096
   [Fully Connected] → 1000 (classes)
   [Softmax] → probabilities

         ↑                         ↑
   FEATURE EXTRACTOR           CLASSIFIER
   (body)                       (head)
```

The pattern is **conv blocks getting deeper but smaller**, then dense layers for the final classification.

---

## Part 1 — Feature Extractor (Body)

The body's job: **convert pixels into useful features**.

```
Tools used:
   ✓ Convolutional layers     → detect patterns
   ✓ ReLU activations          → add non-linearity
   ✓ Pooling layers            → downsample, add invariance

Goal: build a hierarchy of features
   Layer 1:  edges, simple gradients
   Layer 2:  textures, shapes
   Layer 3:  object parts (eyes, wheels)
   Layer 4:  whole objects
```

This part is **task-agnostic** — pretrained feature extractors work across many tasks (image classification, detection, segmentation).

---

## Part 2 — Classifier (Head)

The head's job: **take the extracted features and produce the final prediction**.

```
Tools used:
   ✓ Flatten          → 2D feature maps → 1D vector
   ✓ Fully connected (Dense) layers  → standard MLP
   ✓ Softmax (or sigmoid)             → output activation
```

This part is **task-specific** — change the number of output neurons to match your task (10 classes vs 100, classification vs regression, etc.).

---

## Why "Dense" = "Fully Connected"

```
"Dense layer" and "Fully connected layer" mean the SAME THING.
Every neuron is connected to every neuron in the previous layer.

A "dense" connectivity pattern → "dense layer".
```

It's just terminology — Keras calls them `Dense`, PyTorch calls them `Linear`, papers call them "FC". Same thing.

---

## The Three Layer Types

Every CNN is built from three layer types:

| Layer | What it does | In feature extractor or classifier? |
|-------|-------------|--------------------------------------|
| **Convolutional** | Slides filters to detect patterns | Body |
| **Pooling** | Downsamples and adds invariance | Body |
| **Fully Connected (Dense)** | Combines features into predictions | Head |

In VGG16: blue blocks = Conv + ReLU + Pool (body), then dense layers (head).

---

## What Happens in a Conv Layer (Recap)

A convolutional layer performs:

```
1. CONVOLUTION  — sum of products between filter and image patch
2. ACTIVATION   — ReLU adds non-linearity
```

Without the activation, **stacking conv layers = one giant linear operation** (no power). ReLU breaks this and lets the network learn complex patterns.

```
Layer output = ReLU(Conv(input))
```

---

## Receptive Field

The **receptive field** is the region of the **input image** that contributes to one output value.

```
3×3 filter at layer 1 → receptive field = 3×3 in the original image
   The output value "sees" 9 pixels.

Stack a 2nd 3×3 conv layer:
   Each output of layer 2 sees a 3×3 patch of layer 1.
   But each layer-1 value already saw 3×3 input pixels.
   → Layer 2's effective receptive field = 5×5 in the original image.

Stack more layers:
   Receptive field GROWS with depth.
   Deep layers "see" most of the image.
```

This is why deep networks can detect large objects — by stacking many small filters, the effective receptive field becomes huge.

```
Layer 1:    3×3   (sees 9 pixels)
Layer 2:    5×5   (sees 25 pixels)
Layer 3:    7×7   (sees 49 pixels)
...
Layer 16:   covers most of the image
```

---

## Convolution on RGB Images — Channel Matching

```
Input RGB image:  224 × 224 × 3
   ↑   ↑   ↑
   H   W   channels (R, G, B)

Filter must match channel dimension:
   Filter shape: 3 × 3 × 3
                 ↑   ↑   ↑
                 H   W   channels (matches input)
```

**Rule:** filter's channel dimension MUST equal input's channel dimension.

What happens at one position:

```
Image patch  (3×3×3)
Filter       (3×3×3)
                       ↓ element-wise multiply
Products      (3×3×3 = 27 numbers)
                       ↓ sum
Output value   1 scalar
```

Despite operating on 3 channels, the output of ONE filter at ONE position is **one number** — because we sum everything.

---

## Counting Parameters in a Conv Layer

The number of learnable parameters in a conv layer:

```
Parameters = (number_of_filters × filter_height × filter_width × input_channels) + biases
           = number_of_filters × (F × F × C_in + 1)
                                                  ↑
                                            +1 bias per filter
```

### Worked Example

For one 3×3×3 filter on a 224×224×3 RGB image:

```
Weights:  3 × 3 × 3 = 27
Bias:     1 per filter
Total:    27 + 1 = 28 parameters per filter
```

For 64 filters (typical first layer):

```
64 × (3 × 3 × 3) + 64 = 64 × 27 + 64 = 1,728 + 64 = 1,792 parameters
```

### Why So Few?

Same filter slides across the whole 224×224 image. **Weight sharing** means we don't pay for each position separately.

Compare to an equivalent fully-connected layer:

```
FC layer from 224×224×3 → 64 neurons:
   weights = 224 × 224 × 3 × 64 = 9,633,792
   biases = 64
   Total = ~9.6 million parameters

CNN layer doing similar feature extraction:
   1,792 parameters ← 5400× smaller!
```

That's why CNNs scale to large images while MLPs can't.

---

## Padding — Zero Padding vs Identity Padding

Padding adds extra rows/columns of pixels around the image edges.

### Zero Padding (default in deep learning)

```
Original 5×5 image:           After zero padding (P=1):
  ┌─┬─┬─┬─┬─┐                  ┌─┬─┬─┬─┬─┬─┬─┐
  │1│2│3│4│5│                  │0│0│0│0│0│0│0│
  ├─┼─┼─┼─┼─┤                  ├─┼─┼─┼─┼─┼─┼─┤
  │6│7│8│9│0│                  │0│1│2│3│4│5│0│
  ├─┼─┼─┼─┼─┤                  ├─┼─┼─┼─┼─┼─┼─┤
  │1│2│3│4│5│                  │0│6│7│8│9│0│0│
  ├─┼─┼─┼─┼─┤                  ├─┼─┼─┼─┼─┼─┼─┤
  │6│7│8│9│0│                  │0│1│2│3│4│5│0│
  ├─┼─┼─┼─┼─┤                  ├─┼─┼─┼─┼─┼─┼─┤
  │1│2│3│4│5│                  │0│6│7│8│9│0│0│
  └─┴─┴─┴─┴─┘                  ├─┼─┼─┼─┼─┼─┼─┤
                                │0│1│2│3│4│5│0│
                                ├─┼─┼─┼─┼─┼─┼─┤
                                │0│0│0│0│0│0│0│
                                └─┴─┴─┴─┴─┴─┴─┘
```

Fills the border with zeros.

### Identity Padding (Edge Replication)

```
Replicates the border pixels instead of zeros.
```

### Why Prefer Zero Padding?

```
✓ Adds no extra information
   In the sum-of-product operation: 0 × anything = 0
   → doesn't bias the convolution

✗ Identity padding REPLICATES existing pixels
   → can artificially amplify edge information
```

**In practice, zero padding is the default** in nearly all modern frameworks and architectures.

### When to Use Padding

```
P = 0  (no padding):
   - Output gets smaller each conv layer
   - Edge pixels see fewer filter applications
   - Used in early layers when you WANT to shrink

P = 1 (with 3×3 filter, stride 1):
   - "same" padding — preserves spatial size
   - Standard in deep networks (VGG, ResNet)
   - Output size = input size

Rule of thumb: P = (F-1) / 2 for "same" padding
   - F=3 → P=1
   - F=5 → P=2
   - F=7 → P=3
```

---

## Output Size Recap

```
            N − F + 2P
Output = ─────────────── + 1
                S
```

| Parameter | Symbol | Typical |
|-----------|--------|---------|
| Input size | N | 224 |
| Filter size | F | 3 or 5 |
| Padding | P | 0 or 1 |
| Stride | S | 1 or 2 |

See `16ConvolutionFilter.md` for full examples.

---

## The Typical CNN Block

Modern CNNs are built from repeating "blocks":

```
Block = Conv → BatchNorm → ReLU → (Conv → BatchNorm → ReLU)... → Pool

Repeat the block several times. Each block:
   - Keeps spatial size same (with padding=1, stride=1)
   - Doubles the number of channels
   - Then pool halves the spatial size

Example:
   Block 1: 224×224×64
   Block 2: 112×112×128
   Block 3: 56×56×256
   ...
```

The pattern: **spatial dimensions shrink, channel depth grows**.

---

## Why Spatial Down, Channels Up?

```
Early layers: many spatial details, few feature types
   → 224 × 224 spatial, 64 channels (simple features)

Late layers: few spatial details, many feature types
   → 7 × 7 spatial, 512 channels (complex concepts)
```

The information is **traded** from spatial position to feature richness as we go deeper.

---

## What the Network Produces

After the feature extractor, you have a 3D tensor of feature maps:

```
Final feature map: 7 × 7 × 512
   = 7×7 grid of locations, each with 512-channel feature vector
```

This is **flattened** (7×7×512 = 25,088 values) and fed to the classifier (dense layers + softmax) to produce the final prediction.

---

## Summary

```
CNN architecture = two parts:
   Feature Extractor (body): conv + ReLU + pool layers
   Classifier (head): dense (fully connected) layers + softmax

Each Conv layer:
   Output = ReLU(Convolution(input))
   Receptive field grows with depth
   Channel dimension of filter MUST match input

Parameter count per conv layer:
   filters × (F × F × C_in + 1)
   ← weight sharing → drastically fewer than FC

Padding:
   Zero padding (default) — adds no info
   Identity padding — replicates edges (rare)

Output size: (N − F + 2P) / S + 1
```

> A CNN is just **feature extraction + classification glued together**. The feature extractor learns to see; the classifier learns to decide. Mastering this two-part structure is the foundation of every CNN, from VGG to ResNet to modern Vision Transformers.
