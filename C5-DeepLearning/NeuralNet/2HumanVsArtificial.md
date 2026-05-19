# Human Neuron vs Artificial Neuron

The "neural" in neural networks comes from biology. Artificial neurons are **inspired by** — but not identical to — biological ones.

```
Biological neuron:  cell in the brain that receives, processes, transmits signals
Artificial neuron:  mathematical unit that does weighted sum + activation
```

---

## Biological Neuron — Structure

| Part | Function |
|------|----------|
| **Dendrites** | Receive input signals from other neurons |
| **Cell body (soma)** | Sums up incoming signals; decides whether to fire |
| **Axon** | Transmits output signal to other neurons |
| **Synapses** | Connections between axon and next neuron's dendrites |

The neuron **fires** (sends a signal) if the combined input exceeds a threshold. Otherwise it stays silent.

---

## Artificial Neuron — Structure

| Component | Mathematical Equivalent | Purpose |
|-----------|------------------------|---------|
| **Inputs (x₁, x₂, ...)** | Feature values | Data entering the neuron |
| **Weights (w₁, w₂, ...)** | Learned multipliers | Importance of each input |
| **Bias (b)** | Constant offset | Shifts the decision boundary |
| **Summation** | z = Σ wᵢ·xᵢ + b | Combined input signal |
| **Activation (σ)** | Non-linear function | Decides output magnitude (analogous to firing) |
| **Output (a)** | a = σ(z) | Signal passed to next layer |

---

## Visual Comparison

```
BIOLOGICAL NEURON                      ARTIFICIAL NEURON

  dendrites                              x₁ ──w₁──┐
   \                                     x₂ ──w₂──┤
    \                                              ├── Σ ──► σ ──► output
     \                                   x₃ ──w₃──┤        ↑
      ⬡  cell body  ──axon──►            ...      │      activation
     /                                   x_n──w_n──┘
    /                                                   bias b added
   /
  synapses

  Fires through axon when                Output activates when
  inputs exceed a threshold              weighted sum + bias is large
```

The artificial neuron is a **simplified mathematical caricature** of the biological one.

---

## Information Flow

### In a biological neuron

```
1. Dendrites receive electrical signals from other neurons
2. These signals are summed in the cell body
3. If the sum crosses a threshold → neuron FIRES
4. Action potential travels down the axon
5. Synapses pass the signal to next neurons
   (chemical neurotransmitters)
```

### In an artificial neuron

```
1. Inputs arrive (x₁, x₂, ..., x_n)
2. Each is multiplied by its weight (xᵢ × wᵢ)
3. Sum + bias: z = Σ wᵢxᵢ + b
4. Apply activation: a = σ(z)
5. Pass a to next layer
```

Same conceptual flow — receive, sum, activate, transmit. But the math is much simpler.

---

## Learning Mechanisms

| Human Brain | Artificial Neural Network |
|-------------|--------------------------|
| Strengthens synapses through use (Hebbian learning) | Updates weights via backpropagation + gradient descent |
| Slow, adaptive, lifetime learning | Fast batch training, then frozen |
| Plasticity — rewires under experience | Architecture fixed during inference |
| Energy efficient (~20W) | Energy hungry (kilowatts during training) |
| One-shot / few-shot learning common | Requires many examples |
| Continuous, online, unsupervised | Mostly batch, supervised |

The brain is **vastly more efficient and adaptive** than current ANNs. But ANNs scale better with data and compute.

---

## Mathematical Representation

Each artificial neuron performs:

```
z = w₁·x₁ + w₂·x₂ + ... + w_n·x_n + b
a = σ(z)
```

Where:
- `xᵢ` = inputs
- `wᵢ` = weights (learned)
- `b` = bias (learned)
- `σ` = activation function (ReLU, sigmoid, tanh, ...)
- `a` = output activation

In matrix form for a whole layer:

```
z = W·x + b
a = σ(z)
```

`W` is a weight matrix, `x` is an input vector, `b` is a bias vector. One matrix multiplication does the work of many neurons in parallel.

---

## Key Differences

```
Brain                                Artificial NN
────────────────────                ────────────────────
~86 billion neurons                  thousands to billions (e.g., GPT-3 ~96B params)
Continuous spike trains              Discrete forward/backward passes
Robust to noise & damage             Brittle to adversarial perturbation
Wet, biological                       Silicon-based computation
Learns from few examples              Needs lots of training data
Energy: ~20W                         Energy: kilowatts → megawatts
Conscious experience (?)             None — purely mathematical
```

---

## What ANNs Get Right

```
✓ Layered organisation (like cortex)
✓ Weighted connections (like synaptic strengths)
✓ Non-linear activation (like firing thresholds)
✓ Learning by adjusting connections (like Hebbian learning)
✓ Distributed representations (like population coding)
```

These shared principles let ANNs achieve impressive results on tasks the brain handles — vision, language, motor control — even though the underlying mechanisms differ.

---

## What ANNs Get Wrong (Compared to Brains)

```
✗ No spiking dynamics (biological neurons spike — most ANNs don't)
✗ No temporal coding
✗ Mostly feedforward (brain has rich feedback loops)
✗ No truly continuous learning
✗ No embodiment / no real-world grounding
✗ Energy efficiency is orders of magnitude worse
```

These gaps motivate research in **neuromorphic computing**, **spiking neural networks**, and **continual learning** — bringing ANNs closer to biological inspiration.

---

## Summary

```
Biological neuron       → cell that sums signals and fires above a threshold
Artificial neuron       → math unit: weighted sum + non-linear activation

ANN ≈ caricature of brain — same structure, very different mechanism.

Brain: more efficient, robust, adaptive, conscious(?)
ANN:  scales with data and compute, learns from examples

The brain remains the inspiration, but ANNs are their own thing.
```

> The biology is just a **metaphor**. What makes neural networks powerful isn't that they mimic the brain — it's that they can learn complex functions from data by chaining many simple non-linear units together.
