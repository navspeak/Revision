# Why Ensembles?

No single model is perfect. Each algorithm has its strengths and weaknesses — some capture patterns well but overfit noise, others are stable but miss fine details.

> **Ensemble methods combine many models** to get predictions that are more accurate and robust than any single model.

---

## The Panel-of-Doctors Analogy

```
One doctor's diagnosis    →  one perspective, may be wrong
Panel of doctors          →  combined views average out individual mistakes
```

A second opinion catches errors. A panel of opinions gives you a reliable diagnosis.

That's exactly the ensemble idea — combine multiple **base learners** to produce a better final prediction.

---

## Why Ensembles Beat Single Models

Each individual model makes some errors. But if the models are **diverse enough**, their errors don't all happen at the same data points — so when you combine them, errors **cancel out**.

```
Tree 1: gets points A, B wrong
Tree 2: gets points B, C wrong
Tree 3: gets points D, E wrong

Combined vote: most points are correct → only B might still be wrong
```

For this to work:
- Individual models must be **accurate enough** (better than random)
- Individual models must be **diverse** (make different mistakes)

If all models are identical, ensembling gives you nothing.

---

## Three Main Types of Ensemble Methods

### Bagging (Bootstrap Aggregating)

```
Train models in PARALLEL on different random samples
Combine outputs (average or vote)

Reduces VARIANCE — stabilises unstable learners
Examples: Random Forest, Bagged kNN
```

### Boosting

```
Train models SEQUENTIALLY — each new one corrects previous mistakes
Combine outputs (weighted sum)

Reduces BIAS — turns weak learners into a strong one
Examples: AdaBoost, Gradient Boosting, XGBoost, LightGBM
```

### Stacking (Stacked Generalisation)

```
Train DIFFERENT types of models (logistic, SVM, neural net, etc.)
Use ANOTHER MODEL to combine their predictions

The "meta-model" learns when to trust each base learner
Less common, harder to tune
```

This module focuses on **bagging and boosting** — the two most widely used.

---

## Why Decision Trees Are the Common Base Model

Trees are popular as base learners in ensembles because:

- **Flexible** — capture non-linear relationships
- **Non-parametric** — no distribution assumptions
- **Handle mixed feature types** natively
- **Robust to outliers** and missing values
- **Quick to train** in modern implementations

Their main weaknesses — instability and overfitting — actually **become strengths** when many trees are combined. Each tree is "unstable in a different way", and averaging cancels out that instability.

> Trees + ensembles = the most effective combination for tabular data.

---

## Where Ensembles Are Used

```
Spam detection
Fraud analysis
Credit scoring
Disease classification
Recommendation systems
Stock trend prediction
Kaggle competition winners (most of them)
```

Even with deep learning's rise, **ensembles still dominate tabular ML** — they're the go-to choice for most structured-data problems.

---

## Summary

```
Single model       → may overfit OR may miss patterns
Ensemble           → combine many → cancel errors → robust prediction

Bagging   → parallel, reduces variance        (Random Forest)
Boosting  → sequential, reduces bias          (Gradient Boosting)
Stacking  → different models + meta-learner   (advanced)
```

> The principle: many "okay" models beat one "great" model — especially when the okay models are diverse.
