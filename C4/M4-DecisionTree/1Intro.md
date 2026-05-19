# Decision Trees — Introduction

Linear models assume one global equation fits all data. Real-world data often doesn't — it bends, twists, changes direction depending on feature values.

Decision Trees take a different approach: break the prediction problem into a **series of smaller, simpler decisions** — like how humans actually decide things.

---

## The Umbrella Analogy

How do you decide whether to take an umbrella?

```
Is it cloudy?
   ├── No  → no umbrella
   └── Yes → Does the forecast say rain?
              ├── No  → no umbrella
              └── Yes → take umbrella
```

Each check reduces uncertainty until you land on a decision. That's exactly how a decision tree works.

---

## Why Trees vs Linear Models

| | Linear / Logistic | Decision Tree |
|-|-------------------|---------------|
| Approach | Fit one equation | Sequence of if/else rules |
| Captures non-linearity | Needs feature engineering | Natively |
| Captures interactions | No (without crossing features) | Yes |
| Interpretability | Coefficients | Rule path from root to leaf |
| Feature scaling needed | Yes | No |
| Handles categorical features | Needs one-hot encoding | Natively |

---

## Two Types of Trees

| Type | Target | Leaf prediction |
|------|--------|-----------------|
| **Classification Tree** | Categorical (e.g. Yes/No) | A class label |
| **Regression Tree** | Numerical (e.g. price) | A number |

The tree structure is the same — only how the leaf produces its prediction differs.

---

## Key Idea

> A decision tree is a **non-parametric** model — no equation, no β coefficients. It just learns a hierarchy of rules from data.

Each rule splits the data into more homogeneous groups. The process continues until groups are simple enough to make a prediction.
