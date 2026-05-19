# Classification Metrics

After `model.predict()`, you need to measure how good the predictions are. For classification, the metrics are different from regression.

---

## Accuracy

The simplest metric:

```
Accuracy = (Number of correct predictions) / (Total predictions) × 100
```

### Example

10 students predicted, 8 correct:

```
Accuracy = 8/10 = 80%
```

In sklearn:

```python
from sklearn.metrics import accuracy_score
acc = accuracy_score(y_test, y_pred)
```

---

## The Problem with Accuracy — Imbalanced Data

Suppose you build a fraud detector. 99% of transactions are legitimate, 1% are fraud.

A model that **always predicts "not fraud"** gets:

```
Accuracy = 99/100 = 99%   ← looks great, but catches zero fraud
```

99% accuracy, completely useless. This is the imbalanced class problem.

**Fix:** Use metrics that look at each class separately — precision and recall.

---

## Confusion Matrix

Same structure as Type I / Type II errors in hypothesis testing:

| | H₀ is actually True | H₀ is actually False |
|---|---|---|
| **Reject H₀** | Type I Error (FP) ✗ | Correct (TP) ✓ |
| **Fail to reject H₀** | Correct (TN) ✓ | Type II Error (FN) ✗ |

- **Type I (FP)** — false alarm. Predicted positive, actually negative.
- **Type II (FN)** — missed signal. Predicted negative, actually positive.

In ML terms — using sklearn's convention (rows = actual, columns = predicted):

| | Predicted Negative | Predicted Positive |
|---|---|---|
| **Actually Negative** | TN — Correct ✓ | FP — Type I ✗ |
| **Actually Positive** | FN — Type II ✗ | TP — Correct ✓ |

This is the convention `sklearn.metrics.confusion_matrix` uses — negative class first, rows are the true labels, columns are the predictions:

```
confusion_matrix(y_test, y_pred)
→ [[TN, FP],   = [[85, 5],
   [FN, TP]]      [3,  7]]
```

| Term | Meaning |
|------|---------|
| TP (True Positive) | Predicted positive, actually positive — correct |
| TN (True Negative) | Predicted negative, actually negative — correct |
| FP (False Positive) | Predicted positive, actually negative — **wrong** (Type I error) |
| FN (False Negative) | Predicted negative, actually positive — **wrong** (Type II error) |

### What is "Positive"?

The **positive class** is whichever outcome you are most interested in detecting:

- Fraud detection: Positive = Fraud
- Disease screening: Positive = Disease
- Spam filter: Positive = Spam
- Pass/Fail: Positive = Fail (if that's the risk you're managing)

This is a choice you make. The labels 0 and 1 in your data define it — class 1 is typically positive.

### Example — Fraud Detection

100 transactions: 10 actual fraud, 90 legitimate.

```
Model predicts:
  - 7 fraud correctly    → TP = 7
  - 3 fraud missed       → FN = 3
  - 5 legitimate flagged → FP = 5
  - 85 legitimate OK     → TN = 85
```

Confusion matrix:

```
                Predicted Fraud  Predicted Legit
Actual Fraud  |       7         |       3        |
Actual Legit  |       5         |      85        |
```

In sklearn:

```python
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
```

---

## Precision

Of all predicted positives, how many were actually positive?

```
Precision = TP / (TP + FP)
```

Precision only looks at the **right column** (everything the model predicted positive):

```
                          Predicted Positive (column)
   Actually Negative   →        FP = 3
   Actually Positive   →        TP = 7
                                 ─────
                                 Total = 10

Precision = 7/10 = 70%  ← of those 10 flagged, how many were actually positive?
```

At 70% precision — **30% of flags were false alarms** — predicted positive but actually negative.

**Low precision = trigger-happy — too many false alarms:**
- Fraud detection: legitimate customers wrongly blocked
- Spam filter: real emails going to spam
- Cancer screening: healthy patients getting unnecessary treatment

**High precision = fewer false alarms.** Use when **false positives are costly**.

---

## Recall (Sensitivity)

Of all actual positives, how many did the model catch?

```
Recall = TP / (TP + FN)
```

Recall only looks at the **bottom row** (everything that was actually positive):

```
Actually Positive (row)
   → Predicted Negative: FN = 3
   → Predicted Positive: TP = 7
                         ─────
                         Total = 10

Recall = 7/10 = 70%  ← of those 10 real positives, how many did the model catch?
```

At 70% recall — **30% of real positives were missed**.

**Low recall = missing too many actual positives — dangerous when missing is costly:**
- Disease screening: patients sent home undiagnosed
- Fraud detection: fraud slipping through undetected
- Structural defects: defects missed before shipment

**High recall = fewer missed cases.** Use when **false negatives are costly**.

---

### Pattern to remember

```
Precision → right column (predicted positive)  → FP and TP  → false alarm rate
Recall    → bottom row    (actually positive)   → FN and TP  → miss rate

Precision  →  of what I flagged, how much was real?
Recall     →  of what was real, how much did I catch?
```

---

## When to Use Which

| | Actually Negative | Actually Positive |
|---|---|---|
| **Predicted Positive** | FP — minimise with Precision | TP — Correct ✓ |
| **Predicted Negative** | TN — Correct ✓ | FN — minimise with Recall |

---

## Precision vs Recall Trade-off

They pull in opposite directions. Adjusting the threshold changes both:

| Threshold | Precision | Recall | Effect |
|-----------|-----------|--------|--------|
| High (0.9) | High | Low | Cautious — only flag when very confident, miss more fraud |
| Low (0.1) | Low | High | Aggressive — flag everything suspicious, many false alarms |
| 0.5 | Balanced | Balanced | Default |

There is no free lunch — you have to decide which type of error is more acceptable for your problem.

---

## Specificity

Of all actual **Negatives**, how many did the model correctly identify?

```
Specificity = TN / (TN + FP)
```

```
Specificity = 85 / (85 + 5) = 85/90 = 0.944 = 94.4%
```

Specificity is recall for the negative class. Used mainly in medical contexts.

---

## F1 Score

When you want a single number that balances precision and recall, use F1.

F1 is the **harmonic mean** of precision and recall:

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

Using the fraud example:

```
Precision = 0.583,  Recall = 0.70

F1 = 2 × (0.583 × 0.70) / (0.583 + 0.70)
   = 2 × 0.408 / 1.283
   = 0.816 / 1.283
   = 0.636
```

### Why Harmonic Mean?

The harmonic mean punishes imbalance between precision and recall:

```
Precision = 1.0,  Recall = 0.0  →  F1 = 0.0   (useless despite perfect precision)
Precision = 0.5,  Recall = 0.5  →  F1 = 0.5   (both mediocre)
Precision = 0.9,  Recall = 0.9  →  F1 = 0.9   (both good)
```

A high F1 requires **both** precision and recall to be high.

---

## All Metrics from the Confusion Matrix

```
TP = 7,  FN = 3,  FP = 5,  TN = 85
Total = 100

Accuracy  = (TP + TN) / Total       = (7 + 85) / 100 = 92%
Precision = TP / (TP + FP)          = 7 / 12          = 58.3%
Recall    = TP / (TP + FN)          = 7 / 10           = 70%
Specificity = TN / (TN + FP)        = 85 / 90          = 94.4%
F1        = 2 × P × R / (P + R)     = 0.636
```

---

## Summary Table

| Metric | Formula | Question answered | When to use |
|--------|---------|-------------------|-------------|
| Accuracy | (TP+TN)/Total | Overall correct rate | Balanced classes |
| Precision | TP/(TP+FP) | Of predicted positives, how many real? | FP are costly |
| Recall | TP/(TP+FN) | Of actual positives, how many caught? | FN are costly |
| Specificity | TN/(TN+FP) | Of actual negatives, how many correct? | Medical tests |
| F1 | 2PR/(P+R) | Balance of precision and recall | Imbalanced classes |

---

## sklearn Functions

```python
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

print(accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(precision_score(y_test, y_pred))
print(recall_score(y_test, y_pred))
print(f1_score(y_test, y_pred))

# All at once:
print(classification_report(y_test, y_pred))
```

`classification_report` is the most convenient — it prints precision, recall, F1, and support for each class in one call.
