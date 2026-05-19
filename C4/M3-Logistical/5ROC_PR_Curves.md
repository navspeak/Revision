# ROC Curve and Precision-Recall Curve

Both curves show model performance **across all thresholds** — not just at 0.5.

---

## Precision-Recall (P-R) Curve

Plot Precision vs Recall as you sweep the threshold from 1 → 0:

```
Precision
  1.0 |*
      | \
  0.8 |  \
      |   \___
  0.6 |       \___
      |           \___
  0.4 |_______________\___
                          Recall
      0.4  0.6  0.8  1.0
```

- High threshold → high precision, low recall (cautious)
- Low threshold → low precision, high recall (aggressive)
- Moving right along the curve = lowering the threshold

### Area Under the P-R Curve

```
Ideal model:   area = 1.0   (precision stays 1.0 as recall increases to 1.0)
Random model:  area = proportion of positives in dataset
```

Higher area = better model at all operating points.

**Use P-R curve when:** classes are imbalanced (more negatives than positives) — e.g. fraud, disease detection.

---

## ROC Curve (Receiver Operating Characteristic)

Plot **True Positive Rate (Recall)** vs **False Positive Rate (1 − Specificity)**:

```
TPR = TP / (TP + FN)          ← Recall / Sensitivity
FPR = FP / (FP + TN)          ← 1 − Specificity
```

```
TPR (Recall)
  1.0 |          /‾‾‾‾‾
      |        /
  0.8 |      /
      |    /
  0.5 |  /  ← random model (diagonal)
      |/
  0.0 |__________________
      0.0  0.5  1.0
              FPR (1 − Specificity)
```

- A perfect model → curve goes straight up then right → area = 1.0
- A random model → diagonal line → area = 0.5
- Your model → somewhere above the diagonal → area between 0.5 and 1.0

### AUC (Area Under the ROC Curve)

```
AUC = 1.0   → perfect model
AUC = 0.9   → excellent
AUC = 0.7   → good
AUC = 0.5   → no better than random
AUC < 0.5   → worse than random (predictions are inverted)
```

AUC is **threshold-independent** — it measures overall discriminating ability regardless of where you set the threshold.

---

## P-R Curve vs ROC Curve

| | P-R Curve | ROC Curve |
|-|-----------|-----------|
| Axes | Precision vs Recall | TPR vs FPR |
| Best for | Imbalanced datasets | Balanced datasets |
| Ideal area | 1.0 | 1.0 |
| Random baseline | = positive class proportion | 0.5 (diagonal) |

---

## Why P-R Curve for Imbalanced Data (e.g. Fraud)

When frauds are rare — say 1% fraud, 99% legitimate:

### ROC hides the problem

ROC plots TPR vs FPR. With 99% negatives, FPR stays low even with many FP mistakes:

```
FPR = FP / (FP + TN)

Flag 100 legit as fraud (FP=100) out of 9900 legit (TN=9800):
FPR = 100 / 9900 = 1%   ← looks tiny on ROC
```

The large TN pool absorbs false positives — ROC looks great even when the model is poor at catching fraud.

### P-R curve exposes it

```
Precision = TP / (TP + FP)

Same 100 FP, only 5 TP caught:
Precision = 5 / (5 + 100) = 4.7%   ← immediately visible as poor
```

P-R curve drops sharply → area is low → model is exposed.

Random baseline on P-R = proportion of positives = 1% — your model must beat this. On ROC the random baseline is always 0.5 regardless of class balance.

---

## Rule of Thumb

```
Balanced classes    → ROC / AUC
Imbalanced classes  → P-R curve
Fraud, disease, rare events → always P-R curve
```

---

## sklearn

```python
from sklearn.metrics import (
    precision_recall_curve,
    roc_curve,
    roc_auc_score,
    auc
)

y_prob = model.predict_proba(X_test)[:, 1]   # P(class 1) — all rows, column 1

# P-R Curve
precision, recall, thresholds = precision_recall_curve(y_test, y_prob)
pr_auc = auc(recall, precision)              # no shortcut for PR-AUC, use auc()
print(f"PR-AUC: {pr_auc:.3f}")

# ROC Curve
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = roc_auc_score(y_test, y_prob)      # shortcut for ROC-AUC
print(f"ROC-AUC: {roc_auc:.3f}")

# roc_auc_score and auc(fpr, tpr) are equivalent:
roc_auc_manual = auc(fpr, tpr)               # same result
```

### auc() vs roc_auc_score

`auc` is a **generic** function — computes area under any curve given x and y arrays (trapezoidal integration). Use it whenever there is no dedicated shortcut.

| Function | Use |
|----------|-----|
| `roc_auc_score` | AUC for ROC curve — one line shortcut |
| `auc(fpr, tpr)` | Same, manual |
| `auc(recall, precision)` | AUC for P-R curve — no shortcut exists |
