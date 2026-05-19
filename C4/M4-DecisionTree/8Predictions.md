# Making Predictions with a Trained Tree

A new data point travels **down the tree** following the rules at each node until it lands at a leaf. The leaf's stored value is the prediction.

```
new_point = {BP: 130, Age: 45, Sex: Male}

Root (BP > 120?)   → Yes → go left
Internal (Age > 50?) → No → go right
Leaf → predict "Disease"
```

---

## Classification Trees

At a leaf, the prediction is based on the **training points that landed there**.

### Majority Vote (default)

The most common class in the leaf becomes the prediction:

```
Leaf has 12 training points:
   9 Yes,  3 No
   → predict "Yes"
```

### Class Probabilities

Each leaf can also output **probabilities** — proportion of each class:

```
Leaf has 7 Yes, 3 No
   P(Yes) = 7/10 = 0.70
   P(No)  = 3/10 = 0.30
```

In sklearn:

```python
model.predict(X_test)         # class labels
model.predict_proba(X_test)   # probability per class
```

### Threshold

For binary, threshold defaults to **0.5** — same idea as Logistic Regression. You can adjust it for imbalanced problems:

```python
y_prob = model.predict_proba(X_test)[:, 1]
y_pred = (y_prob >= 0.3).astype(int)   # lowered threshold
```

For multiclass, the predicted label is whichever class has the highest probability.

---

## Regression Trees

Leaves contain **numerical values**, so the prediction is a single number — typically the **mean** of the training targets that landed there.

```
Leaf has 5 training points with y values:
   {10, 12, 9, 11, 8}

Mean = 10
→ all new points landing here are predicted 10
```

Why mean? It minimises the sum of squared errors within the leaf — consistent with the variance-reduction criterion used during training.

### Median as Alternative

If the targets are skewed or have outliers, **median** is more robust:

```
Leaf values: {5, 6, 7, 100}

Mean = 29.5  ← misleading
Median = 6.5 ← much more reasonable
```

Median minimises the sum of absolute errors. Used when `criterion='absolute_error'`.

---

## Piecewise-Constant Predictions

Trees produce **flat predictions inside each region** — one value per leaf:

```
Regression tree on 1D data:

  y
  │       _____
  │      |     |
  │ _____|     |___
  │|              |____
  │
  └─────────────────── x
```

This is the **piecewise-constant** nature of trees. Trees can't extrapolate or interpolate smoothly — they predict the same value everywhere within a region.

This is why trees can't capture continuous trends as smoothly as linear models — and why deeper trees are needed to approximate fine details (which leads to overfitting).

---

## Summary

```
Classification leaf  → majority class (or class probabilities)
Regression leaf      → mean (or median) of training values
Prediction process   → traverse root → leaf using node rules
Output               → constant within each leaf's region
```
