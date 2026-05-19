# Outliers in K-Means

K-Means is **highly sensitive to outliers**. Centroids are averages — and a single extreme point can drag a centroid toward it, distorting the entire cluster.

```
Cluster of 9 normal points + 1 outlier:

  .   .  .                     The mean (centroid) gets pulled
  .  .  .         OUTLIER  →   away from the dense cluster
  .   .                        toward the outlier

  centroid here ←--- not here  (where the real cluster is)
```

---

## Why It Happens

The centroid is the **mean** of all assigned points. The mean is heavily influenced by extreme values:

```
Cluster points (1D): [10, 11, 12, 13, 14]
Mean = 12 ✓

Add an outlier:      [10, 11, 12, 13, 14, 100]
Mean = 26.7   ← shifted massively by one outlier
```

That outlier pulled the centroid from 12 → 26.7. The centroid is now in "no man's land", far from any of the original cluster's points.

---

## Effects

```
✗ Centroid is in the wrong place
✗ Points may get assigned to the wrong cluster
✗ Cluster size and shape get distorted
✗ WCSS becomes misleading (high WCSS because of the outlier, not the cluster)
✗ Silhouette score drops
```

---

## How to Handle Outliers

### 1. Remove them

If the outliers are clearly errors or rare events you don't care about, just drop them:

```python
from scipy import stats

z_scores = np.abs(stats.zscore(X))
X_clean = X[(z_scores < 3).all(axis=1)]   # keep rows where all features are within 3 std devs
```

Or use IQR-based filtering:

```python
Q1, Q3 = X.quantile(0.25), X.quantile(0.75)
IQR = Q3 - Q1
mask = ((X > (Q1 - 1.5 * IQR)) & (X < (Q3 + 1.5 * IQR))).all(axis=1)
X_clean = X[mask]
```

### 2. Transform the data

Log-scale or square-root features that have heavy tails:

```python
X['income_log'] = np.log1p(X['income'])
```

This compresses extreme values without dropping them — useful when outliers carry signal you want to keep.

### 3. Use a different algorithm

Some clustering methods are **robust to outliers**:

- **DBSCAN** — outliers naturally form a "noise" cluster
- **K-Medoids** — uses medians instead of means, more robust
- **Hierarchical clustering** — outliers form their own singleton clusters

If outliers are inherent to your data and you can't remove them, consider switching.

### 4. Detect and isolate first

Detect outliers with isolation forest or one-class SVM, then cluster the rest:

```python
from sklearn.ensemble import IsolationForest

iso = IsolationForest(contamination=0.05, random_state=42)
outlier_mask = iso.fit_predict(X) == 1
X_clean = X[outlier_mask]
```

---

## Concrete Example

Imagine clustering customers by spending:

```
Cluster 1: low spenders, mean = $100
Cluster 2: medium spenders, mean = $500

Now add one ultra-high-spending corporate buyer: $50,000

Without scaling/outlier handling:
   Cluster 1 mean ≈ $200 (pulled up by some pull from outlier)
   Cluster 2 mean ≈ $5,500 (heavily distorted)
   → real low/medium split is lost
```

After removing the outlier:

```
Cluster 1: $100  ← back to true center
Cluster 2: $500
```

The clusters become meaningful again.

---

## Why This Matters Beyond K-Means

The centroid sensitivity comes from using the **mean**. Any algorithm based on means has this issue:

- K-Means (means → outliers shift centroids)
- Linear regression (least squares → outliers shift the line)
- Mean as a summary statistic (vs median, which is robust)

For robustness, replace mean with **median** wherever possible. K-Medoids does exactly that — it's the median version of K-Means.

---

## Summary

```
K-Means uses means → outliers drag centroids → bad clusters

How to handle:
   1. Remove outliers (z-score, IQR)
   2. Transform features (log, sqrt)
   3. Use robust algorithms (DBSCAN, K-Medoids)
   4. Detect and isolate before clustering
```

> Always check for outliers BEFORE running K-Means. A single extreme point can ruin everything.
