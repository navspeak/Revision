# Data Augmentation for CNNs

**Generate more training data from existing samples** by applying realistic transformations. This makes models more robust and reduces overfitting.

```
Real-world variation:
   ✓ photos taken from different angles
   ✓ different lighting conditions
   ✓ rotated, cropped, zoomed
   ✓ slightly different colours

Augmentation simulates these variations during training,
so the model learns to be INVARIANT to them.
```

---

## The Core Idea

```
Original training image: 1 cat photo
                          ↓ apply random transformations
Augmented "new images":
   - flipped horizontally
   - rotated 15°
   - cropped to 90% size
   - colour-jittered
   - blurred slightly

The model SEES these as different inputs → trains on a virtually larger dataset.
```

A dataset of 10,000 images, with 5-10 augmentations per image per epoch, gives the model **effectively 50-100K images** to learn from — without collecting any new data.

---

## Why Augmentation Works

```
✓ Reduces overfitting
   Model can't memorise specific pixel patterns when they keep changing

✓ Improves generalisation
   Model learns INVARIANT features (cat = cat regardless of rotation)

✓ Effectively increases dataset size
   No new collection effort needed

✓ Robust to real-world variation
   Test images won't be perfectly centred and lit either

✓ Free in compute (applied on the CPU during data loading)
```

For small datasets (a few thousand images), augmentation is the single most effective trick to boost accuracy.

---

## Common Augmentations for Vision

### 1. Geometric Transformations

```
✓ Horizontal flip      — random left-right mirror
✓ Vertical flip         — random up-down (less common; depends on data)
✓ Random rotation       — typically ±15° to ±30°
✓ Random crop           — extract a random sub-region
✓ Resize                — scale to slightly different sizes
✓ Translation           — shift image horizontally / vertically
✓ Shearing               — slight perspective distortion
✓ Random scaling         — zoom in or out
```

### 2. Colour / Photometric Transformations

```
✓ Brightness jitter    — randomly darken / lighten
✓ Contrast jitter       — adjust contrast
✓ Saturation jitter     — change colour intensity
✓ Hue jitter            — shift colour palette
✓ Grayscale (random)    — sometimes convert to grayscale
✓ Gaussian noise        — add random noise to pixels
```

### 3. Cutout / Erasing

```
✓ Random erasing — replace a random rectangular region with noise or zeros
                   → model can't rely on any one part of the image
```

### 4. Advanced Augmentations

```
✓ MixUp           — blend two images linearly: 0.7·imageA + 0.3·imageB
                    label is the same mix → "softer" supervision
✓ CutMix          — paste a random patch from one image into another
✓ AutoAugment     — learns the best augmentation policy from data
✓ RandAugment    — random subset of augmentations applied
```

These are state-of-the-art techniques used in modern training pipelines (e.g., training EfficientNet, Vision Transformers).

---

## Which Augmentations to Use?

Depends on the data and task. Some examples:

```
Photos of objects (cats, cars, food):
   ✓ horizontal flip ✓ rotation ✓ colour jitter ✓ random crop
   ✗ vertical flip (upside-down cats are weird)

Aerial / satellite images:
   ✓ horizontal AND vertical flip ✓ rotation 0-360°
   (orientation is arbitrary in top-down imagery)

Medical imaging:
   ✓ slight rotation ✓ slight scaling
   ✗ heavy colour changes (medical scans have specific intensities)

Text / OCR:
   ✗ horizontal flip (text would be backwards)
   ✓ slight rotation, slight translation

Handwritten digits (MNIST):
   ✗ horizontal flip (a flipped '3' isn't a '3')
   ✓ slight rotation, slight translation
```

**Rule:** augmentation should produce images that **could realistically appear in the test set**.

---

## In PyTorch — Standard Pipeline

```python
import torchvision.transforms as T

train_transform = T.Compose([
    T.RandomResizedCrop(224),                 # random crop + resize
    T.RandomHorizontalFlip(p=0.5),            # 50% chance to flip
    T.RandomRotation(15),                     # ±15° rotation
    T.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2,
        hue=0.1
    ),
    T.ToTensor(),
    T.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Validation / test — NO augmentation
val_transform = T.Compose([
    T.Resize(256),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
```

**Important:** apply augmentation **only to training data**. Validation and test sets should be evaluated on the original (or deterministic) preprocessing.

---

## When Augmentations Are Applied

```
Each epoch, each image gets randomly augmented:

Epoch 1, image #5:    flipped horizontally + 10° rotation + slight crop
Epoch 2, image #5:    not flipped + 5° rotation + colour jitter
Epoch 3, image #5:    flipped + 15° rotation + brighter

Same image, different augmentations each epoch → looks like a "new" image.
```

This is why training over many epochs with augmentation gives the model exposure to thousands of effective variations per original image.

---

## Augmentation Modern Libraries

| Library | Use case |
|---------|----------|
| **torchvision.transforms** | PyTorch built-in, simple |
| **albumentations** | Faster, more transforms, popular for vision |
| **kornia** | GPU-accelerated transforms |
| **imgaug** | Older, very comprehensive |
| **AutoAugment / RandAugment** | Learned / random augmentation policies |

```python
# Example with albumentations
import albumentations as A

train_transform = A.Compose([
    A.RandomResizedCrop(224, 224),
    A.HorizontalFlip(p=0.5),
    A.Rotate(limit=15),
    A.ColorJitter(p=0.5),
    A.Normalize(),
    A.ToTensorV2()
])
```

---

## Tasks Beyond Classification

Augmentation extends to other vision tasks:

```
Semantic segmentation:
   When flipping/rotating, MUST flip/rotate the segmentation mask too
   → use library that applies the same transform to both image and mask

Object detection:
   Bounding boxes must be transformed alongside the image
   → albumentations and others handle this automatically

Keypoint detection:
   Keypoint coordinates must follow the geometric transformations
```

---

## How Much to Augment?

```
Too little:
   ✗ Risk of overfitting (especially on small datasets)
   ✗ Model not robust to real-world variation

Too much:
   ✗ Training becomes unstable
   ✗ Model can't learn — augmentations are too extreme
   ✗ Train accuracy drops because images get mangled

Sweet spot:
   ✓ Augmentations that resemble realistic variations
   ✓ Strong but not destructive
   ✓ Tune intensity based on validation performance
```

Modern best practice: start moderate, increase if overfitting; decrease if model can't fit at all.

---

## Augmentation vs Other Regularisation

```
Augmentation     →  diversifies the training distribution
                    cheap and effective for vision
                    
L2 / Weight Decay → keeps weights small
                    works with any model
                    
Dropout          →  randomly deactivates neurons
                    forces redundancy
                    
Early Stopping   →  monitors validation loss
                    always useful

These all combine well — modern training pipelines use ALL of them.
```

---

## Summary

```
Data augmentation:
   ✓ generates new "synthetic" training examples
   ✓ via realistic transformations of existing images
   ✓ applied randomly during training
   ✓ reduces overfitting, improves generalisation
   ✓ free compute (CPU during data loading)
   
Common augmentations for vision:
   - Flip, rotation, crop, scale
   - Colour jitter, brightness, contrast
   - Cutout, MixUp, CutMix (advanced)

Apply to TRAINING only — never to validation or test.

In PyTorch: torchvision.transforms.Compose([...])
For more power: albumentations
```

> Augmentation is **the cheapest way to improve a CNN's performance** on a small dataset. Always include it in your training pipeline unless you have a specific reason not to.
