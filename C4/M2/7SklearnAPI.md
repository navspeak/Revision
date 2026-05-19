# sklearn API Pattern

Every supervised learning model in sklearn follows the same three-step pattern. Learn it once — it works for every model.

---

## The Pattern

```python
# Step 1 — Create the model
model = LinearRegression()

# Step 2 — Fit: learn from training data
model.fit(X_train, y_train)      # X = features, y = target

# Step 3 — Predict: apply to new data
y_pred = model.predict(X_test)   # returns array of predictions
```

---

## What Each Step Does

### fit(X, y)

This is where **learning happens**.

- Linear Regression → finds β₀, β₁ ... via OLS or gradient descent
- Decision Tree → builds the tree splits
- Logistic Regression → finds the decision boundary
- K-Means → finds cluster centres

After `fit()`, the model has learned everything it needs from the training data. It is now ready to make predictions.

### predict(X)

This is where **learned model is applied**. No more training — pure math.

- Takes new feature values (X)
- Returns predicted y values

> Rule: always `fit()` on training data, `predict()` on test data. Never fit on test data — that would leak future information into the model.

---

## Same Pattern Across All Models

```python
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans

# Every single one follows the same pattern:
model = AnyModel()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

The only thing that changes is what happens **inside** `fit()`. The API stays identical — swap any model in one line.

---

## The Full Flow

```
Raw data
    ↓
train_test_split(X, y, test_size=0.2, random_state=42)
    ↓
model.fit(X_train, y_train)       ← learning
    ↓
y_pred = model.predict(X_test)    ← prediction
    ↓
metrics(y_test, y_pred)           ← evaluation
```

---

## Metrics After Predict

### Regression

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error, r2_score
import numpy as np

mae   = mean_absolute_error(y_test, y_pred)
mse   = mean_squared_error(y_test, y_pred)
rmse  = np.sqrt(mean_squared_error(y_test, y_pred))
mape  = mean_absolute_percentage_error(y_test, y_pred) * 100
r2    = r2_score(y_test, y_pred)

n, p  = X_test.shape
adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
```

### Classification (later modules)

```python
from sklearn.metrics import accuracy_score, confusion_matrix
acc = accuracy_score(y_test, y_pred)
```

---

## predict([[5]]) — Why Double Brackets?

sklearn's `predict()` expects a **2D array** — rows × columns — because in general you pass multiple samples with multiple features.

```
model.predict([[5]])

[[5]]  →  1 row, 1 feature
 ↑ ↑
 │ └── 1 feature (e.g. Muffins = 5)
 └──── 1 sample (one prediction request)
```

Passing `[5]` (1D) would raise a warning or error — sklearn always expects shape `(n_samples, n_features)`.

### What it computes internally

```python
# model fit: Time = 10 + 2 × Muffins
model.predict([[5]])   →   10 + 2 × 5 = 20 mins
```

### Multiple predictions at once

```python
model.predict([[3],     # 3 muffins → 16 mins
               [5],     # 5 muffins → 20 mins
               [10]])   # 10 muffins → 30 mins
# → [16, 20, 30]
```

Each inner list = one sample. That's why it's always double brackets for a single prediction.

---

## Model-Specific Attributes After fit()

After `fit()`, the model stores what it learned. For Linear Regression:

```python
model.fit(X_train, y_train)

model.intercept_          # β₀
model.coef_               # [β₁, β₂, ...]

# Read as:
print(dict(zip(X.columns, model.coef_)))
```

---

## Summary

| Step | Method | What happens |
|------|--------|-------------|
| 1 | `model = AnyModel()` | Create model object with hyperparameters |
| 2 | `model.fit(X_train, y_train)` | Model learns from data |
| 3 | `model.predict(X_test)` | Model applies learning to new data |
| 4 | `metrics(y_test, y_pred)` | Measure how good the predictions are |

> The API is the same for every model. Only the algorithm inside `fit()` changes.
