# Overfitting and Generalisation in CNNs

CNNs have **millions of parameters** trained on relatively few images. Without safeguards, they **memorise the training data** instead of learning to generalise.

```
Overfitting in CNNs → very common, very destructive
Generalisation       → the actual goal of training
```

This is the consolidated playbook for **detecting and fixing overfitting** specifically for CNNs. Cross-references existing files where relevant.

---

## Why CNNs Overfit So Easily

```
Typical CNN:        50M parameters
Typical dataset:    50,000 images (or fewer for niche tasks)

Parameter ratio:    1000+ parameters per image
   → memorisation is mathematically possible
   → and easy to do
```

CNNs have **massive capacity**. Without regularisation they'll fit any training data perfectly — including the noise.

---

## Symptoms of Overfitting in CNNs

```
✓ Training accuracy keeps rising past 99%
✓ Validation accuracy stops improving (or DROPS)
✓ Training loss keeps falling
✓ Validation loss starts RISING
✓ Large gap between train and val accuracy (5-20%+)
✓ Model misclassifies obvious test images
✓ Model is fooled by minor image perturbations
✓ Predictions are highly confident even when wrong
```

```
Loss
  │\
  │ \___                       Training loss (keeps dropping)
  │     \___
  │         \___
  │             \________
  │
  │      __________
  │   /             \____
  │  /                   \___   Validation loss
  │ /                        \___
  │/                              ↑
  │                            starts rising → overfitting
  └─────────────────────────────── epoch
              ↑
       best stopping point
```

If you see this pattern → you're overfitting.

---

## The 7-Step CNN Anti-Overfitting Playbook

```
1. Get MORE DATA (if possible)
2. AUGMENT existing data
3. Use TRANSFER LEARNING from a pretrained model
4. Apply REGULARISATION (L2 weight decay, dropout)
5. Use BATCH NORMALISATION
6. EARLY STOPPING with validation monitoring
7. REDUCE model capacity (smaller architecture)
```

In practice, you'll use **several of these together**. Modern CNN training pipelines almost always include items 2-6.

---

## 1. Get More Data

```
The single best fix for overfitting.

Doubling your training data > nearly any other technique.

In practice:
   - Collect more labelled images
   - Use online datasets (ImageNet, COCO, OpenImages)
   - Synthetic data generation (GANs, simulation)
   - Web scraping (with licence considerations)
```

But often you can't get more data. That's where the other 6 techniques come in.

---

## 2. Data Augmentation

The cheapest "free" way to get more data. Apply realistic transformations to existing images.

```
Common augmentations:
   ✓ Horizontal flip
   ✓ Random crop (with resize)
   ✓ Rotation (±15° typically)
   ✓ Colour jitter (brightness, contrast, saturation)
   ✓ Random erasing / cutout
   ✓ MixUp / CutMix (advanced — blend images)
```

**Effect:** an "image of a dog rotated 10°" looks like a different image to the network → effectively 5-10× more training examples per epoch.

Full coverage: see `20DataAugmentation.md`.

---

## 3. Transfer Learning

Reuse a CNN pretrained on a HUGE dataset (typically ImageNet's 1.2M images).

```
The pretrained CNN already knows:
   ✓ How to detect edges, textures, shapes, parts, objects
   
You only need to:
   ✓ Replace the final classification head
   ✓ Fine-tune (or just freeze + train head)
```

This drastically reduces overfitting because you're not learning the conv filters from scratch — you're adapting already-good ones.

```
Training from scratch:   needs millions of images
Transfer learning:        works with hundreds
```

Full coverage: see `21TransferLearning.md`.

---

## 4. Regularisation — L2 and Dropout

### L2 Weight Decay

```
Add penalty to loss for large weights:
   loss = task_loss + λ × Σ wᵢ²

Effect: keeps weights small → smoother decision boundary → less overfitting.
```

In PyTorch:

```python
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
```

`weight_decay=1e-4` is a sensible default. Always include it.

### Dropout

```
Randomly "drop" (zero out) some neurons during training.
   → network can't rely on any single neuron
   → forces redundancy → less overfitting
```

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(512, 256),
    nn.ReLU(),
    nn.Dropout(0.5),    # 50% dropout
    nn.Linear(256, num_classes)
)
```

```
Typical CNN dropout:
   Convolutional layers:  0.0-0.2  (low — preserves spatial features)
   Fully connected head:  0.3-0.5  (higher — typical place)
```

Full coverage: see `12Regularization.md`.

---

## 5. Batch Normalisation

```
Normalises activations across the batch in each layer.
   → stabilises training
   → enables higher learning rates
   → acts as MILD regularisation
```

Used in nearly every modern CNN (ResNet, VGG, EfficientNet).

```python
model = nn.Sequential(
    nn.Conv2d(3, 64, 3, padding=1),
    nn.BatchNorm2d(64),       # ← normalises after conv
    nn.ReLU(),
    ...
)
```

Standard pattern: **Conv → BatchNorm → ReLU**.

Full coverage: see `13Normalization.md`.

---

## 6. Early Stopping

```
Monitor validation loss.
Stop training when val loss stops improving.
Restore the best-checkpoint weights.
```

Critical for CNNs because:
- Validation loss starts rising well before training "ends"
- Continued training only memorises noise from there on

```python
best_val_loss = float('inf')
patience = 5
counter = 0

for epoch in range(max_epochs):
    train(...)
    val_loss = evaluate(val_loader)
    
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        counter = 0
        torch.save(model.state_dict(), 'best.pt')
    else:
        counter += 1
        if counter >= patience:
            print(f'Early stopping at epoch {epoch}')
            break

model.load_state_dict(torch.load('best.pt'))
```

Full coverage: see `14EarlyStopping.md`.

---

## 7. Reduce Model Capacity

If your model is too big for your data, just **use a smaller architecture**.

```
Too much capacity → easy to overfit
Right capacity    → enough to learn the patterns, not memorise

Options:
   - Fewer layers
   - Fewer filters per layer
   - Smaller fully-connected head
   - Use efficient architectures (MobileNet, EfficientNet-Lite)
```

A 5M-parameter model on 10,000 images often generalises better than a 50M-parameter model.

---

## CNN-Specific Considerations

### Spatial Augmentation Helps More

Unlike tabular data, CNNs benefit massively from **spatial transformations** (flip, rotate, crop). Why? Because the spatial structure is what makes images images.

### Pretrained Models Are Almost Always Available

Vision has the **best transfer learning ecosystem** of any domain. Always try transfer learning first.

### Shortcut Learning Is a Real Risk

CNNs can latch onto **spurious features** (background, watermarks, colour distributions):

```
"Husky vs Wolf" classifier → actually detected SNOW (wolves photographed in snow)
"Pneumonia X-ray" model    → actually detected HOSPITAL TAGS on the images
```

**Visualise** what your CNN is looking at (Grad-CAM) to catch shortcuts.

Full coverage: see `22VisualizingCNN.md`.

---

## Quick Decision Guide

| Symptom | First fix to try |
|---------|------------------|
| **Big gap** between train/val | Add dropout, augmentation |
| Val loss never goes down | Try transfer learning |
| Tiny dataset (< 1K images) | Transfer learning + augmentation |
| Medium dataset | Augmentation + weight decay + early stopping |
| Large dataset, still overfitting | Smaller model or more aggressive dropout |
| Training works but test fails | Check for distribution shift / shortcut learning |

---

## Building a Robust Training Pipeline

A modern CNN training recipe combines almost everything:

```python
import torchvision.transforms as T
import torchvision.models as models
import torch.nn as nn
import torch.optim as optim

# 1. Augmentation (training only)
train_transform = T.Compose([
    T.RandomResizedCrop(224),
    T.RandomHorizontalFlip(),
    T.RandomRotation(15),
    T.ColorJitter(0.2, 0.2, 0.2),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 2. Transfer learning — start from ImageNet pretrained
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
model.fc = nn.Linear(model.fc.in_features, num_classes)

# 3. L2 weight decay + Adam
optimizer = optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-4)
criterion = nn.CrossEntropyLoss()

# 4. Training loop with early stopping
best_val_loss = float('inf')
patience = 5
counter = 0

for epoch in range(50):
    train_one_epoch(model, train_loader, optimizer, criterion)
    val_loss = validate(model, val_loader, criterion)
    
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        counter = 0
        torch.save(model.state_dict(), 'best.pt')
    else:
        counter += 1
        if counter >= patience:
            break

model.load_state_dict(torch.load('best.pt'))
```

This single recipe handles:
- Augmentation (#2)
- Transfer learning (#3)
- L2 weight decay (#4)
- Normalisation (built into pretrained model)
- Early stopping (#6)

Typically achieves strong generalisation with just hundreds to thousands of training images.

---

## How to Tell Generalisation Is Good

After training:

```
✓ Train and val accuracy are CLOSE (gap < 5%)
✓ Test accuracy ≈ val accuracy
✓ Model handles unseen variations (different lighting, angles, backgrounds)
✓ Grad-CAM shows the model attending to RELEVANT regions
✓ Confidence is calibrated (high prob → usually right; low prob → uncertain)
✓ Performance is similar across demographic groups (no shortcut to spurious features)
```

If any of these fail, go back to the playbook.

---

## Cross-References

| Topic | File |
|-------|------|
| General overfitting + regularisation | `12Regularization.md` |
| Batch / layer normalisation | `13Normalization.md` |
| Early stopping | `14EarlyStopping.md` |
| Data preparation | `19DataPreparation.md` |
| Data augmentation | `20DataAugmentation.md` |
| Transfer learning | `21TransferLearning.md` |
| Visualising CNN attention (for shortcut detection) | `22VisualizingCNN.md` |
| Evaluation metrics (for any classifier) | `C4/M3-Logistical/4Metrics.md` |

---

## Summary

```
CNNs overfit easily — they have MILLIONS of parameters.

The anti-overfitting playbook:
   1. More data           (the gold standard)
   2. Data augmentation   (cheap fake data)
   3. Transfer learning    (start from a strong model)
   4. Regularisation       (L2 + dropout)
   5. Batch normalisation  (also a mild regulariser)
   6. Early stopping       (don't train too long)
   7. Smaller model        (less capacity)

Modern training pipelines use 4-6 of these AT THE SAME TIME.

Detect overfitting:
   - Train accuracy rising, val accuracy stuck
   - Gap > 5% is suspicious
   - Visualise with Grad-CAM to check for shortcut learning
```

> Overfitting is the **default outcome** for CNNs without intervention. Your training pipeline must actively fight it. The playbook above is what every production CNN uses.
