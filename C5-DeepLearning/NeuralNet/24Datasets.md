# Common Vision Datasets

Reference for the standard benchmark datasets used in CNN research and learning. **CIFAR** is the most-mentioned, but you'll meet all of these.

```
MNIST            → "Hello World" of vision
Fashion-MNIST    → harder MNIST
CIFAR-10         → standard CNN benchmark
CIFAR-100        → harder CIFAR
ImageNet         → real-world classification benchmark
COCO             → object detection / segmentation
```

---

## CIFAR — Canadian Institute for Advanced Research

A famous benchmark dataset for computer vision research, named after the **Canadian Institute for Advanced Research**.

```
CIFAR-10  →  60,000 images, 10 classes (size 32×32)
CIFAR-100 →  60,000 images, 100 classes (size 32×32)
```

The **"Hello World" dataset for CNN research** — small enough to train quickly, challenging enough to be useful.

### CIFAR-10 Details

```
60,000 colour images, 32×32 pixels, 3 channels (RGB)
   - 50,000 training images
   - 10,000 test images

10 classes (6,000 images each):
   airplane, automobile, bird, cat, deer,
   dog, frog, horse, ship, truck
```

Examples per class:

```
airplane  →  passenger jets, fighter planes, prop planes
cat       →  domestic cats in different poses
ship      →  cargo ships, yachts, boats
truck     →  delivery trucks, semi-trailers
```

### CIFAR-100 Details

```
Same setup as CIFAR-10, but 100 classes (only 600 images each).

100 fine-grained classes grouped into 20 SUPERCLASSES:
   aquatic mammals    →  beaver, dolphin, otter, seal, whale
   fish                →  aquarium fish, flatfish, ray, shark, trout
   flowers             →  orchid, poppy, rose, sunflower, tulip
   ...

More classes, fewer examples per class → much harder.
```

### Why CIFAR Matters

```
✓ SMALL — fits in memory, trains in minutes (with a GPU)
✓ STANDARD — every paper compares against CIFAR-10/100 accuracy
✓ HARD ENOUGH — distinguishing cats from dogs at 32×32 is non-trivial
✓ FREE — public, no licensing issues
✓ BALANCED — equal examples per class
```

### Image Format

```
32×32 pixels, 3 channels (RGB)
   → each image is 3,072 numbers

Tiny by modern standards (ImageNet is 224×224, ~50× larger).

Why so small?
   - Original release in 2009 (compute was limited)
   - Forces models to learn from low-resolution
   - Makes training fast
```

When you look at a CIFAR image, you can BARELY tell what it is at native size — even humans get 5-10% wrong.

### Typical CNN Accuracy on CIFAR-10

```
Random guessing:           10%
Simple MLP:                ~50%
Basic CNN (LeNet-like):    ~75-85%
VGG-style CNN:             ~90-93%
ResNet:                    ~93-95%
Modern architectures:      96-99%
SOTA (with extra tricks):   99.5%+
```

Reaching 90% is a standard CNN exercise. Beyond 95% requires careful design.

### Loading CIFAR in PyTorch

```python
import torchvision
import torchvision.transforms as T

transform = T.Compose([
    T.ToTensor(),
    T.Normalize(
        mean=[0.4914, 0.4822, 0.4465],   # CIFAR-10 channel means
        std=[0.2023, 0.1994, 0.2010]     # CIFAR-10 channel stds
    )
])

trainset = torchvision.datasets.CIFAR10(
    root='./data', train=True, download=True, transform=transform
)
testset = torchvision.datasets.CIFAR10(
    root='./data', train=False, download=True, transform=transform
)
```

`torchvision` downloads the dataset automatically (~170 MB).

### A Simple CIFAR CNN

```python
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(128 * 4 * 4, 256)
        self.fc2 = nn.Linear(256, num_classes)
        self.dropout = nn.Dropout(0.5)
    
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))   # 32×32 → 16×16
        x = self.pool(F.relu(self.conv2(x)))   # 16×16 → 8×8
        x = self.pool(F.relu(self.conv3(x)))   # 8×8 → 4×4
        x = x.view(x.size(0), -1)
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)
        return x
```

Hits ~80% in 30 epochs. Add augmentation + batch norm + skip connections to push higher.

### Tricks for High CIFAR-10 Accuracy

```
Architecture:
   ResNet (with skip connections)     → 93-95%
   DenseNet, EfficientNet              → similar

Augmentation:
   Random crop (with padding)
   Random horizontal flip
   AutoAugment / RandAugment           → +1-2%
   MixUp / CutMix                       → +1-2%

Regularisation:
   Weight decay (L2)
   Dropout (mild — 0.1-0.3)
   Label smoothing

Training:
   Cosine learning rate schedule
   SGD with momentum + warmup
   200+ epochs
```

Combined, these push CIFAR-10 over 96%.

---

## MNIST — The Original Vision Benchmark

```
70,000 grayscale images of handwritten digits (0-9)
   - 60,000 training
   - 10,000 test
   - 28×28 pixels, 1 channel
   
10 classes (the digits 0-9)
```

```
Random guessing: 10%
Logistic regression: ~92%
Simple MLP: ~98%
Basic CNN: ~99%+
SOTA: 99.9%+
```

**Considered "solved"** — too easy to be interesting for modern research. Used in tutorials only.

---

## Fashion-MNIST — A Slightly Harder MNIST

```
Same format as MNIST (70K, 28×28 grayscale, 10 classes)
BUT classes are: T-shirt, trouser, pullover, dress, coat,
                  sandal, shirt, sneaker, bag, ankle boot

Harder than MNIST because:
   - Similar items (shirt vs T-shirt vs pullover)
   - More variation per class
```

```
Basic CNN: ~90%
Modern CNN: ~95%
```

Drop-in replacement for MNIST when you want a slightly more challenging task.

---

## ImageNet — The Big One

```
1.2 MILLION training images
   50,000 validation images
   100,000 test images
   
1,000 classes (fine-grained: 120 dog breeds, 90 plant species, etc.)
Image size: variable (typically resized to 224×224 or 256×256)
```

```
Random: 0.1%
AlexNet (2012): 63% top-1 accuracy   ← the breakthrough
VGG / GoogLeNet: ~73%
ResNet (2015): 76%+
EfficientNet: 84%+
Vision Transformer: 87%+
SOTA: 90%+ top-1
```

**THE benchmark for image classification.** Pretrained models almost always come from ImageNet.

Used for transfer learning everywhere — see `21TransferLearning.md`.

---

## COCO — Common Objects in Context

```
330,000 images
80 object categories (with bounding boxes, segmentation masks, captions)

Used for:
   ✓ Object detection
   ✓ Semantic / instance segmentation
   ✓ Keypoint detection (poses)
   ✓ Image captioning
   ✓ Panoptic segmentation
```

Much richer than CIFAR/ImageNet — multiple objects per image, with location info. Standard for detection / segmentation research.

---

## Comparison Table

| Dataset | Images | Classes | Size | Channels | Typical use |
|---------|--------|---------|------|----------|-------------|
| **MNIST** | 70K | 10 (digits) | 28×28 | 1 | Trivial, "Hello World" |
| **Fashion-MNIST** | 70K | 10 (clothes) | 28×28 | 1 | Slightly harder MNIST |
| **CIFAR-10** | 60K | 10 | 32×32 | 3 | Standard CNN benchmark |
| **CIFAR-100** | 60K | 100 | 32×32 | 3 | Harder, fine-grained |
| **ImageNet** | 1.2M | 1000 | ~224×224 | 3 | Real-world classification, pretraining |
| **COCO** | 330K | 80 (with boxes) | Variable | 3 | Object detection / segmentation |

CIFAR sits in the **middle** — harder than MNIST, faster to train than ImageNet.

---

## Other Useful Datasets

```
SVHN (Street View House Numbers):
   600K real-world digit images from Google Street View.
   Harder than MNIST. 10 classes (0-9).

CelebA:
   200K celebrity face images with 40 binary attributes.
   Used for face recognition, attribute prediction, GANs.

Cityscapes:
   5K high-res street scenes with pixel-level annotations.
   Standard for autonomous driving segmentation research.

LFW (Labelled Faces in the Wild):
   13K face images for face recognition / verification.

VOC (PASCAL Visual Object Classes):
   20 categories. Older but still cited. Detection / segmentation.

OpenImages:
   9M+ images. Largest open dataset for vision.

KITTI:
   Autonomous driving dataset with LiDAR + camera data.
```

---

## Choosing a Dataset for Practice

```
First neural network ever?         → MNIST (5 minutes to train)
Learning CNNs:                       → CIFAR-10 (real but tractable)
Trying transfer learning:            → CIFAR-10 with ImageNet-pretrained ResNet
Studying object detection:          → COCO
Want a SOTA benchmark:               → ImageNet (need a GPU cluster)
```

---

## Where You'll See These Datasets Used

```
✓ Almost every deep learning paper uses CIFAR-10 or ImageNet
✓ PyTorch / TensorFlow tutorials default to MNIST or CIFAR
✓ Course assignments lean on MNIST and CIFAR-10
✓ Pretrained models (ResNet, VGG, etc.) → trained on ImageNet
✓ Modern object detection → COCO
```

---

## Summary

```
CIFAR = Canadian Institute for Advanced Research

CIFAR-10:   60K colour images, 10 classes, 32×32
   → standard CNN benchmark
   → harder than MNIST, faster to train than ImageNet

CIFAR-100:  same but 100 classes (harder)

Other key datasets:
   MNIST:       70K, 10 digits, 28×28 grayscale (trivial)
   Fashion-MNIST: same format, clothing (slightly harder)
   ImageNet:    1.2M, 1000 classes (real-world benchmark)
   COCO:        330K, 80 categories with boxes (detection)
```

> CIFAR-10 is to computer vision what XOR is to neural networks — the universal "does my approach work?" test. Master it before tackling anything bigger.
