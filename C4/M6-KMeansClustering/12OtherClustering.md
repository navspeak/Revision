# Other Clustering Methods

K-Means is the most popular but it's not always the right choice. Other methods handle situations where K-Means fails.

```
K-Means assumes:
   - Numerical data
   - Spherical clusters
   - Similar cluster sizes
   - No outliers

If any of these don't hold → use a different method.
```

---

## K-Modes — Categorical Data

Already covered in `11Categorical.md`. The categorical version of K-Means:

```
Mean         → Mode (most frequent category)
Euclidean    → Matching distance (count of differences)
```

For datasets entirely composed of categorical features.

---

## K-Prototypes — Mixed Data

Combines K-Means and K-Modes:

```
Numerical features  → mean, Euclidean distance
Categorical features → mode, matching distance
Combined            → weighted total distance
```

For datasets with both types of features.

---

## Hierarchical Clustering — Tree of Clusters

Builds a **tree** of clusters (called a **dendrogram**), allowing you to choose the level of granularity afterwards.

### Two approaches

```
Agglomerative (bottom-up):
   Start: each point is its own cluster
   Step:  merge the two closest clusters
   Stop:  one cluster contains everything
   → produces a tree showing merge history

Divisive (top-down):
   Start: all points in one cluster
   Step:  split the cluster that reduces variance most
   Stop:  each point in its own cluster
```

Agglomerative is the common one.

### Advantages

```
✓ No need to specify K in advance — cut the tree at any height
✓ Naturally handles irregular cluster shapes
✓ Produces a visual hierarchy (dendrogram)
✓ Works with any distance metric (Gower, cosine, etc.)
```

### Disadvantages

```
✗ Slow — O(n² log n) or worse → struggles on large datasets
✗ Hard to undo a merge once made (greedy)
```

```python
from sklearn.cluster import AgglomerativeClustering
agg = AgglomerativeClustering(n_clusters=3, linkage='ward')
labels = agg.fit_predict(X)
```

---

## DBSCAN — Density-Based

**DBSCAN** = Density-Based Spatial Clustering of Applications with Noise.

```
A cluster is a dense region of points.
A point is in a cluster if it has enough neighbours within a radius.
Points without enough neighbours = NOISE (no cluster assignment).
```

### Two key parameters

| | Meaning |
|-|---------|
| `eps` | Radius — neighbours within this distance count |
| `min_samples` | Minimum neighbours required to be a "core point" |

### What DBSCAN does well

```
✓ Finds clusters of ARBITRARY SHAPE (not just spherical)
✓ Identifies outliers naturally (as noise)
✓ Doesn't require specifying K
✓ Robust to outliers — they just become noise
```

### Disadvantages

```
✗ Sensitive to eps and min_samples
✗ Struggles when clusters have very different densities
✗ Doesn't work well in high dimensions
```

```python
from sklearn.cluster import DBSCAN
db = DBSCAN(eps=0.5, min_samples=5)
labels = db.fit_predict(X)
# Points with label -1 are noise (outliers)
```

When to use: irregular cluster shapes, want to detect outliers, K is unknown.

---

## Gaussian Mixture Models (GMM)

Assumes each cluster is a **Gaussian distribution** — a probabilistic generalisation of K-Means.

```
K-Means: hard assignment (point belongs to one cluster)
GMM:     soft assignment (point has a probability of being in each cluster)
```

Each cluster is described by:
- Mean (centre)
- Covariance (shape — can be elongated, rotated, etc.)
- Weight (how much of the data it represents)

### Advantages

```
✓ Captures ELLIPTICAL clusters (K-Means is spherical only)
✓ Soft assignment — uncertainty information about each point
✓ Can model overlapping clusters
```

### Disadvantages

```
✗ Slower to fit
✗ Sensitive to initialisation
✗ Number of components K still needs to be chosen
```

```python
from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=3, random_state=42)
gmm.fit(X)
labels = gmm.predict(X)
probs  = gmm.predict_proba(X)   # soft probabilities
```

---

## Fuzzy Clustering (Fuzzy C-Means)

Each point belongs to **multiple clusters** with **degrees of membership**.

```
Hard K-Means:  point is in exactly 1 cluster
Fuzzy:         point is 70% in cluster A, 30% in cluster B
```

Useful when:
- Clusters overlap genuinely
- Boundaries between groups aren't sharp
- You want to identify "borderline" points

Less common than other methods but powerful for fuzzy boundaries.

---

## Spectral Clustering

Uses **eigenvectors of a similarity matrix** to cluster:

```
1. Compute similarity matrix between all points
2. Compute the Laplacian and its eigenvectors
3. Cluster the eigenvectors using K-Means
```

### Strengths

```
✓ Captures complex, non-convex cluster shapes
✓ Works well when traditional methods fail (e.g. concentric circles)
```

### Weaknesses

```
✗ Computationally expensive (O(n³) in worst case)
✗ Need to choose a similarity measure carefully
```

---

## Decision Guide — Which Algorithm?

| Situation | Best choice |
|-----------|-------------|
| Standard numerical data, roughly spherical clusters | **K-Means** |
| Categorical features only | **K-Modes** |
| Mixed numerical + categorical | **K-Prototypes** |
| Irregular shapes, many outliers | **DBSCAN** |
| Don't know K, want hierarchy | **Hierarchical** |
| Elliptical / overlapping clusters | **GMM** |
| Fuzzy boundaries | **Fuzzy C-Means** |
| Complex non-convex shapes | **Spectral** |

---

## Summary

```
K-Means: the go-to default for clean numerical data with spherical clusters

When K-Means fails:
   Categorical data → K-Modes / K-Prototypes
   Irregular shapes → DBSCAN
   Don't know K     → Hierarchical
   Overlapping/elliptical → GMM
   Fuzzy boundaries → Fuzzy C-Means
   Non-convex shapes → Spectral

Clustering is a broad field — choose the right tool for your data.
```

> K-Means is the most common but not always the best. Match the algorithm to the data, not the other way around.
