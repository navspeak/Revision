# Neural Networks — Module Overview

Neural Networks are the foundation of modern deep learning. They power image recognition, NLP, speech, recommendation systems, and most state-of-the-art AI today.

This module covers **classical feedforward networks** — the building blocks. Specialised architectures (CNNs, RNNs, Transformers) are covered in separate modules.

---

## Files

| # | File | Topic |
|---|------|-------|
| 1 | `1Introduction.md` | What is a neural network, motivation, applications |
| 2 | `2HumanVsArtificial.md` | Biological neurons vs artificial neurons |
| 3 | `3Architecture.md` | Layers, neurons, weights, biases, hyperparameters |
| 4 | `4NetworkTypes.md` | Feedforward, CNN, RNN — when to use which |
| 5 | `5ActivationFunctions.md` | Why non-linearity matters, sigmoid, ReLU, tanh, softmax |
| 6 | `6HiddenLayers.md` | Role, depth, expressive power, universal approximation |
| 7 | `7ForwardProp.md` | How input flows through layers to produce output |
| 8 | `8BackwardProp.md` | Computing gradients via chain rule |
| 9 | `9Optimizers.md` | SGD, mini-batch, momentum, RMSProp, Adam |

---

## Key Concepts to Remember

```
Forward propagation  → input → predictions
Loss function        → measures how wrong predictions are
Backpropagation      → computes gradient of loss w.r.t. weights
Optimizer            → uses gradients to update weights
Activation function  → adds non-linearity (essential for learning)
Hidden layers        → enable hierarchical feature learning
```

The basic training loop:

```
1. Forward pass    → compute predictions
2. Compute loss    → measure error
3. Backward pass   → compute gradients
4. Update weights  → optimizer takes a step
5. Repeat
```

---

## Learning Objectives

By the end of this module you should be able to:

- Explain what a neural network is and why it works
- Describe the forward and backward propagation algorithms
- Choose appropriate activation functions per layer
- Understand the role of depth and width
- Pick the right optimizer (and why Adam is the default)
- Connect neural network concepts to deep learning architectures used today
