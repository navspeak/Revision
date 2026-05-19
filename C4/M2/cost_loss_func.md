# Cost Function and Loss Function

The cost function measures **how wrong the model is** — a single number that summarises the total error across all training examples.

```
Cost function = how bad are my current β values?
```

The model's job during training is to **minimise the cost function**.

---

## Different Models, Different Cost Functions

| Model | Cost Function | Formula |
|-------|--------------|---------|
| Linear Regression | MSE | Σ(y − ŷ)² / n |
| Logistic Regression | Log-loss | −mean[y log(p) + (1−y) log(1−p)] |
| Neural Networks | Depends | MSE or Cross-entropy |

---

## Cost Function vs Loss Function

These terms are often used interchangeably. Technically:

```
Loss function   = error on a single training example
Cost function   = average loss over all training examples
```

In practice, people say "cost function" and "loss function" to mean the same thing.

---

## The Connection to Gradient Descent

```
Cost function defines the surface
Gradient descent navigates that surface to find the minimum

High cost → bad β values
Low cost  → good β values
Minimum   → best β values the model can find
```

When gradient descent nudges β — it nudges in the direction that **reduces the cost function**.
