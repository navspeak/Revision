# Bagging vs Boosting — Side by Side

Both combine many trees. But they take **opposite philosophies**.

```
Bagging:  parallel, independent learners → reduce VARIANCE
Boosting: sequential, dependent learners → reduce BIAS
```

---

## Core Comparison

| | Bagging | Boosting |
|-|---------|----------|
| Training | **Parallel** — trees are independent | **Sequential** — each tree depends on previous |
| Each tree sees | Different bootstrap sample of data | Errors / residuals of previous trees |
| Combine via | Vote (classification) or average (regression) | Weighted sum |
| Tree depth | **Deep** trees (full / unbounded) | **Shallow** trees (depth 3–8) |
| Each tree is | A strong learner (overfits alone) | A weak learner (slightly better than random) |
| Reduces | Variance (errors cancel by averaging) | Bias (errors corrected step by step) |
| Risk | Underfits if trees too shallow | Overfits if too many rounds / high learning rate |
| Tunability | Forgiving — defaults work | Needs careful tuning |
| Speed | **Fast** — parallelisable | **Slower** — sequential, can't parallelise core loop |
| Sensitive to noise | Robust — averaging dilutes noise | Sensitive — noise gets amplified each round |
| Canonical algorithm | Random Forest | Gradient Boosting (XGBoost, LightGBM) |

---

## Visual Comparison

### Bagging — Parallel

```
                  Training Data
                       |
        ┌──────┬──────┬──────┬──────┐
        ↓      ↓      ↓      ↓      ↓
     Sample  Sample Sample Sample Sample
       1       2     3      4      5
        ↓      ↓      ↓      ↓      ↓
     Tree 1  Tree 2 Tree 3 Tree 4 Tree 5
        \      |      |      |      /
         └─────┴──────┼──────┴─────┘
                      ↓
                  Vote / Average
                      ↓
                  Final Prediction
```

All trees train at the same time, see the same overall pattern, just on different samples.

### Boosting — Sequential

```
   Training Data
       ↓
    Tree 1 (baseline)
       ↓
    Residuals
       ↓
    Tree 2 (fixes Tree 1's errors)
       ↓
    Updated Residuals
       ↓
    Tree 3 (fixes Tree 1+2's errors)
       ↓
    ...
       ↓
    Weighted sum of all trees = Final Prediction
```

Each tree builds on the previous. Can't be trained in parallel — Tree N needs Tree N−1's output.

---

## Bias-Variance Decomposition

```
Total error = Bias² + Variance + Irreducible noise
```

```
Single deep tree:        low bias, HIGH variance
Bagging (RF):            low bias, low variance     ← variance reduced by averaging
                                                       (KEEPS deep trees)

Single shallow tree:     HIGH bias, low variance
Boosting (GBM):          low bias, low variance     ← bias reduced by sequential correction
                                                       (KEEPS shallow trees)
```

Both arrive at low bias AND low variance — but from opposite starting points.

---

## When to Use Which

### Choose Random Forest if:

```
✓ Quick baseline needed
✓ Want robustness without tuning
✓ Limited time for hyperparameter search
✓ Noisy data with outliers
✓ Want OOB error / feature importance with low effort
✓ Production needs predictable behaviour
```

### Choose Gradient Boosting if:

```
✓ Need maximum accuracy
✓ Have time to tune hyperparameters
✓ Data is reasonably clean
✓ Competing in a Kaggle competition (XGBoost / LightGBM usually wins)
✓ Production performance matters more than training time
```

---

## Common Workflow

In practice, **try both**:

```
1. Start with RandomForest as baseline (low effort)
2. Try GradientBoosting (XGBoost / LightGBM) with light tuning
3. Compare on held-out test set
4. Pick the winner (often boosting wins by 1-3% on accuracy)
5. If close — pick RF for robustness, boosting for raw accuracy
```

---

## Memorable One-Liners

```
"Many strong learners voting"   → Bagging
"Many weak learners cooperating" → Boosting

"Average out randomness"         → Bagging
"Hammer down errors"             → Boosting

"Variance buster"                → Bagging
"Bias buster"                    → Boosting
```

---

## Summary

```
Bagging  → parallel, deep trees, variance reduction, robust, easy
Boosting → sequential, shallow trees, bias reduction, accurate, needs tuning

Both share: tree-based, handle mixed data, no scaling needed,
            built-in feature importance, work great on tabular data.

Different mostly in: HOW they combine errors (cancel vs correct).
```

> Random Forest is the safer choice. Gradient Boosting is the higher-ceiling choice. Both belong in your toolbox.
