# Convolutional Filters

**Convolutional filters** = small matrices of weights that slide across an image, detecting specific patterns at each position.

```
Filter = a small grid of learnable weights (typically 3×3 or 5×5)
       = a "pattern detector"

Apply it everywhere in the image → produces a "feature map" showing
where that pattern appears.
```

Filters are the **fundamental building block** of CNNs.

---

## What a Filter Looks Like

A typical 3×3 filter:

```
filter = [[ w₁  w₂  w₃ ],
          [ w₄  w₅  w₆ ],
          [ w₇  w₈  w₉ ]]

Just 9 numbers. These weights are LEARNED during training.
```

---

## How a Filter Works — Convolution Operation

The filter **slides over the image**, one position at a time. At each position:

```
1. Place the filter on a patch of the image
2. Multiply each filter value by the corresponding pixel
3. Sum all products to get ONE OUTPUT VALUE
4. Slide the filter to the next position
5. Repeat until the whole image is covered
```

### Concrete Example

Suppose we have a 5×5 image and a 3×3 filter:

```
Image:                            Filter:
┌──┬──┬──┬──┬──┐                  [1  0  1]
│ 0│ 1│ 2│ 1│ 0│                  [0  1  0]
├──┼──┼──┼──┼──┤                  [1  0  1]
│ 1│ 0│ 1│ 0│ 1│
├──┼──┼──┼──┼──┤
│ 2│ 1│ 0│ 1│ 2│
├──┼──┼──┼──┼──┤
│ 1│ 0│ 1│ 0│ 1│
├──┼──┼──┼──┼──┤
│ 0│ 1│ 2│ 1│ 0│
└──┴──┴──┴──┴──┘
```

Apply the filter to the top-left 3×3 region:

```
Image patch:       Filter:        Element-wise multiply:
[0  1  2]         [1  0  1]       [0   0   2]
[1  0  1]    ×    [0  1  0]   =   [0   0   0]
[2  1  0]         [1  0  1]       [2   0   0]

Sum all results: 0 + 0 + 2 + 0 + 0 + 0 + 2 + 0 + 0 = 4
                                                     ↑
                                                One output value
```

That `4` goes into position [0,0] of the output (the **feature map**).

Then **slide** the filter one position to the right, repeat. Continue across the entire image:

```
Output feature map (3×3 from a 5×5 input):

[ 4,  ?,  ? ]
[ ?,  ?,  ? ]
[ ?,  ?,  ? ]

Each value = filter applied at one image position.
```

---

## Why Filters Detect Patterns

The genius is that **specific filter values detect specific patterns**:

### Edge Detection Filter (vertical edge)

```
filter = [[-1  0  +1],
          [-1  0  +1],
          [-1  0  +1]]
```

This filter outputs **large positive values** when there's a bright region on the right and dark on the left — i.e., a **vertical edge**:

```
Dark | Bright  →  filter output: large positive
Bright | Dark  →  filter output: large negative
Uniform        →  filter output: near zero
```

### Horizontal Edge Filter

```
filter = [[-1 -1 -1],
          [ 0  0  0],
          [+1 +1 +1]]
```

Detects horizontal edges (bright above dark, etc.).

### Other Classic Filters

```
Identity:          [0 0 0]        →  copies the input
                   [0 1 0]
                   [0 0 0]

Blur (average):    [⅑ ⅑ ⅑]        →  smooths the image
                   [⅑ ⅑ ⅑]
                   [⅑ ⅑ ⅑]

Sharpen:           [ 0 -1  0]      →  enhances edges
                   [-1  5 -1]
                   [ 0 -1  0]
```

---

## Filters Are Learned, Not Designed

In **classical computer vision**, people hand-designed filters (edge detectors, Gabor wavelets, etc.).

In **CNNs**, filters are **learned automatically** through backpropagation:

```
Initial filter weights:  random values

Training:
   Forward pass: apply filter, get prediction
   Loss: how wrong the prediction was
   Backward pass: compute gradient of loss w.r.t. filter weights
   Update: adjust filter weights to reduce loss

After training:
   Filters have evolved into useful pattern detectors
   (edges, textures, parts, etc.)
```

---

## Sliding the Filter — The Convolution

Sliding the filter across the image is called **convolution**. Visually:

```
Step 1: filter at top-left position
   ┌─┬─┬─┬─┬─┐
   │█│█│█│ │ │   filter covers this region
   │█│█│█│ │ │
   │█│█│█│ │ │
   │ │ │ │ │ │
   │ │ │ │ │ │
   └─┴─┴─┴─┴─┘

Step 2: shift right by 1
   ┌─┬─┬─┬─┬─┐
   │ │█│█│█│ │
   │ │█│█│█│ │
   │ │█│█│█│ │
   │ │ │ │ │ │
   │ │ │ │ │ │
   └─┴─┴─┴─┴─┘

... continues across the whole image
```

Each position produces one number → these numbers form the **feature map**.

---

## What "Sliding" Produces — The Feature Map

```
Input image (28×28) + 3×3 filter
   ↓
Feature map (26×26)
```

The feature map is a **2D heatmap** showing **where** the pattern was detected in the original image. Bright spots = strong pattern match.

---

## Many Filters in Parallel

A single convolutional layer doesn't use just ONE filter. It uses **many filters at once** — typically 32, 64, 128, or more:

```
Convolutional layer:
   filter 1 → detects vertical edges    → feature map 1
   filter 2 → detects horizontal edges  → feature map 2
   filter 3 → detects diagonal patterns → feature map 3
   ...
   filter 64 → detects something else   → feature map 64

Output: a STACK of 64 feature maps
        (called a "feature volume" or 3D tensor)
```

Each filter learns a **different pattern**.

---

## Filter Channels for Colour Images

RGB images have 3 channels. Filters extend to 3D:

```
For an RGB input (height × width × 3 channels):

Filter shape: 3 × 3 × 3
   ↑   ↑   ↑
   H   W   channels (matches input channels)

The filter looks across ALL THREE COLOR CHANNELS at once.
```

---

## Filter Hyperparameters

| Hyperparameter | What it does | Typical |
|----------------|--------------|---------|
| **Filter size** | Spatial dimensions of the filter | 3×3, 5×5 |
| **Number of filters** | How many different patterns to detect | 32, 64, 128, 256 |
| **Stride** | How many pixels to shift between positions | 1 (or 2 for downsampling) |
| **Padding** | Pixels added around image edges | "same" or "valid" |

---

## Output Size Formula

The size of the feature map produced by a convolution depends on input size, filter size, padding, and stride.

```
            N − F + 2P
Output = ─────────────── + 1
                S

Where:
   N = input size (height or width)
   F = filter size
   P = padding (pixels added on each side)
   S = stride (how many pixels to shift)
```

### Example

Input: 7×7, filter: 3×3, padding: 0, stride: 1

```
N = 7, F = 3, P = 0, S = 1

Output = (7 − 3 + 0) / 1 + 1
       = 4 / 1 + 1
       = 4 + 1
       = 5

Output: 5 × 5
```

A 7×7 input with a 3×3 filter (no padding, stride 1) → 5×5 feature map.

### More Examples

**Same padding (preserves size):**

```
N = 28, F = 3, P = 1, S = 1
Output = (28 − 3 + 2) / 1 + 1 = 27 + 1 = 28

Output: 28 × 28  (same as input)
```

This is why P=1 is paired with F=3 ("same" padding for 3×3 filter).

**Stride 2 (downsampling by ~half):**

```
N = 32, F = 3, P = 1, S = 2
Output = (32 − 3 + 2) / 2 + 1 = 31/2 + 1 = 15 + 1 = 16

Output: 16 × 16  (halved)
```

Stride > 1 is often used to **shrink the feature map** instead of using pooling.

**Larger filter, no padding:**

```
N = 32, F = 5, P = 0, S = 1
Output = (32 − 5 + 0) / 1 + 1 = 27 + 1 = 28

Output: 28 × 28  (shrunk by 4 pixels)
```

### Why Padding Matters

```
Without padding:
   - feature map SHRINKS each layer
   - corner/edge pixels see FEWER filter applications
   - lose information at the borders

With padding (P > 0):
   - can maintain spatial dimensions
   - corner pixels treated equally to interior pixels
   - common: P = (F-1) / 2 for "same" padding
```

### Why Stride Matters

```
Stride = 1:
   - filter shifts by 1 pixel each time
   - dense overlap between positions
   - output is roughly same size as input

Stride = 2:
   - filter shifts by 2 pixels each time
   - half-resolution output
   - common alternative to pooling for downsampling
```

### Rule of Thumb

```
Want to KEEP spatial size:
   F = 3, P = 1, S = 1   → "same" 3×3 conv
   F = 5, P = 2, S = 1   → "same" 5×5 conv

Want to DOWNSAMPLE:
   F = 3, P = 1, S = 2   → halve the size
   OR use F=2 max pooling with stride 2
```

---

## In PyTorch

```python
import torch.nn as nn

# A convolutional layer with 32 filters of size 3×3
conv = nn.Conv2d(
    in_channels=3,       # input has 3 channels (RGB)
    out_channels=32,     # use 32 filters → 32 output feature maps
    kernel_size=3,       # 3×3 filters
    stride=1,
    padding=1            # 'same' padding
)
```

This layer has only **896 parameters** vs. millions for an equivalent fully-connected layer.

---

## Which Feature Maintains Spatial Locality?

**The CONVOLUTION OPERATION (filters applied to local patches) is what maintains spatial locality.**

More specifically — the key idea is **local connectivity**:

```
Each filter looks at only a SMALL LOCAL PATCH of the image at a time.
   → 3×3 filter sees 9 pixels at one position
   → only NEIGHBOURING pixels interact within a filter

This is what PRESERVES SPATIAL STRUCTURE.
```

### Why Local Connectivity Preserves Locality

```
Fully connected (MLP):
   Every output neuron connects to EVERY input pixel.
   → top-left pixel and bottom-right pixel are equally close
   → spatial structure is destroyed

Convolution:
   Each output value depends on a SMALL LOCAL PATCH of input pixels.
   → near-by pixels interact through the same filter
   → far-apart pixels DON'T interact at this layer
   → SPATIAL STRUCTURE PRESERVED
```

### The Three Architectural Choices Together

Three CNN properties work together to maintain spatial locality:

| Feature | How it preserves spatial info |
|---------|-------------------------------|
| **Local connectivity** | Each filter only sees a small neighbourhood, not the whole image |
| **Weight sharing (sliding filters)** | Same filter applied at every position — relative pixel relationships are preserved |
| **No flattening between conv layers** | Feature maps remain 2D — spatial layout maintained |

```
Image stays as a 2D grid throughout the convolutional layers.
Each layer's output is a 2D feature map.
Spatial position is preserved end to end.

→ Only at the very end, when feeding into final classifier,
   do we flatten to a 1D vector.
```

### The Bigger Picture

```
Spatial locality in CNNs = "pixels that were close in the input
                            stay close in the feature maps"

Achieved by:
   1. Convolution operation (local patches)
   2. Local connectivity (small filter size)
   3. Keeping 2D feature maps throughout
   4. (and weight sharing for translation invariance)
```

If you flattened the image before conv layers, all locality is lost. The whole point of convolution is to **process the image AS A 2D GRID** — respecting which pixels are neighbours.

---

## Summary

```
A convolutional filter is:
   - a small matrix of weights (typically 3×3 or 5×5)
   - learned during training (not hand-designed)
   - applied at every position of the image via sliding

Each conv layer uses MANY filters in parallel (32, 64, 128, ...)
producing a stack of feature maps.

KEY PROPERTY: spatial locality is preserved through:
   ✓ Local connectivity (filter only sees a small patch)
   ✓ 2D feature maps maintained throughout
   ✓ Same filter applied via sliding (weight sharing)
   ✓ No flattening until the final classifier

This is why CNNs are PERFECT for images while MLPs fail.
```

> Convolutional filters are the **eyes** of a CNN. Each filter "sees" one specific pattern in a local patch; together they build up rich visual understanding while **respecting spatial structure** — the single most important architectural insight that made deep learning for vision possible.
