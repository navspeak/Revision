# Classification

Classification is predicting **which category** something belongs to — not a number, but a label.

---

## Regression vs Classification

| | Regression | Classification |
|-|------------|----------------|
| Output | A number | A category / class label |
| Example | Predict exam score | Pass or Fail? |
| Example | Predict house price | Fraud or Not Fraud? |
| Example | Predict revenue | Spam or Not Spam? |

---

## Simple Example

You have study hours → predict Pass / Fail.

```
Hours studied:  1   2   3   4   5   6   7
Outcome:       F   F   F   P   P   P   P
```

This is a **binary classification** problem — two possible outcomes.

---

## Binary vs Multiclass

| Type | # of Classes | Example |
|------|-------------|---------|
| Binary | 2 | Pass/Fail, Spam/Not Spam, Fraud/Not Fraud |
| Multiclass | 3+ | Dog/Cat/Bird, Low/Medium/High, A/B/C/D/F |

---

## Decision Boundary

The decision boundary is the line (or curve) that separates one class from another.

```
Hours:   1    2    3  |  4    5    6    7
Outcome: F    F    F  |  P    P    P    P
                      ↑
               Decision boundary
               (e.g., threshold at 3.5 hours)
```

- Points on one side → Class 0 (Fail)
- Points on the other side → Class 1 (Pass)

In 2D (two features) the boundary is a line. In higher dimensions it becomes a hyperplane.

---

## Why Not Linear Regression for Classification?

If you apply linear regression to a binary target (0/1):

- Predictions can go **below 0** or **above 1** — not valid probabilities
- A prediction of 0.7 makes sense. A prediction of 2.3 does not.
- The model treats classes as if 0→1→2 is a meaningful scale (it isn't for categories)

**Fix:** Use a model that outputs a value between 0 and 1 — a probability. That is what Logistic Regression does.

---

## The Goal of Classification

Given features X, predict the class label y:

```
X (features) → model → P(y = 1 | X) → threshold → class label
```

1. Model outputs a **probability** (e.g., 0.82)
2. Apply a **threshold** (default: 0.5)
3. If probability ≥ 0.5 → predict class 1
4. If probability < 0.5 → predict class 0
