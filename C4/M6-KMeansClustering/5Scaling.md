# Feature Scaling — Essential for K-Means

K-Means uses **Euclidean distance**. Distance is sensitive to feature scale — so features with larger numeric ranges will **dominate** the clustering.

> **Always scale features before applying K-Means.**

---

## The Problem in One Example

Customer segmentation with two features:

```
Feature 1: Annual income (in lakhs)    → range: 0 to 100
Feature 2: Satisfaction rating         → range: 1 to 5
```

A customer A with income = 50, rating = 4.
A customer B with income = 52, rating = 1.

```
Distance(A, B) = √((50−52)² + (4−1)²)
              = √(4 + 9)
              = √13 ≈ 3.6
```

Now compare to customer C with income = 95, rating = 4 (same rating as A):

```
Distance(A, C) = √((50−95)² + (4−4)²)
              = √(2025 + 0)
              = √2025 = 45
```

Income dominates **completely**. The rating feature is invisible to the algorithm.

Result: clusters are formed almost entirely on income — even though rating is supposed to matter equally.

---

## The Fix — Standardisation or Normalisation

Bring all features to a comparable scale.

### Standardisation (z-score)

```
Subtract the mean, divide by the standard deviation.

x_scaled = (x − μ) / σ

→ each feature has mean 0 and std 1
```

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

### Normalisation (Min-Max)

```
Scale all values to a fixed range, usually [0, 1].

x_scaled = (x − min) / (max − min)

→ each feature lies between 0 and 1
```

```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
```

---

## After Scaling — Same Example

Standardised income and rating both have mean 0, std 1:

```
Customer A: income_scaled ≈ -0.2, rating_scaled = +0.5
Customer B: income_scaled ≈ -0.1, rating_scaled = -1.5
Customer C: income_scaled ≈ +1.8, rating_scaled = +0.5

Distance(A, B) ≈ √(0.01 + 4.0) ≈ 2.0
Distance(A, C) ≈ √(4.0 + 0)   ≈ 2.0
```

Now both features contribute equally to the distance. The algorithm can see the rating, not just the income.

---

## Standardisation vs Normalisation — Which to Use?

| | StandardScaler | MinMaxScaler |
|-|----------------|--------------|
| Output | Mean 0, std 1 | Range [0, 1] |
| Affected by outliers? | Yes (mean and std are pulled by outliers) | Yes (max pulled by outliers) |
| Range | Unbounded (can be > 1 or < 0) | Bounded [0, 1] |
| Default for K-Means | **StandardScaler** (most common) | Works well for bounded features |

When in doubt, **use StandardScaler** for K-Means. It's the standard choice for distance-based methods.

---

## Workflow

```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 1. Scale first
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 2. Cluster on scaled data
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_scaled)
```

The original (unscaled) values stay in your dataframe for interpretation — but the algorithm operates on scaled values.

---

## Warning — Forgetting to Scale

Common bug:

```python
# Wrong — features dominate by their scale
kmeans.fit(X_unscaled)         # income (lakhs) dominates rating (1-5)

# Right
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans.fit(X_scaled)
```

If your clusters look weird or are dominated by a single feature — **check that you scaled**.

---

## Summary

```
K-Means uses Euclidean distance → scale-sensitive
Features on different scales → larger-scale features dominate

ALWAYS scale before K-Means:
   StandardScaler (mean 0, std 1)  → default
   MinMaxScaler   ([0, 1])         → alternative
```

> Scaling isn't optional for K-Means. It's not a "consideration" — it's a requirement.
