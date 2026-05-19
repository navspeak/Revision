# Transfer Learning

**Reuse knowledge from a CNN trained on a large dataset** to accelerate and improve training on your specific task.

```
Train ResNet50 on ImageNet (1.2M images, 1000 classes) → costly, takes days/weeks
                              ↓
   Reuse those learned features for YOUR task (e.g., dog breeds, X-rays)
                              ↓
                Train in minutes, with thousands of times less data.
```

This is **the single most impactful technique** for applied deep learning in vision.

---

## The Core Idea

A CNN trained on ImageNet has learned **general visual features**:

```
Layer 1:  edges, corners, gradients
Layer 2:  textures, simple shapes
Layer 3:  object parts (eyes, wheels, leaves)
Layer 4:  complete objects (faces, cars, plants)
```

These features are **task-agnostic** — useful for ANY image task, not just the original ImageNet classes.

```
Why train edge detectors from scratch for your X-ray classifier?
ImageNet-trained CNNs already KNOW edges, textures, shapes.

Reuse them. Just adapt the last layers to your task.
```

---

## Why It Works So Well

```
✓ Pretrained features are GENERAL
   → useful for X-rays, satellite images, fashion, food, animals, etc.

✓ Massive data already invested
   → ImageNet has 1.2 million labelled images
   → trained on a 1000-class problem with rich visual variety

✓ Training a CNN from scratch is HARD
   → needs huge data (millions of images)
   → needs huge compute (days of GPU time)
   → most teams don't have this

✓ Transfer learning lets you piggyback on that investment
   → train competitive models with hundreds of images
   → fits on a single GPU in minutes
```

The vast majority of production vision models are built via transfer learning.

---

## Two Modes of Transfer Learning

### 1. Feature Extraction (Frozen Backbone)

```
Use the pretrained CNN as a FIXED feature extractor.
Replace the final classifier head with a new one for your task.
Train ONLY the new head.

Conv layers: FROZEN (weights don't update)
Head:        TRAINABLE (learns from scratch)
```

**When to use:**
- Very small dataset (few hundred to few thousand images)
- Your task is similar to ImageNet (natural images)

**Why it works:** features from ImageNet are already great; you just need to learn how to combine them for your task.

### 2. Fine-Tuning (Whole Network)

```
Initialise with pretrained weights.
Train the ENTIRE network on your data — including conv layers.
Use a SMALL learning rate so pretrained features don't get wrecked.
```

**When to use:**
- Larger dataset (thousands to millions of images)
- Your task differs significantly from ImageNet (e.g., medical scans)

**Why it works:** features start near-optimal; fine-tuning adapts them to your specific domain.

---

## When to Choose Which

| Dataset size | Domain | Strategy |
|--------------|--------|----------|
| Small (< 1K images) | Similar to ImageNet | **Feature extraction** |
| Small | Very different from ImageNet | Feature extraction + small head |
| Medium (1K-100K) | Similar to ImageNet | **Fine-tune last few layers** |
| Medium | Very different | Fine-tune more layers |
| Large (100K+) | Any | **Fine-tune entire network** |

---

## In PyTorch — Feature Extraction

```python
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights

# Load pretrained ResNet50
model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)

# Freeze all parameters
for param in model.parameters():
    param.requires_grad = False

# Replace the final classifier (originally 1000 classes for ImageNet)
num_classes = 10  # your task
model.fc = nn.Linear(model.fc.in_features, num_classes)
# Only model.fc has requires_grad=True now

# Train — only the head learns
optimizer = torch.optim.Adam(model.fc.parameters(), lr=1e-3)
```

The conv backbone is frozen. Training updates only the new head.

---

## In PyTorch — Fine-Tuning

```python
from torchvision.models import resnet50, ResNet50_Weights

# Load pretrained ResNet50
model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)

# Replace the final layer
model.fc = nn.Linear(model.fc.in_features, num_classes)

# Train EVERYTHING — but with a small learning rate
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)  # 100× smaller than usual!
```

Smaller learning rate prevents the pretrained features from being "forgotten" during early training.

### Even Better — Layer-Wise Learning Rates

```python
optimizer = torch.optim.Adam([
    {'params': model.layer4.parameters(), 'lr': 1e-5},   # late layers — fine-tune
    {'params': model.layer3.parameters(), 'lr': 1e-6},   # earlier layers — barely update
    {'params': model.layer2.parameters(), 'lr': 1e-7},
    {'params': model.fc.parameters(),     'lr': 1e-3}    # new head — train normally
])
```

The deeper into the network, the higher the learning rate. Earliest layers (edge detectors) barely need to change; late layers and the new head need more adjustment.

---

## Popular Pretrained Models

| Model | Parameters | Where it's used |
|-------|-----------|----------------|
| **ResNet50** | 25M | Strong general-purpose baseline |
| **ResNet101 / 152** | 44M / 60M | Slightly better, more compute |
| **EfficientNet** | 5M-66M | State-of-the-art accuracy/compute |
| **VGG16 / VGG19** | 138M / 144M | Historical, still teaching standard |
| **MobileNet** | 4M | Mobile / edge devices |
| **Vision Transformer (ViT)** | 86M-300M | Modern alternative to CNNs |
| **CLIP** | 100M-400M | Text-image joint training |

PyTorch's `torchvision.models` and Hugging Face's `transformers` give you these in one line of code.

---

## What Layers to Replace

The final layer needs to match YOUR task:

```
ImageNet:      1000-class softmax output
Your task:     binary classification → 1 output + sigmoid
               5-class classification → 5 outputs + softmax
               regression (age, etc.) → 1 output + linear
```

Replace the final layer to match. Optionally add intermediate dense layers if your task is complex.

```python
model.fc = nn.Sequential(
    nn.Linear(model.fc.in_features, 256),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(256, num_classes)
)
```

---

## Transfer Learning Beyond Classification

```
Object detection:
   Initialise CNN backbone from ImageNet
   Train detection-specific layers (anchors, classifier, box regressor)

Semantic segmentation:
   Initialise encoder from ImageNet
   Train task-specific decoder

NLP:
   Initialise from BERT / GPT pretrained on huge text corpora
   Fine-tune on your specific task (classification, NER, QA, etc.)

Audio:
   Initialise from audio classification models (PANN, YAMNet)
   Fine-tune on your dataset

Code:
   Initialise from CodeBERT / CodeGen
   Fine-tune for your language / task
```

**Transfer learning is the rule, not the exception**, across all of modern deep learning.

---

## When NOT to Use Transfer Learning

```
✗ Your data is COMPLETELY DIFFERENT from ImageNet
   - Galaxy spectroscopy, gene expression heatmaps, etc.
   - Even then, pretrained features sometimes help a little

✗ Your dataset is MASSIVE (millions of images)
   - Training from scratch can match or beat transfer learning
   - But this is rare — usually still worth starting pretrained

✗ Privacy / IP concerns
   - Some industries can't use models pretrained on web-scraped data
```

In 95%+ of cases, transfer learning is the right starting point.

---

## A Typical Training Recipe

```python
# 1. Load pretrained model
model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)

# 2. Replace head
model.fc = nn.Linear(model.fc.in_features, num_classes)

# 3. Prepare data with ImageNet normalisation
transform = T.Compose([
    T.RandomResizedCrop(224),
    T.RandomHorizontalFlip(),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 4. Fine-tune with small learning rate
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-4)
criterion = nn.CrossEntropyLoss()

# 5. Train for 10-50 epochs with early stopping
for epoch in range(50):
    for batch_x, batch_y in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(batch_x), batch_y)
        loss.backward()
        optimizer.step()
    # ... validate, early stop, etc.
```

This recipe gives strong results with **very little data** and minimal compute.

---

## Summary

```
Transfer learning =
   Take a CNN pretrained on a large dataset (e.g., ImageNet)
   Reuse its conv layers as a feature extractor
   Replace the final layers for YOUR task
   Train on YOUR data (cheap, fast, accurate)

Modes:
   Feature extraction (frozen backbone)  → for small datasets
   Fine-tuning (whole network)           → for larger datasets

Why it works:
   Early layers learn GENERIC visual features (edges, textures)
   These transfer to ANY image task
   Only the last few layers need to be task-specific

The DEFAULT approach in modern computer vision.
```

> Transfer learning is the **biggest practical advance** that made deep learning accessible. Instead of needing millions of images and weeks of training, you start with a pretrained model and train on **hundreds** of images in **minutes**.
