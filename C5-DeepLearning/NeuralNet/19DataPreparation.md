# Data Preparation and Normalisation for CNNs

Even the best CNN architecture fails on **poorly prepared data**. Good data preparation makes training **stable, fast, and effective**.

```
Garbage in → Garbage out.
Well-prepared data → smooth training curves, better accuracy.
```

---

## The Standard Data Preparation Pipeline

```
1. Load raw images
2. Resize to consistent dimensions
3. Convert to tensors
4. Normalise pixel values
5. Split into train / val / test
6. Batch and shuffle
```

Each step matters — skip any one and training quality suffers.

---

## Step 1 — Resizing

CNNs typically need **fixed input size** (e.g., 224×224 for VGG, ResNet).

```
Raw images: any size (640×480, 1024×768, 200×200, ...)
            ↓ resize
All images:  same size (e.g., 224×224)
```

### Approaches

```
Direct resize:     stretch/squish to target size
                    ✗ distorts aspect ratio

Resize + crop:     resize so smaller side matches, then centre-crop
                    ✓ preserves aspect ratio
                    ✗ loses some image content at edges

Pad + resize:      pad with zeros (or replicate edges), then resize
                    ✓ preserves entire image
                    ✗ adds black borders
```

Modern frameworks: ResNet/VGG style → resize so smaller dim = 256, then crop to 224.

---

## Step 2 — Pixel Value Range

Raw image pixels are integers 0-255. CNN inputs are typically converted to **floats in [0, 1] or normalised further**.

```
Raw pixel:     0 to 255 (uint8)
                ↓ divide by 255
Scaled pixel:  0.0 to 1.0 (float32)
```

This first step is just rescaling. The next step is the real normalisation.

---

## Step 3 — Channel-Wise Normalisation (Standardisation)

Each colour channel (R, G, B) is normalised separately to have **mean 0 and std 1**:

```
For each channel:
   normalised_pixel = (pixel − channel_mean) / channel_std
```

### Why Normalise?

```
✓ Stabilises training — activations stay in a reasonable range
✓ Speeds up convergence — gradients are better-scaled
✓ Compatible with pretrained models — they expect normalised inputs
✓ Prevents exploding/vanishing gradients
```

Without normalisation, raw pixel values (0-255) would produce huge activations in the first layer, leading to unstable gradients.

---

## ImageNet Normalisation Statistics

The most common convention — using the mean/std of the **ImageNet dataset**:

```
Mean:  [0.485, 0.456, 0.406]    (R, G, B)
Std:   [0.229, 0.224, 0.225]
```

These values come from averaging across millions of ImageNet images. **Most pretrained models expect input normalised with these stats** — even if you're using your own data.

If you compute mean/std on **your own dataset**, that works too — but you must then **always use those same stats** consistently between training, validation, and inference.

---

## In PyTorch — torchvision.transforms

```python
import torchvision.transforms as T

transform = T.Compose([
    T.Resize(256),                              # resize shorter side to 256
    T.CenterCrop(224),                          # crop centre 224×224
    T.ToTensor(),                                # converts to float [0, 1]
    T.Normalize(
        mean=[0.485, 0.456, 0.406],              # ImageNet stats
        std=[0.229, 0.224, 0.225]
    )
])

# Apply to a single image
image_tensor = transform(pil_image)
# Shape: (3, 224, 224), normalised
```

This is the **standard preprocessing pipeline** for vision tasks.

---

## Step 4 — Train/Val/Test Split

```
Train (60-80%):   used to update weights
Val   (10-20%):   used to monitor overfitting, tune hyperparameters
Test  (10-20%):   used ONCE at the end for honest evaluation
```

Critical: compute normalisation stats from **training set only** (or use ImageNet). Don't let test data leak into preprocessing.

```python
from torch.utils.data import random_split

train_set, val_set, test_set = random_split(
    full_dataset, [0.7, 0.15, 0.15]
)
```

---

## Step 5 — Batching with DataLoader

CNNs train on **batches**, not single images:

```python
from torch.utils.data import DataLoader

train_loader = DataLoader(
    train_set,
    batch_size=32,        # process 32 images per step
    shuffle=True,          # randomise order each epoch
    num_workers=4         # parallel loading
)
```

Why batches?

```
✓ GPU efficiency — batch operations are faster than one-at-a-time
✓ More stable gradients — averaged across multiple samples
✓ Memory constraints — can't fit whole dataset in GPU memory
```

Common batch sizes: 16, 32, 64, 128 (powers of 2 for GPU efficiency).

---

## Different Stats for Different Splits?

**No** — use the SAME mean/std for training, validation, and test.

```
Wrong: compute val/test mean/std from val/test data
        → introduces data leakage

Right: compute mean/std from TRAINING data
       apply those same values to val and test
```

This ensures all data is on the same scale at inference time.

---

## Per-Image vs Per-Dataset Normalisation

Two strategies:

### Per-dataset (standard)

```
Compute mean/std across ALL training images.
Apply the same mean/std to every image.
```

This is the default. Cheap, simple, works well.

### Per-image (sample-wise)

```
For each image, compute its OWN mean/std and normalise.
```

Used when:
- Images come from very different sources
- Lighting / colour calibration varies wildly

Less common in modern deep learning.

---

## Common Preparation Mistakes

```
✗ Different normalisation for train and test
   → model trained on one distribution, tested on another → fails

✗ Forgetting to convert to float before normalisation
   → integer division causes issues, gradients can't flow

✗ Using uint8 (0-255) inputs directly
   → first-layer activations huge → unstable training

✗ Shuffling the test set
   → not wrong, but breaks reproducibility of evaluation

✗ Normalising AFTER augmentation in some cases
   → can sometimes amplify augmentation artefacts
   → conventional order: augment → ToTensor → Normalize
```

---

## What Else Matters in CNN Data Prep

```
Class balance:
   Are some classes much more common than others?
   → use class weights or oversample minority classes

Image quality:
   Are images corrupted, blurry, mislabeled?
   → clean the dataset first

Data leakage:
   Are test images similar to training images?
   → check for duplicates across splits
```

---

## Why It Matters for CNNs Specifically

```
CNNs have HUGE numbers of parameters that learn from raw pixels.
Without normalisation:
   - First-layer activations have huge ranges
   - Gradients explode or vanish
   - Training is unstable

Normalisation:
   - Each colour channel ~ standard normal
   - Activations stay in a sensible range
   - Gradient updates are well-scaled
   - Training is FAST and STABLE
```

This is why every modern CNN tutorial includes the ImageNet normalisation step — it's not optional.

---

## Summary

```
Data preparation for CNNs:
   1. Resize to consistent dimensions (e.g., 224×224)
   2. Convert to float tensor (range [0, 1])
   3. Channel-wise normalisation (mean/std subtraction)
   4. Split into train / val / test
   5. Batch with DataLoader

Standard normalisation:
   Use ImageNet stats:
      mean = [0.485, 0.456, 0.406]
      std  = [0.229, 0.224, 0.225]
   
   OR compute your own from training data.
   Apply SAME stats to train, val, and test.

This is foundational — every CNN training pipeline includes it.
```

> Good data preparation is half the battle in training CNNs. Skip normalisation and you'll fight unstable gradients forever; include it and training "just works".
