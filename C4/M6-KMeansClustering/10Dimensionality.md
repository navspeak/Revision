# High Dimensionality — The Curse

K-Means relies on **distance** to assign points to clusters. As the number of features grows, distance becomes **less and less informative**.

This is the **curse of dimensionality**.

---

## What Happens in High Dimensions

In 2D, you can clearly see clusters. In 1000D... not so much.

### Distance becomes uniform

```
In 2D space:
   Point distances range: 0.5 to 10   → 20× variation, useful

In 100D space:
   Point distances range: 14.2 to 14.6  → 1.03× variation, useless
```

As dimensions increase, **distances between points become nearly equal**. The "nearest" and "farthest" points are almost the same distance away.

### Why?

For a vector with d features each drawn from the same distribution:

```
Total distance² = sum of d squared differences
                 = d × (average squared difference per dimension)
```

As d grows, the random variation in each dimension **averages out**. All distances tend toward the same value.

Result: K-Means has no way to discriminate. Every point is roughly equidistant from every centroid.

---

## Symptoms in K-Means

```
✗ Silhouette score collapses toward 0
✗ Clusters look "indecisive" — many points equidistant from multiple centroids
✗ WCSS is high regardless of K
✗ Results unstable — different runs find different clusters
✗ Compute time grows linearly in d
```

---

## Solutions

### 1. Dimensionality Reduction

Reduce features before clustering. The most common technique: **PCA**.

```python
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Reduce 100D → 10D, keeping most of the variance
pca = PCA(n_components=10)
X_reduced = pca.fit_transform(X_scaled)

kmeans = KMeans(n_clusters=3, random_state=42).fit(X_reduced)
```

### How many components?

Choose enough to retain ~80–95% of variance:

```python
pca = PCA(n_components=0.90)   # keep 90% of variance
X_reduced = pca.fit_transform(X_scaled)
print('Components used:', pca.n_components_)
```

### 2. Feature Selection

Drop features that don't contribute. Use:

```
Correlation analysis    → remove highly correlated features
Variance threshold      → remove low-variance features (uninformative)
Domain knowledge        → drop features irrelevant to clustering
```

```python
from sklearn.feature_selection import VarianceThreshold
selector = VarianceThreshold(threshold=0.01)
X_reduced = selector.fit_transform(X)
```

### 3. Better Distance Metrics

In high dimensions, **cosine distance** can work better than Euclidean — it measures angle rather than magnitude:

```python
from sklearn.metrics.pairwise import cosine_distances
```

But this requires a different clustering algorithm — K-Means uses Euclidean by definition.

### 4. Use a Different Algorithm

Some methods handle high dimensions better:

```
DBSCAN              → density-based, sensitive to noise but handles dimensions OK
Spectral clustering → works with similarity matrices
Hierarchical        → cluster on cosine or correlation distance
```

---

## Compute Costs

Beyond the math, high dimensions are **slow**:

```
K-Means complexity ≈ O(n × K × d × iters)

n = data points
K = clusters
d = features         ← linear in d
```

Reducing d from 1000 to 10 → 100× speedup, plus better clusters.

---

## Workflow for High-Dimensional Data

```
1. Scale all features (StandardScaler)
2. Apply PCA to reduce dimensions:
      - keep enough to retain ~90% of variance
3. Run K-Means on the reduced data
4. Use original features only for interpretation, not clustering
```

---

## When NOT to Reduce

```
✓ Already low-dimensional (d < ~10) — don't bother
✓ All features are critical to interpretation
   → use feature engineering instead of brute-force reduction
```

---

## Summary

```
Curse of dimensionality:
   - distances become uniform → K-Means can't distinguish clusters
   - silhouette drops, results unstable

Solutions:
   1. PCA → reduce features while keeping variance
   2. Feature selection → drop irrelevant / low-variance features
   3. Cosine distance / different algorithm
   4. Compute cost: reducing d is also faster

Workflow: Scale → Reduce → Cluster
```

> If you have more than ~20 features, **start with PCA**. K-Means rarely works well in raw high-dimensional space.
