# Quiz — Logistic Regression + Linear Regression Regularisation

---

## Questions 1–3 — Logistic Regression (Breast Cancer)

### Task

- Load `load_breast_cancer()` from `sklearn.datasets`
- Target = `dataset.target` (0 = malignant, 1 = benign — binary classification)
- Fit `LogisticRegression()` with **default solver**
- 80:20 split, `random_state=9001`
- Scale features with `MinMaxScaler()`
- Report metrics via `classification_report()`

### Concepts being tested

| Concept | Where covered |
|---------|---------------|
| Binary classification with Logistic Regression | `1Classification.md`, `2LogisticRegression.md` |
| Default solver (`lbfgs`) | `2LogisticRegression.md` |
| Feature scaling — `MinMaxScaler` | `10Regularisation.md` (standardisation note) |
| Train/test split with fixed random_state | `9CrossValidation.md` |
| Classification metrics — accuracy, precision, recall | `4Metrics.md` |
| `classification_report` output | `4Metrics.md` |

### Code template

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=9001
)

scaler = MinMaxScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)        # transform only — no re-fit

model = LogisticRegression()                # default L2, C=1.0
model.fit(X_train_s, y_train)

y_pred = model.predict(X_test_s)
print(classification_report(y_test, y_pred))
```

### Watch-outs

- `fit_transform` on train, `transform` on test — never re-fit scaler on test
- Default `LogisticRegression()` already applies L2 regularisation (C=1.0)
- `classification_report` returns precision/recall/F1 **per class** plus accuracy

---

## Questions 4–5 — Linear Regression with Regularisation (Diabetes)

### Task

- Load `load_diabetes()` from `sklearn.datasets`
- Target = `dataset.target` (disease progression score — continuous)
- Fit three models:
  - Plain `LinearRegression()` (no regularisation)
  - `Lasso(alpha=1)` (L1)
  - `Ridge(alpha=1)` (L2)
- 80:20 split, `random_state=9001`
- Scale features with `MinMaxScaler()`
- Compute MSE for all three
- Inspect `.coef_` for each model

### Concepts being tested

| Concept | Where covered |
|---------|---------------|
| Linear Regression baseline | C4/M2 |
| L1 (Lasso) vs L2 (Ridge) | `10Regularisation.md` |
| Effect of `alpha` (= λ) | `10Regularisation.md` |
| MSE as regression metric | `12Scoring.md`, C4/M2 |
| Reading `.coef_` | `10Regularisation.md`, `6Coefficients.md` |
| Sparsity from Lasso (some β = 0) | `10Regularisation.md` — calculus view |

### Code template

```python
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import mean_squared_error
import pandas as pd

data = load_diabetes()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=9001
)

scaler = MinMaxScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

models = {
    'Linear (none)': LinearRegression(),
    'Lasso (L1)':    Lasso(alpha=1),
    'Ridge (L2)':    Ridge(alpha=1)
}

results = []
for name, model in models.items():
    model.fit(X_train_s, y_train)
    y_pred = model.predict(X_test_s)
    mse    = mean_squared_error(y_test, y_pred)
    nz     = (model.coef_ != 0).sum()
    results.append({'Model': name, 'MSE': round(mse, 2), 'Non-zero coefs': nz})

print(pd.DataFrame(results))

# Coefficient comparison
coefs = pd.DataFrame({
    name: m.coef_ for name, m in models.items()
})
print(coefs.round(2))
```

### What to expect

- **Lasso with alpha=1** is aggressive on this dataset — many coefficients will be exactly 0
- **Ridge with alpha=1** keeps all coefficients non-zero but shrunk
- **Plain LR** gives the largest coefficient magnitudes
- MSE comparison depends on how much overfitting plain LR was doing — sometimes regularised is worse on this small clean dataset

### Watch-outs

- `Lasso(alpha=1)` on a small dataset can zero almost everything — verify if results look odd
- `MinMaxScaler` scales to [0, 1] — different from `StandardScaler` which gives mean 0, std 1
- MSE is unaffected by feature scaling on the target side — but coefficient magnitudes change with feature scale

---

## Quick Reference — Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Re-fitting scaler on test set | `fit_transform(train)` + `transform(test)` |
| Forgetting `random_state` | Always set for reproducibility |
| Comparing coefficients without scaling | Always scale first |
| Using accuracy on imbalanced data | Use precision/recall/F1 |
| Tuning hyperparameters on test set | Use GridSearchCV on train only |

---

## Concept Recap

```
Binary classification → LogisticRegression
Continuous target     → LinearRegression / Ridge / Lasso

Default LogisticRegression() → L2 with C=1.0 (regularisation ON)
Default LinearRegression()   → no regularisation

alpha = λ in Ridge / Lasso
C = 1/λ in LogisticRegression  (inverted!)

MinMaxScaler → scales to [0, 1]
StandardScaler → mean=0, std=1
```
