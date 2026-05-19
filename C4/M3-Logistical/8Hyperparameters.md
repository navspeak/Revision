# Hyperparameters vs Parameters

Two completely different things that often get confused.

---

## Parameters

What the model **learns** from data during `fit()`:

```
Linear Regression:     β₀, β₁, β₂, ...        ← coefficients
Logistic Regression:   β₀, β₁, ... (log-odds)  ← coefficients
Decision Tree:         the splits at each node
Neural Network:        millions of weights
```

You don't set these — `fit()` finds them by minimising the cost function.

```python
model.coef_         # parameters (learned)
model.intercept_    # parameter   (learned)
```

---

## Hyperparameters

What **you** set **before** `fit()` is called — they shape how learning happens:

| Model | Hyperparameter | Role |
|-------|---------------|------|
| Ridge / Lasso | `alpha` (λ) | Regularisation strength |
| Logistic Regression | `C` (= 1/λ) | Inverse regularisation |
| Logistic Regression | `penalty` | l1, l2, elasticnet |
| Gradient Descent | learning rate α | Step size |
| Gradient Descent | `max_iter` | Iterations |
| Decision Tree | `max_depth` | Tree depth limit |
| KNN | `n_neighbors` | Number of neighbours |

```python
model = LogisticRegression(C=0.1, penalty='l1', max_iter=1000)
#                          ↑ hyperparameters — you choose these
```

---

## Why Hyperparameters Can't Be Learned

If they could, you'd just put them in `fit()`. The problem:

```
Training a model with C=0.001 vs C=100 gives different parameters β
But both models can fit training data well — just in different ways.
```

So you can't pick C by minimising training error — extreme C values may give 100% training accuracy but generalise poorly.

**Solution:** evaluate each candidate hyperparameter on **unseen data** — that's where cross-validation comes in.

---

## The Tuning Workflow

```
1. Define candidate values:  C ∈ {0.001, 0.01, 0.1, 1.0, 10, 100}
2. For each candidate:
       Run k-fold CV
       Average the validation scores
3. Pick the candidate with the best CV score
4. Train final model on full training set with that value
5. Evaluate once on held-out test set
```

In sklearn this is automated by `GridSearchCV`.

---

## Summary

| | Parameters | Hyperparameters |
|-|-----------|------------------|
| Who sets | The model (during `fit`) | You (before `fit`) |
| Example | β coefficients | `alpha`, `C`, `max_depth` |
| Found by | Optimisation (OLS / GD) | Trial — usually via CV |
| Tuning | Not applicable | `GridSearchCV`, `RandomSearchCV` |

> Parameters are **learned**. Hyperparameters are **chosen**.
