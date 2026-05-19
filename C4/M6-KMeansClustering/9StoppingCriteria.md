# Stopping Criteria

K-Means is iterative. When does it stop?

Three common conditions — the algorithm stops when **any one** is met:

```
1. Centroids stop moving significantly (convergence)
2. WCSS change falls below a threshold
3. Maximum iterations reached
```

---

## 1. Centroids Stop Moving — True Convergence

The natural stopping point. Once centroids settle:

```
Iteration 10: centroid moves from (3.1, 4.2) → (3.1, 4.2)    no change
Iteration 11: cluster assignments don't change → algorithm done
```

The clusters have stabilised. No more improvement possible.

In practice, "no change" is rare — usually we check if the change is **smaller than a tolerance**:

```
tolerance = 1e-4

if |new_centroid − old_centroid| < tolerance:
    stop
```

In sklearn this is the **`tol`** parameter:

```python
KMeans(tol=1e-4)   # default
```

---

## 2. WCSS Change Below Threshold

Equivalent to centroid stability — when WCSS barely improves anymore, the algorithm stops.

```
Iteration 8:   WCSS = 45.31
Iteration 9:   WCSS = 45.30   (change 0.01, very small)
Iteration 10:  WCSS = 45.30   → converged
```

When WCSS plateaus, further iterations waste compute.

---

## 3. Maximum Iterations — `max_iter`

A safety cap to prevent infinite (or very slow) loops:

```python
KMeans(max_iter=300)   # default in sklearn
```

If K-Means hasn't converged in 300 iterations, it stops anyway. The current cluster assignment becomes the result.

### When you might hit max_iter

```
✗ Tolerance set too tight
✗ Very high-dimensional data
✗ Pathological data (oscillating between configurations)
```

For most well-behaved data, K-Means converges in **10–50 iterations** — well below the default 300.

---

## Sklearn Parameters

```python
KMeans(
    n_clusters=K,
    tol=1e-4,         # convergence tolerance for centroid movement
    max_iter=300,     # hard cap on iterations
)
```

After fitting:

```python
kmeans.n_iter_       # how many iterations were actually used
```

If `n_iter_ == max_iter`, the algorithm hit the cap (didn't fully converge). You may want to investigate or increase `max_iter`.

---

## Visualising Convergence

WCSS over iterations typically looks like:

```
WCSS
  │\
  │ \____
  │      \____
  │           \___
  │               \___
  │                   \____
  │                        \____    ← plateau (converged)
  │                             \____
  └────────────────────────────────── iteration
```

Rapid early progress, then flat. The "flat" region is where the algorithm could safely stop.

---

## Why Stopping Matters

```
Too aggressive (tight tol, low max_iter):
   may stop too early → suboptimal clustering

Too lenient (loose tol, high max_iter):
   wastes compute on negligible improvements

Default values usually fine:
   tol=1e-4, max_iter=300 → balance of speed and quality
```

---

## Combined with Multiple Initialisations

Each run of K-Means (within `n_init`) has its own stopping behaviour:

```
n_init=10:
   Run 1 stops after 12 iterations (converged)
   Run 2 stops after 18 iterations
   ...
   Run 10 stops after 9 iterations

Sklearn keeps the run with the lowest final WCSS.
```

So if some runs converge fast and others slow, sklearn handles it — you don't have to manage stopping per-run.

---

## Summary

```
K-Means stops when ANY of:
   1. Centroids barely move (|change| < tol)        ← typical
   2. WCSS barely changes                            ← equivalent
   3. max_iter reached                               ← safety cap

Defaults in sklearn:
   tol=1e-4         → reasonable convergence threshold
   max_iter=300     → almost never reached in practice
```

> Stopping criteria rarely need tuning. Sklearn defaults handle them — only worry if `n_iter_ == max_iter` after fitting.
