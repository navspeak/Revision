# Boosting

The other major ensemble family. The opposite philosophy from bagging.

```
Bagging   → Train models in PARALLEL, each on a different sample
Boosting  → Train models SEQUENTIALLY, each one fixing the previous ones' mistakes
```

The goal: turn a collection of **weak learners** (slightly better than random) into one **strong learner** (highly accurate).

---

## The Tutor Analogy

Imagine a student struggling with a subject:

```
Tutor 1: explains the basics → student understands most things but still fails on hard topics
Tutor 2: focuses on the topics where Tutor 1 failed → fixes specific gaps
Tutor 3: focuses on what Tutor 1 & 2 together still didn't cover → further refinement
...
```

Each tutor specialises in what the previous ones got wrong. By the end, the student has mastery — not because any one tutor was great, but because each one **targeted the gaps left by the others**.

That's boosting: each model corrects the previous models' errors.

---

## How Boosting Works — Big Picture

```
1. Train model 1 on the data → it makes some predictions, some wrong
2. Identify which data points were predicted poorly
3. Train model 2 to focus on those weak predictions
4. Combine model 1 + model 2
5. Identify remaining errors
6. Train model 3 to fix those
...
Continue for K rounds
Final prediction = weighted combination of all K models
```

Each new learner is trained on the **residuals** (errors) of the combined ensemble so far. The ensemble slowly corrects itself over many rounds.

---

## Reduces Bias, Not Variance

Recall:

```
Bagging:  reduces variance (stabilises unstable learners)
Boosting: reduces bias    (sharpens systematically wrong predictions)
```

This shapes the choice of base learner:

```
Bagging → deep, complex trees (high variance, low bias)
Boosting → shallow, weak trees (low variance, high bias)
```

A shallow tree alone is barely better than random — but boosted together, many shallow trees become highly accurate. This is why boosting **specifically uses weak learners**.

---

## A Simple Worked Idea

Imagine predicting house prices. Each tree predicts a value:

```
Truth for some point: $300,000

Model 1 (baseline)  predicts $250,000   →  residual = $50,000 too low
Model 2 trained on residuals predicts +$40,000 → ensemble now predicts $290,000
                                              →  residual = $10,000 too low
Model 3 trained on residuals predicts +$8,000  → ensemble predicts $298,000
                                              →  residual = $2,000 too low
Model 4 trained on residuals predicts +$1,500  → ensemble predicts $299,500
...
```

Each step shrinks the error. After enough models, the ensemble is very close to the true value.

This is exactly how **Gradient Boosting** works — covered next in `6GradientBoosting.md`.

---

## Boosting Variants

| Method | Year | What's different |
|--------|------|-----------------|
| AdaBoost | 1995 | Reweights data after each round — wrong points get more weight |
| Gradient Boosting | 2001 | Fits each new tree to **gradients of the loss function** (residuals for MSE) |
| XGBoost | 2014 | Optimised gradient boosting with regularisation, parallel tree building |
| LightGBM | 2016 | Microsoft — much faster, uses leaf-wise growth |
| CatBoost | 2017 | Yandex — native categorical handling |

These are all variants on the same sequential-correction idea. **Gradient Boosting** is the conceptual core; XGBoost / LightGBM / CatBoost are engineering refinements.

---

## Trade-offs vs Bagging

```
Boosting often achieves HIGHER accuracy than bagging
Boosting is MORE PRONE to overfitting (especially on noisy data)
Boosting is SLOWER (sequential, can't parallelise easily)
Boosting needs MORE careful tuning (learning rate, number of trees, depth)
```

The reason boosting can overfit is exactly **because** it keeps fixing residuals — eventually it starts fitting noise.

That's why boosting models always include:

- **Learning rate** (small step size per round)
- **Early stopping** (stop when validation error starts rising)
- **Regularisation** (L1/L2 penalties on tree weights in XGBoost)

---

## Summary

```
Boosting       = sequential ensemble where each model fixes previous errors
Reduces        → BIAS
Best when      → base model is weak (high-bias, low-variance, e.g. shallow tree)
Combine via    → weighted sum (not simple average)
Risk           → overfitting if too many rounds or learning rate too high
Examples       → AdaBoost, Gradient Boosting, XGBoost, LightGBM, CatBoost
```

> Boosting trades robustness for raw accuracy. Tuned carefully, it's often the highest-performing approach for tabular data.
