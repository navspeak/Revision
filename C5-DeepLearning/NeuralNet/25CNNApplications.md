# CNN Applications — Classification, Detection, Segmentation, Face Recognition, OCR

CNNs aren't a single technique — they're a **family of approaches** applied to many vision tasks. The architecture stays similar; the **head and loss change** based on the task.

```
Image classification      →  WHAT is in this image?
Object detection           →  WHERE and WHAT are the objects?
Image segmentation         →  Which class does EACH PIXEL belong to?
Facial recognition         →  WHO is this person?
OCR (Optical Char Recog.)  →  WHAT TEXT is in this image?
```

Each builds on the previous in terms of complexity and information extracted.

---

## 1. Image Classification

**The simplest CNN task** — assign ONE label to the whole image.

```
Input:    image
Output:   single class label (with optional probabilities)

"What's in this picture?" → "a dog"
"What's in this picture?" → "a cat"
```

### How a CNN Does It

```
Image
   ↓
Conv layers extract features (edges → shapes → objects)
   ↓
Flatten + Dense head
   ↓
Softmax over classes
   ↓
Class with highest probability
```

### Output

```
For 1000-class ImageNet:
   [P(class_1), P(class_2), ..., P(class_1000)]
   → all probabilities sum to 1
   → predict the one with highest probability
```

### Loss Function

```
Multiclass classification → Categorical Cross-Entropy
nn.CrossEntropyLoss()
```

### Examples

- "Is this a cat, dog, or horse?"
- ImageNet 1000-class classification
- Medical: "Is this X-ray normal or pneumonia?"
- Quality control: "Is this product defective?"

**Key limitation:** classification gives ONE label per image. It doesn't tell you WHERE objects are or how many. For that → object detection.

---

## 2. Object Detection

**Extends classification** by also locating objects with bounding boxes.

```
Input:    image
Output:   list of (class, bounding box, confidence) for each detected object

"What objects are in this picture?"
   → "1 dog at (50, 100, 200, 300) confidence 0.95"
   → "2 cats at ... confidence ..."
   → "1 person at ... confidence ..."
```

### How It Extends Classification

```
Image classification:    1 label per IMAGE
Object detection:         many labels + locations per image

For each object found:
   - Class (what is it?)
   - Bounding box (where is it? [x, y, width, height])
   - Confidence score (how sure are we?)
```

### How a CNN Does It

```
Two main approaches:

Two-stage detectors (Faster R-CNN):
   Stage 1: propose candidate regions ("where MIGHT objects be?")
   Stage 2: classify each region + refine the box
   → accurate but slower

Single-stage detectors (YOLO, SSD, RetinaNet):
   One pass through the network
   Predicts class + box for every position simultaneously
   → faster, slightly less accurate (gap closing)
```

### Architecture

```
Image
   ↓
Conv layers (often pretrained, e.g., ResNet50 backbone)
   ↓
Feature maps preserved (NOT flattened)
   ↓
Detection head:
   - Bounding box regression (4 numbers per anchor)
   - Classification (softmax over classes per anchor)
   - Objectness score (is there ANY object here?)
   ↓
Non-Maximum Suppression (NMS) — remove duplicate detections
   ↓
List of final detections
```

### Loss Function

Detection requires a **combined loss**:

```
Total loss = classification loss (Cross-Entropy or BCE)
           + box regression loss (Smooth L1 or IoU loss)
           + objectness loss (BCE)
```

### Examples

- Self-driving cars (find pedestrians, cars, signs)
- Retail: count items on shelves
- Security cameras: detect intruders
- Medical: locate tumours in scans
- Sports analytics: track players

**Key advance over classification:** finds **multiple objects** at **specific locations**.

---

## 3. Image Segmentation

**Pixel-level classification** — every single pixel gets a class label.

```
Input:    image
Output:   mask of the same shape, with class for EACH PIXEL

"Which pixels are car? Which are road? Sky? Building?"
```

### What Makes It Unique

```
Image classification:    1 label for entire image
Object detection:         labels + bounding boxes per object
Image segmentation:        labels per PIXEL — most fine-grained
```

The output is a colour-coded mask matching the image's spatial dimensions.

### Two Types

```
Semantic segmentation:
   Label each pixel with its CLASS
   "Two pixels both car" → both labelled "car" (same colour)

Instance segmentation:
   Label each pixel + distinguish different INSTANCES of the same class
   "Two pixels both car" → labelled "car #1" and "car #2" separately
```

### How a CNN Does It

```
Encoder-decoder architecture (U-Net is canonical):

Image (H × W × 3)
   ↓ ENCODER: conv + pool layers (downsample)
Feature maps (low resolution, high semantic)
   ↓ DECODER: upsampling + conv (recover spatial detail)
Output mask (H × W × num_classes)
   → softmax per pixel
```

Skip connections from encoder to decoder preserve fine details.

### Loss Function

```
Per-pixel Cross-Entropy:
   apply CE loss to every pixel, then average

Or Dice Loss for imbalanced classes:
   measures overlap between predicted and ground truth mask
   robust when foreground is rare (medical tumours, etc.)
```

### Examples

- Medical imaging: outline tumours pixel-perfectly
- Self-driving: identify drivable area
- Satellite imagery: detect roads, buildings, deforestation
- Photo editing: separate foreground from background
- Augmented reality: replace surfaces in real-time

**Key advance:** **pixel-precise** understanding of the image.

---

## 4. Facial Recognition

**Identify or verify WHO a person is** from a face image.

```
Input:    face image
Output:   person's identity (or match score against a known face)

"Is this person Alice?"          (verification)
"Who is this person?"             (identification — search in a database)
```

### How CNNs Help

CNNs learn **unique features for each person's face** — eye shape, jaw line, nose width, distances between features. These features:

```
✓ Are STABLE across different lighting, angles, expressions
✓ Are DISTINCTIVE — different people produce different feature vectors
✓ Are LEARNED automatically — no hand-crafted facial landmarks
```

### Pipeline

```
1. Face DETECTION    →  find faces in the image (a detection task!)
2. Face ALIGNMENT     →  rotate/scale to a canonical pose
3. Feature EXTRACTION →  CNN produces a fixed-size embedding (e.g., 512-d vector)
4. MATCHING           →  compare embedding against known faces
                        → "same person" if vectors are CLOSE in feature space
```

### Architecture

```
Face image (e.g., 112×112)
   ↓
Pretrained CNN backbone (e.g., FaceNet, ArcFace)
   ↓
Output: 128-d or 512-d EMBEDDING vector
   ↓
Compare: cosine similarity between embeddings
   → same person if similarity > threshold (e.g., 0.6)
```

### Loss Function

Standard classification loss isn't ideal for face recognition. **Margin-based losses** are used:

```
Triplet Loss:
   pull anchor + positive (same person) close
   push anchor + negative (different person) apart

ArcFace / CosFace:
   add angular margin between class boundaries
   → much tighter clusters per identity
```

These produce **embeddings that cluster by identity**, even for people not seen during training.

### Examples

- Phone unlock (Face ID)
- Airport biometric gates
- Photo organising (Google Photos, Apple Photos)
- Surveillance and security
- Attendance systems

**Key advance:** doesn't classify into pre-defined classes — produces an **embedding** that generalises to unseen faces.

---

## 5. OCR — Optical Character Recognition

**Recognise text in images** and convert it to digital characters.

```
Input:    image containing text (sign, document, receipt, etc.)
Output:   the text as a string

"What does this say?"
   → "Welcome to New York"
```

### Pipeline

```
1. Text DETECTION:
   Find regions of the image that contain text
   → bounding boxes around words/lines

2. Text RECOGNITION:
   For each detected region, identify the characters
   → "STOP", "Welcome", "$12.99"
```

### How CNNs Help

CNNs learn visual patterns of characters:

```
Layer 1: detect edges, strokes
Layer 2: detect character parts (curves, lines)
Layer 3: detect whole characters
Layer 4: build words / sequences from characters
```

### Architecture — CRNN (CNN + RNN)

Modern OCR often combines CNN with RNN:

```
Image of a word (e.g., "HELLO")
   ↓
CNN extracts visual features (preserves left-to-right spatial info)
   ↓
RNN (LSTM or GRU) reads the features sequentially
   → handles variable-length text
   ↓
Output: sequence of character predictions
   → "H", "E", "L", "L", "O"
```

Modern systems use Transformers instead of RNN, but the principle is the same.

### Loss Function

```
CTC Loss (Connectionist Temporal Classification):
   handles variable-length output sequences
   doesn't need character-level alignment in training
```

### Examples

- Scanning documents into editable text
- Reading licence plates
- Extracting receipts and invoices
- Digitising historical archives
- Real-time translation (point camera at sign → translation)

**Key advance:** converts unstructured pixel data into **structured, searchable text**.

---

## Comparison Table

| Task | Output per image | Granularity | Common Loss | Use case |
|------|------------------|-------------|-------------|----------|
| **Classification** | 1 label | Whole image | Cross-Entropy | "What's in this image?" |
| **Object Detection** | List of (class, box) | Object level | CE + Smooth L1 | "Where are the objects?" |
| **Segmentation** | Mask same shape as image | Pixel level | Per-pixel CE / Dice | "Label every pixel" |
| **Face Recognition** | Embedding vector | Whole face | Triplet / ArcFace | "Who is this?" |
| **OCR** | Text string | Character / word | CTC Loss | "Read this text" |

---

## How They Build on Each Other

```
Classification:        WHAT
Detection:             WHAT + WHERE
Segmentation:          WHAT for every PIXEL
Face Recognition:      WHO (specific identity)
OCR:                   WHAT TEXT
```

Each task adds more granularity / specificity. The conv backbone is often the SAME — only the **head** and **loss** change.

---

## Modern Approaches (Beyond Pure CNNs)

```
Vision Transformers (ViT):
   - Replace conv layers with attention
   - State-of-the-art on classification

DETR (Detection Transformer):
   - Object detection using Transformers
   - Removes need for anchors and NMS

Segment Anything (SAM, 2023):
   - Foundation model for segmentation
   - Works on any object class

CLIP:
   - Joint image + text embeddings
   - Enables zero-shot classification
```

Even with Transformers winning some benchmarks, **CNN principles remain foundational** — convolutions are still used in many state-of-the-art models.

---

## Quick Answers to the Practice Questions

```
Q: What does a CNN learn in image classification?
A: Predict a SINGLE LABEL that best describes the whole image.

Q: How does object detection extend classification?
A: Identifies MULTIPLE OBJECTS and their POSITIONS (bounding boxes).

Q: What's unique about image segmentation?
A: Labels EVERY PIXEL based on the object it belongs to.

Q: How do CNNs contribute to facial recognition?
A: Learn UNIQUE PATTERNS in facial features → produce embeddings
   that identify individuals.

Q: What problem does OCR solve using CNNs?
A: Recognises TEXT CHARACTERS from images and converts them into
   digital (machine-readable) form.
```

---

## Summary

```
CNNs power most computer vision tasks:

1. CLASSIFICATION    → "what's in this image?" (one label)
2. DETECTION          → "what + where?" (boxes around objects)
3. SEGMENTATION       → "label every pixel"
4. FACE RECOGNITION   → "who is this person?" (embedding-based)
5. OCR                → "what text is here?" (CNN + sequence model)

Same conv backbone, different heads and losses.
Each task = more granular understanding than the previous.
```

> CNNs go far beyond "classify this image". The same architecture, with different output heads, drives medical imaging, self-driving cars, photo apps, biometric security, and document digitisation. **One technology, dozens of applications.**
