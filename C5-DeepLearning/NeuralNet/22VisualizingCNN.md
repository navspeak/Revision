# Visualising CNN Activations

CNNs are often called "black boxes" — but they're actually one of the **more interpretable** deep learning models. By inspecting filters, activations, and gradient flows, you can literally **see what the network has learned**.

```
What does the CNN "look at" when predicting "cat"?
What patterns does the first conv layer detect?
Where in the image is the network paying attention?

→ Visualisation answers all of these.
```

---

## Why Visualise?

```
✓ Debug — understand why the model is making wrong predictions
✓ Trust — confirm the model uses relevant features (not shortcuts)
✓ Insight — see what the network has actually learned
✓ Fairness — detect biases (model relying on background, gender, etc.)
✓ Communication — explain models to non-technical stakeholders
```

In high-stakes domains (medicine, finance, hiring), interpretability is often a regulatory requirement.

---

## What to Visualise

There are four main techniques, each answering a different question:

```
1. FILTER VISUALISATION       → what patterns does each filter detect?
2. ACTIVATION MAPS             → what does the network "see" at each layer?
3. ATTRIBUTION / SALIENCY       → which input pixels matter most?
4. CLASS ACTIVATION MAPS (CAM) → where in the image is the network looking?
```

---

## 1. Filter Visualisation

The actual learned filter weights of a conv layer can be displayed as small images.

```
First-layer filters (3×3 or 5×5):
   Typically look like edge detectors, Gabor filters, colour blobs
   → very interpretable

Deeper-layer filters:
   Harder to interpret directly — they detect compositions of lower features
```

### Example

```python
import matplotlib.pyplot as plt

# Get the first conv layer's filters
filters = model.conv1.weight.data    # shape: (64, 3, 7, 7)

# Plot a few
for i in range(8):
    plt.subplot(2, 4, i+1)
    plt.imshow(filters[i].permute(1, 2, 0))  # convert to (H, W, C)
    plt.axis('off')
plt.show()
```

What you'll see: edges in different orientations, colour gradients, simple textures — classic early-vision features.

---

## 2. Activation Maps (Feature Maps)

Show what the network "produces" at each layer when fed a specific image.

```
Input image → conv layer 1 → 64 feature maps (one per filter)
                            → some are bright where the input had edges
                            → some are bright where there were specific textures
```

### Example

```python
# Hook to capture activations
activations = {}
def hook(module, input, output):
    activations['conv1'] = output

model.conv1.register_forward_hook(hook)

# Forward pass
output = model(input_image)

# Visualise activation maps
feature_maps = activations['conv1'][0]  # first image in batch, shape (64, H, W)
for i in range(8):
    plt.subplot(2, 4, i+1)
    plt.imshow(feature_maps[i].cpu(), cmap='viridis')
    plt.axis('off')
plt.show()
```

What you'll see:
```
Early layers: edges, gradients clearly visible in feature maps
Middle layers: shapes, textures, blobs
Late layers: abstract, less interpretable — high-level concepts
```

---

## 3. Saliency / Attribution Maps

Show **which input pixels most influence the prediction** by computing gradients of the output with respect to the input.

```
∂(predicted_score) / ∂(input_pixel)
   = "how much does this pixel matter for the prediction?"

→ map of importance over the input image
```

### Common Techniques

| Method | Description |
|--------|-------------|
| **Vanilla Saliency** | Plot the gradient of output w.r.t. input |
| **Integrated Gradients** | Integrate gradient along a path from baseline to input |
| **SmoothGrad** | Average saliency over noisy versions of the input |
| **Guided Backpropagation** | Modified gradient — cleaner visualisations |

### Simple Saliency in PyTorch

```python
input_image.requires_grad = True
output = model(input_image)
predicted_class = output.argmax(dim=1)
output[0, predicted_class].backward()
saliency = input_image.grad.abs().squeeze()
plt.imshow(saliency.cpu(), cmap='hot')
```

What you'll see: bright spots over the **important regions** of the image (e.g., the cat's face, not the background).

---

## 4. Class Activation Maps (CAM / Grad-CAM)

The most popular CNN interpretability tool — **shows the spatial region the network is "attending to"** for a specific class prediction.

```
Grad-CAM highlights image regions important for the decision.
   → "the network thinks this is a dog BECAUSE of this part of the image"
```

### How Grad-CAM Works (Conceptually)

```
1. Forward pass: get the final conv layer's feature maps
2. Backward pass: compute gradients of the target class w.r.t. those feature maps
3. Average gradients per channel → get importance weights
4. Weighted sum of feature maps → heatmap
5. Overlay heatmap on the original image
```

### Visualisation Result

```
Original image: dog standing on grass

Grad-CAM heatmap:
   - Bright red over the dog's face and body
   - Dark over the background grass

→ The network correctly focuses on the dog, not the surroundings.
```

If Grad-CAM showed the bright region over the background → the model is using **shortcut features** (e.g., "grass = dog photos") and won't generalise to dogs on different backgrounds.

### Library

```python
# Easy way: use pytorch-grad-cam or captum
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image

cam = GradCAM(model=model, target_layers=[model.layer4[-1]])
grayscale_cam = cam(input_tensor=input_image)
visualization = show_cam_on_image(image_np, grayscale_cam[0])
plt.imshow(visualization)
```

---

## Detecting Model Failures via Visualisation

Common things visualisation reveals:

```
✓ Shortcut learning: model uses watermarks, captions, or backgrounds
   instead of the actual subject

✓ Bias: model focuses on faces, gender, or skin tone instead of relevant features

✓ Overfitting: model attends to specific pixel-level noise

✓ Spurious correlations: model learned that "all photos with snow → wolves"
   (a famous example: Wolves vs Huskies classifier was actually a "snow detector")
```

Without visualisation, these failures stay hidden until production.

---

## Famous Examples

```
Husky vs Wolf classifier:
   Looked great in accuracy.
   Grad-CAM showed it was looking at SNOW (background).
   → it was a snow detector, not a wolf detector.

Pneumonia X-ray classifier:
   Achieved high accuracy.
   Visualisation showed it was using HOSPITAL MARKERS on X-rays.
   → it learned "this hospital does more pneumonia cases" not pneumonia itself.

Medical diagnosis models:
   Often discovered to focus on irrelevant artefacts (scanner type, patient position).
   Visualisation catches this before deployment.
```

---

## Why CNNs Are More Interpretable Than MLPs

```
MLP: flat input → fully connected layers → output
     → no spatial information → can't visualise WHERE attention goes
     → harder to debug

CNN: input image → conv feature maps → output
     → SPATIAL feature maps maintained through layers
     → can ALWAYS overlay attention back onto the original image
     → visualisations have natural spatial meaning
```

This is one of the underrated benefits of CNNs.

---

## Modern Interpretability Tools

```
Captum (PyTorch)               → comprehensive attribution library
                                 supports Integrated Gradients, SHAP, etc.

pytorch-grad-cam               → Grad-CAM and variants

Lucid (TensorFlow)             → feature visualisation, activation atlases

torchinfo                       → model summary (params, shapes)

tensorboard.plugins.histogram   → distributions of weights and gradients

Weights & Biases (wandb)        → experiment tracking + visualisations
```

---

## Visualisation Tips

```
✓ ALWAYS visualise during early development — not just at the end
✓ Look at training images that the model gets wrong
✓ Compare visualisations across multiple architectures
✓ Combine multiple techniques (saliency + Grad-CAM gives richer insights)
✓ Track changes during training — see what the model learns over time
```

---

## Summary

```
CNN Visualisation:

1. Filter visualisation
   → see the actual learned filter weights
   → especially interpretable for early layers (edges, textures)

2. Activation maps
   → see what each layer "produces" for a specific input
   → reveals the feature hierarchy

3. Saliency / Attribution
   → see which input pixels matter most
   → vanilla saliency, Integrated Gradients, SmoothGrad

4. Class Activation Maps (Grad-CAM)
   → see WHERE in the image the network focuses
   → the gold standard for visual interpretability

Used for:
   Debugging
   Detecting bias / shortcut learning
   Building trust in high-stakes applications
   Communicating model behaviour
```

> CNNs aren't true black boxes — they're transparent if you know what to visualise. **Always inspect what your model is looking at** before deploying it. Visualisation is the difference between "the model works" and "I understand why the model works".
