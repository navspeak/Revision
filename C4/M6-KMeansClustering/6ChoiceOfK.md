# Choosing K — How Many Clusters?

K is the number of clusters you ask K-Means to find. **You have to choose it.** It's not learned from data.

Pick K too small → distinct groups get merged.
Pick K too large → real groups get split.

Two main techniques to guide your choice:

```
Elbow method          → uses WCSS / inertia
Silhouette analysis   → uses silhouette score
```

And **domain knowledge** — sometimes the business problem dictates K.

---

## The Elbow Method

Plot WCSS against different K values:

```
WCSS
  │\
  │ \
  │  \
  │   \____           ← elbow
  │       \____
  │            \____
  │                 \____
  │_____________________________ K
    1   2   3   4   5   6   7
```

- For very small K → high WCSS (clusters too big)
- As K increases → WCSS drops rapidly (clusters become tighter)
- At some point → drop **slows down** sharply — this is the **elbow**
- Beyond the elbow → adding clusters gives diminishing returns

Pick the K at the elbow.

### Why the elbow point?

```
Before the elbow: each new cluster genuinely captures structure → big WCSS reduction
After the elbow:  new clusters just slice already-tight groups → small WCSS reduction
```

The elbow is where "real" splits stop happening.

---

## Computing the Elbow Plot

```python
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_scaled)
    inertias.append(kmeans.inertia_)

plt.plot(range(1, 11), inertias, 'o-')
plt.xlabel('Number of clusters K')
plt.ylabel('WCSS (inertia)')
plt.title('Elbow method')
plt.show()
```

Inspect visually — the elbow is often around 3–6 for typical real-world data.

### Caveat

Sometimes the curve is smooth — no clear elbow. In that case use silhouette score instead, or rely on domain knowledge.

---

## Silhouette Analysis

Compute silhouette score for each candidate K, pick the highest:

```python
from sklearn.metrics import silhouette_score

scores = []
for k in range(2, 11):                # K must be at least 2
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_scaled)
    score = silhouette_score(X_scaled, kmeans.labels_)
    scores.append(score)
    print(f'K={k}: silhouette = {score:.3f}')

best_k = 2 + scores.index(max(scores))
print(f'Best K: {best_k}')
```

```
K=2: silhouette = 0.55
K=3: silhouette = 0.62   ← highest
K=4: silhouette = 0.48
K=5: silhouette = 0.42

→ best K = 3
```

### Why silhouette can give a different answer than elbow

```
Elbow method:        finds where compactness gains plateau
Silhouette score:    measures BOTH compactness AND separation
```

The elbow says "K=4 is enough". Silhouette might prefer K=3 if K=4 splits a cluster the algorithm can't separate cleanly.

When they disagree, **trust silhouette more** for cluster quality — it measures separation, which elbow doesn't.

---

## Domain Knowledge — The Real Tiebreaker

Sometimes the math suggests one answer and the business needs another. **Domain wins**.

```
Data-driven K:    K = 4 (math says so)
Business asks:    "We have 3 marketing tiers — give us 3 segments"
   → Use K = 3

Data-driven K:    K = 2
Business asks:    "We need to segment 10,000 customers into tiers we can act on"
   → Use K = 5 or 6 (even if silhouette is slightly worse)
```

K-Means is a tool. Cluster quality matters, but **so does usability of the result**.

---

## Combining Both Methods

The practical workflow:

```
1. Plot the elbow curve for K = 1 to 10
2. Identify the elbow region (often a range, not a single point)
3. Compute silhouette scores for that range
4. Pick the K with highest silhouette
5. Sanity-check against business needs
```

---

## Other Methods

For completeness:

- **Gap statistic** — compares WCSS to that of random data
- **Davies-Bouldin index** — ratio of within-cluster to between-cluster variance (lower is better)
- **Calinski-Harabasz index** — ratio of between to within variance (higher is better)

These are alternatives but elbow + silhouette covers 90% of practical cases.

---

## Summary

```
Elbow method      → plot WCSS vs K → find where curve flattens
Silhouette score  → plot silhouette vs K → pick highest
Domain knowledge  → align K with business reality

Rule of thumb:
   Use elbow to narrow down the range
   Use silhouette to pick the best
   Use domain knowledge to validate
```

> No "correct" K exists — only choices that work for the problem.
