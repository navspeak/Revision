# Initialization — Where to Place the First Centroids

K-Means starts by placing K centroids in the feature space. Where you place them **dramatically affects the final clusters**.

```
Random initialisation:  centroids placed randomly → may converge to a local minimum
K-means++:              centroids spread apart   → much better starting position
```

---

## The Problem with Random Initialisation

K-Means converges to a local minimum — not necessarily the global one. The local minimum it lands at depends on where the centroids started.

```
Same data, different random starts → different final clusters
```

### Example

Two well-separated true clusters in 2D:

```
With random init A:                   With random init B:
   ●●●           ▲▲▲                     ●●●           ●●●
   ●●●           ▲▲▲                     ●●●           ▲▲▲
   ●●●           ▲▲▲                     ▲▲▲           ▲▲▲

   Correct clustering found              Stuck in local minimum —
                                         centroids split each true cluster
                                         instead of separating them
```

Bad luck on initial placement = bad clusters.

---

## The Fix — K-means++

**K-means++** is a smart initialisation scheme. Instead of placing centroids randomly, it picks them **spread out across the data**.

### How K-means++ works

```
1. Pick the first centroid uniformly at random from the data points.

2. For each remaining data point x, compute D(x) =
   the distance from x to the NEAREST already-chosen centroid.

3. Pick the next centroid with probability ∝ D(x)²
   → far-away points are more likely to become centroids.

4. Repeat until K centroids are chosen.
```

This pushes centroids apart at the start, making them more likely to land in different clusters.

### Why it works

- Random init: centroids might all start in the same dense region → poor cluster discovery.
- K-means++: each new centroid biased toward unseen regions → trees catch the natural cluster structure.

K-means++ is **provably close to optimal** (proven by Arthur & Vassilvitskii, 2007).

### sklearn default

```python
KMeans(init='k-means++')   # default — almost always use this
KMeans(init='random')      # only if you want pure random init
```

---

## Multiple Initialisations — `n_init`

Even with K-means++, results can vary slightly. Sklearn runs K-Means **multiple times with different inits** and keeps the best (lowest WCSS):

```python
KMeans(n_init=10)   # try 10 different inits, keep the one with lowest WCSS
```

- Higher `n_init` → more reliable, but more compute
- Default in sklearn ≥ 1.4: `n_init='auto'` (10 with `k-means++`, 1 otherwise)

For production, set `n_init=10` or higher to be safe.

---

## Putting It Together

```python
from sklearn.cluster import KMeans

kmeans = KMeans(
    n_clusters=K,
    init='k-means++',     # smart init
    n_init=10,            # try 10 starts, keep best
    random_state=42       # reproducibility
)
```

This combination — K-means++ with multiple starts — is the standard practice. It minimises the risk of bad local minima.

---

## When to Worry About Initialization

Initialisation matters more when:

```
✗ K is large (more chances for a bad placement)
✗ Clusters are uneven in size or density
✗ Data is high-dimensional (centroids matter more)
```

It matters less when:

```
✓ K is small (2 or 3)
✓ Clusters are well-separated
✓ Data is well-behaved
```

In either case, **just use K-means++ with n_init=10**. It's free insurance.

---

## Reproducibility

To get the same clusters every run, fix `random_state`:

```python
kmeans = KMeans(n_clusters=3, random_state=42)
```

Without `random_state`, even K-means++ gives slightly different results each time (due to the random selection of the first centroid).

---

## Summary

```
Random init     → can land in local minima
K-means++       → spreads centroids out → much better starts
n_init=10       → try multiple starts, keep the best
random_state    → reproducibility

Defaults in sklearn:
   init='k-means++'   ✓
   n_init=10 (or 'auto')  ✓
   max_iter=300       ✓
```

> Just use `KMeans(n_clusters=K, random_state=42)` — sklearn's defaults handle init correctly.
