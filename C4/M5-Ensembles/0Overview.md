# M5 — Ensembles

You've studied individual models — linear regression, logistic regression, decision trees. **Ensembles** combine multiple models into one prediction, achieving stronger performance than any single model alone.

```
Single model:    one perspective, prone to errors
Ensemble:        many perspectives, errors cancel out
```

The principle: **diverse models reinforce each other's strengths and cancel each other's weaknesses**.

---

## The Two Main Families

### Bagging (Bootstrap Aggregating)

```
Train many models in PARALLEL on different random samples of data.
Combine outputs (vote / average).

Reduces VARIANCE — stabilises unstable learners (like deep trees).

Canonical example: Random Forest
```

### Boosting

```
Train models SEQUENTIALLY — each new model corrects the previous one's errors.
Combine outputs (weighted sum).

Reduces BIAS — turns weak learners into a strong predictor.

Canonical example: Gradient Boosting (XGBoost, LightGBM, CatBoost)
```

---

## Why Ensembles Matter

Even in the age of deep learning, ensembles remain the **#1 choice for tabular data**:

```
✓ Highly accurate
✓ Robust to noise and outliers
✓ Handle mixed feature types
✓ No feature scaling needed
✓ Built-in feature importance
✓ Win the majority of Kaggle competitions on tabular problems
```

---

## Learning Objectives

By the end of this module you should be able to:

- Understand the motivation for using ensembles — why combining models outperforms a single learner
- Explain the mechanics of **bagging** and how random forests operate
- Describe the process of **boosting** and how gradient boosting sequentially improves predictions
- Compare the strengths and trade-offs between bagging and boosting
- Recognise how hyperparameters (number of trees, learning rate, tree depth) influence performance and complexity
- Appreciate why ensembles are among the most successful and widely used methods in modern ML

---

## Module Agenda

| # | Topic | Key Ideas |
|---|-------|-----------|
| 1 | Why Ensembles | Wisdom of crowds, bias-variance reduction |
| 2 | Bagging | Bootstrap sampling, parallel training, voting |
| 3 | Random Forest | Bagging + feature subsampling |
| 4 | Feature Importance | How RF ranks features, OOB error |
| 5 | Boosting | Sequential learning, weighted updates |
| 6 | Gradient Boosting | Residual fitting, learning rate |
| 7 | Bagging vs Boosting | Side-by-side comparison |
| 8 | Hyperparameters | n_estimators, max_depth, learning_rate |

---

## Files

| File | Content |
|------|---------|
| `1WhyEnsembles.md` | Motivation, panel-of-doctors analogy, bagging/boosting/stacking types |
| `2Bagging.md` | Bootstrap aggregating — weight-guessing analogy, variance reduction |
| `3RandomForest.md` | RF mechanics — bagging + random feature subsets, prediction examples |
| `4EvaluatingRF.md` | OOB error, feature importance, pros/cons, hyperparameters |
| `5Boosting.md` | Sequential learning — tutor analogy, AdaBoost vs Gradient Boost vs XGBoost |
| `6GradientBoosting.md` | GBM mechanics — residuals, learning rate, gradient interpretation |
| `7EvaluatingGBM.md` | Early stopping, pros/cons, hyperparameters, tuning strategy |
| `8BaggingVsBoosting.md` | Side-by-side comparison, when to use which |
| `9Applications.md` | Finance, healthcare, marketing, Kaggle reality |
| `11OtherEnsembles.md` | Stacking, AdaBoost, XGBoost, LightGBM, CatBoost |
| `Ensembles.ipynb` | Hands-on demo — single tree vs RF vs GBM (classification + regression) |
| `quiz.ipynb` | Practice — RF vs LightGBM on breast cancer with markdown explanations |
