# Cluster Quality — WCSS and Silhouette

How do you know if your clusters are "good"? Two key metrics:

```
WCSS (Inertia)        → measures COMPACTNESS within clusters
Silhouette score      → measures SEPARATION between clusters
```

A good clustering has **both** — tight clusters that are well-separated.

---

## What Makes a "Good" Cluster?

```
Good cluster:                     Bad cluster:

  .    .    .   . . .              .  .       .
    .  *  .    . * .                .  .   .  *  .
   .   .  .   . . .                  .  *  .  .  
                                       .   .   .

Tight within, separated between    Loose within, mixed between
   ← well-defined groups               ← overlapping, unclear
```

Two distance-based goals:

| Distance type | Want it to be | Why |
|---------------|--------------|-----|
| **Intra-cluster** (within) | **Small** | Points in same cluster are similar |
| **Inter-cluster** (between) | **Large** | Different clusters are clearly distinct |

---

## WCSS / Inertia — Compactness

**WCSS** = Within-Cluster Sum of Squares. Also called **inertia**.

```
WCSS = Σ ‖C − xᵢ‖²
   over all points xᵢ in all clusters
   where C = centroid of the cluster xᵢ belongs to
```

For each point, compute the squared distance to its centroid. Add them all up.

### What it measures

```
Low WCSS  → points tight around their centroids → good
High WCSS → points spread out from centroids    → bad
```

### Worked example

```
Cluster 1: centroid = (3, 4), points = (2,4), (4,4), (3,5)
   distances² = 1, 1, 1 → sum = 3

Cluster 2: centroid = (8, 8), points = (7,9), (9,7)
   distances² = 2, 2 → sum = 4

WCSS = 3 + 4 = 7
```

In sklearn:

```python
kmeans.inertia_   # WCSS of the fitted model
```

### Limitation

WCSS always **decreases** as K increases (more clusters → smaller clusters → less variation within each). So you can't just "minimise WCSS" — you'd end up with K = N (each point its own cluster, WCSS = 0).

That's why we use the **elbow method** to find a balance — see `6ChoiceOfK.md`.

---

## Silhouette Score — Separation

The silhouette score measures how well a point fits its own cluster compared to other clusters.

For each point:

```
a = average distance to OTHER points in the SAME cluster      (cohesion)
b = average distance to points in the NEAREST OTHER cluster   (separation)

silhouette = (b − a) / max(a, b)
```

### Range

```
+1   →  point is far from neighbouring clusters, perfectly placed
 0   →  point is on the boundary between two clusters
-1   →  point is in the WRONG cluster (closer to a different one)
```

Overall silhouette score = average across all points.

### Reading silhouette values

```
> 0.7   →  strong clusters
0.5-0.7 →  reasonable clusters
0.25-0.5 →  weak / overlapping
< 0.25  →  no real structure
```

In sklearn:

```python
from sklearn.metrics import silhouette_score
score = silhouette_score(X, labels)
```

---

## WCSS vs Silhouette

| | WCSS / Inertia | Silhouette |
|-|---------------|------------|
| Measures | Compactness only | Compactness AND separation |
| Range | 0 to ∞ | −1 to +1 |
| Best | As low as possible (but always drops with K) | As high as possible |
| Direct interpretation | Squared distances summed | Quality score per point |
| Used for | Elbow method (find K) | Validating cluster quality |
| Cost to compute | Cheap | Slower (needs all pairwise distances) |

Use **both together**:
- WCSS to find a good K via the elbow plot
- Silhouette to validate that K really produces well-separated clusters

---

## Other Quality Indicators

| Aspect | Good clusters | Bad clusters |
|--------|--------------|--------------|
| Compactness | Low WCSS — tight around centroid | High WCSS — spread out |
| Separation | Far apart between clusters | Overlapping |
| Silhouette | Close to 1 | Near 0 or negative |
| Shape | Roughly spherical (for K-Means) | Elongated, irregular |
| Interpretability | Make sense in the domain | Hard to explain |

K-Means specifically assumes **spherical clusters** — if your data has elongated or irregular shapes, K-Means will give poor silhouette scores. In that case use DBSCAN or hierarchical clustering instead.

---

## Summary

```
WCSS / Inertia     → compactness within clusters (lower is better)
Silhouette score   → how well-separated points are (higher is better)

Good cluster = tight within, well-separated between
   - Low WCSS
   - High silhouette
   - Roughly spherical
   - Interpretable in domain
```

> Use WCSS to pick K, use silhouette to validate the final clustering.
