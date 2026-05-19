# CNN Intro — Why MLPs Fail for Images

Multi-Layer Perceptrons (fully connected networks) work great on tabular data. But for **images**, they hit a wall:

```
MLPs treat images as flat lists of pixels.
   → They lose spatial structure
   → They explode in parameter count
   → They don't generalise across positions

CNNs were invented to fix all three problems.
```

Before we dive into how CNNs work, let's understand **why we need them at all**.

---

## The 4 Reasons MLPs Fail for Images

### 1. Parameter Explosion

A modest 256×256 RGB image has:

```
256 × 256 × 3 = 196,608 pixel values per image
```

If you feed this into an MLP with a 1000-neuron first layer:

```
First-layer weights: 196,608 × 1000 = 196,608,000 parameters
                                     ≈ 200 million weights
                                     in just ONE layer!
```

And that's just the first layer. A typical model would have 5-10 layers, each needing similarly massive matrices.

```
✗ Memory explodes
✗ Training time becomes infeasible
✗ Massive risk of overfitting
✗ Most weights aren't really useful
```

Real-world images can be 1024×1024 or larger — the math gets absurd.

---

### 2. Spatial Structure Is Destroyed

MLPs require a **flat input vector**. To feed an image, you have to flatten it:

```
Original image (28×28):                 Flattened (784 values):
   ┌─────┬─────┬─────┐
   │  1  │  2  │  3  │      flatten      [1, 2, 3, 4, 5, 6, 7, 8, 9, ...]
   ├─────┼─────┼─────┤      ─────────►
   │  4  │  5  │  6  │
   ├─────┼─────┼─────┤
   │  7  │  8  │  9  │
   └─────┴─────┴─────┘
```

**Problem:** the model sees only the flat list. It has **no idea** that:

```
Pixel 1 is next to pixel 2 (horizontally)
Pixel 1 is next to pixel 4 (vertically — they were neighbours!)
Pixel 5 is in the middle, surrounded by others
```

For images, **spatial relationships are everything**:

```
A "cat ear" is a SPECIFIC PATTERN of nearby pixels
Edges, corners, textures are LOCAL relationships
Spatial proximity carries meaning
```

MLPs throw all this away by flattening. They'd have to relearn spatial relationships from scratch — needing way more data than a CNN that bakes them in.

---

### 3. No Translation Invariance

If you train an MLP to recognise a cat in the top-left of an image, what happens when the cat appears in the bottom-right?

```
                                
   Top-left cat                Bottom-right cat
   ┌───────────┐               ┌───────────┐
   │ 🐱        │               │           │
   │           │               │           │
   │           │               │        🐱 │
   └───────────┘               └───────────┘

   ↓ flatten                    ↓ flatten
   [🐱, 0, 0, 0, ...]           [0, 0, 0, ..., 🐱]

   completely different flat vectors!
```

To an MLP, these are **two completely different inputs**. The weights that recognised "cat = first few pixels" don't help when "cat = last few pixels".

The MLP would need to see the cat in **every possible position** to learn to recognise it everywhere. This means:

```
✗ Massive training data needed
✗ Model gets fooled by even small shifts
✗ Generalisation across positions is poor
```

CNNs solve this with **weight sharing** — the same feature detector slides across the entire image.

---

### 4. No Built-In Hierarchy

Visual understanding is naturally hierarchical:

```
Pixels       → edges       → shapes      → parts        → objects
(level 1)    (level 2)     (level 3)     (level 4)      (level 5)
```

MLPs don't naturally exploit this. They learn a flat mapping from pixel values to class labels — without any structural prior.

CNNs are **designed** to mirror this hierarchy:

```
Early layers:    detect edges and gradients
Middle layers:   combine edges into shapes and textures
Late layers:     combine shapes into object parts
Final layers:    recognise whole objects
```

This makes them sample-efficient and naturally generalisable.

---

## How CNNs Fix These Problems

### Problem 1 (Parameter Explosion) → Weight Sharing

Instead of having every neuron connect to every pixel, CNNs use **small filters** (kernels) that are shared across the entire image:

```
Filter (3×3):     [w₁  w₂  w₃]
                  [w₄  w₅  w₆]
                  [w₇  w₈  w₉]

Only 9 weights — and the SAME 9 weights detect the same pattern
ANYWHERE in the image.
```

For a 256×256 image, this filter slides across all positions but uses only 9 weights total — instead of millions.

```
MLP first layer:    200 MILLION parameters
CNN first layer:    a few hundred to a few thousand parameters
```

---

### Problem 2 (Spatial Structure) → Local Connectivity

CNN filters operate on **local patches** of the image:

```
Image                          Filter result
┌──┬──┬──┬──┬──┐
│  │  │  │  │  │
├──┼──┼──┼──┼──┤
│  │██│██│██│  │ ←─ a 3×3 filter sees these 9 pixels  → produces 1 output
├──┼──┼──┼──┼──┤
│  │██│██│██│  │     and uses their LOCAL relationship
├──┼──┼──┼──┼──┤
│  │██│██│██│  │
├──┼──┼──┼──┼──┤
│  │  │  │  │  │
└──┴──┴──┴──┴──┘
```

The filter respects neighbourhood. Pixel structure isn't flattened away.

---

### Problem 3 (Translation Invariance) → Sliding Filters

The same filter slides across the entire image:

```
Filter applied at top-left position:    detects feature here
Filter applied at top-middle:            detects feature here
Filter applied at bottom-right:          detects feature here
...

Same weights, every location.
```

So if the network learns to detect a "cat ear" pattern, it detects that pattern **anywhere** in the image automatically. **Translation invariance** comes for free.

---

### Problem 4 (Hierarchy) → Stacked Convolutional Layers

By stacking convolutional layers, CNNs naturally build hierarchies:

```
Layer 1: detects edges, corners, simple gradients
Layer 2: combines edges into textures, simple shapes
Layer 3: combines shapes into object parts (eyes, wheels, leaves)
Layer 4: combines parts into whole objects
```

Each layer builds on the previous — exactly matching how visual perception works.

---

## Side-by-Side Comparison

| | MLP for images | CNN |
|-|----------------|-----|
| **Input** | Flat vector (loses spatial info) | 2D grid (preserves spatial info) |
| **Parameters** | Millions in first layer | Thousands (weight sharing) |
| **Translation invariance** | No — fails on shifted images | Yes — built-in via sliding filter |
| **Local relationships** | Has to learn from scratch | Inherent in architecture |
| **Hierarchy** | None | Naturally hierarchical |
| **Sample efficiency** | Needs huge data | Generalises with less data |
| **Modern use for vision** | ✗ Obsolete | ✓ Default until Vision Transformers |

---

## The Core Idea of CNNs

```
CNN = MLP + 3 architectural priors specifically for images:

   1. LOCAL CONNECTIVITY
      Neurons see only a small local patch (e.g. 3×3).

   2. WEIGHT SHARING
      Same filter applied at every position.

   3. POOLING (downsampling)
      Reduce spatial size while keeping important features.
      Adds another layer of translation invariance.
```

These three together turn the "image is a flat list of pixels" mess into a tractable, sample-efficient learning problem.

---

## Where MLPs Still Fit

MLPs aren't useless — they're just the wrong tool for images. They still excel at:

```
✓ Tabular data (rows of features)
✓ Final classification layers AFTER a CNN extracts features
✓ Simple regression / classification tasks
✓ Any input where features don't have spatial structure
```

In fact, the **last few layers of a CNN are usually fully-connected (MLP) layers** — they take CNN-extracted features and produce the final predictions.

---

## Quick Visual

```
   Image input
   ───────────
   
   MLP approach:
   ┌──┬──┬──┬──┐
   │ flatten   │ → [196608 values] → 200M params first layer → ⚠️
   └──┴──┴──┴──┘

   CNN approach:
   ┌──┬──┬──┬──┐
   │  │  │  │  │ → small filter slides → reuses 9 weights everywhere → ✓
   ├──┼──┼──┼──┤
   │  │██│██│  │   (then stack layers, pool, etc.)
   ├──┼──┼──┼──┤
   │  │██│██│  │
   ├──┼──┼──┼──┤
   │  │  │  │  │
   └──┴──┴──┴──┘
```

---

## Summary

```
MLPs fail on images because:
   1. PARAMETER EXPLOSION — fully connected first layer is huge
   2. NO SPATIAL STRUCTURE — flattening destroys neighbourhood relationships
   3. NO TRANSLATION INVARIANCE — recognising "cat at top" ≠ "cat at bottom"
   4. NO HIERARCHY — flat mapping from pixels to labels

CNNs fix this with:
   1. WEIGHT SHARING — same small filter reused across image
   2. LOCAL CONNECTIVITY — preserves spatial structure
   3. SLIDING FILTERS — translation invariance built-in
   4. STACKED LAYERS + POOLING — natural hierarchical features
```

> CNNs are MLPs that respect the structure of images. That single insight — building **inductive bias** for visual data into the architecture — kicked off the deep learning revolution in computer vision.
