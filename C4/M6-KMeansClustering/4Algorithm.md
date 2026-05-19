# K-Means Algorithm — Step by Step

The complete K-Means recipe:

```
1. Choose K (number of clusters)
2. Randomly initialise K centroids
3. Assign each point to its nearest centroid
4. Move each centroid to the mean of its assigned points
5. Repeat 3-4 until centroids stop moving
6. Evaluate cluster quality (WCSS / silhouette)
```

Two alternating steps form the **main loop**: **assignment** and **update**.

---

## The Loop — Visual

```
INITIALISE
   K centroids placed randomly in the feature space

REPEAT:
   ASSIGN STEP:
      For each data point:
         compute distance to each centroid
         assign to nearest centroid → forms a cluster

   UPDATE STEP:
      For each centroid:
         move to the mean of its newly-assigned points

UNTIL:
   centroids stop moving significantly
   OR maximum iterations reached
```

---

## Concrete Walkthrough

Tiny dataset, K = 2:

```
6 data points in 2D:

    (1, 1)   (2, 1)   (1, 2)
                                    (8, 8)   (9, 8)   (8, 9)
```

### Step 1 — Initialise (random)

```
Centroid 1: (3, 3)     ← randomly placed
Centroid 2: (7, 7)
```

### Step 2 — Assign each point

Compute distance from each point to each centroid:

```
Point (1,1):  d(C1) = √8 ≈ 2.83,  d(C2) = √72 ≈ 8.49  → joins C1
Point (2,1):  d(C1) = √5 ≈ 2.24,  d(C2) = √61 ≈ 7.81  → joins C1
Point (1,2):  d(C1) = √5 ≈ 2.24,  d(C2) = √61 ≈ 7.81  → joins C1
Point (8,8):  d(C1) = √50 ≈ 7.07, d(C2) = √2 ≈ 1.41   → joins C2
Point (9,8):  d(C1) = √61 ≈ 7.81, d(C2) = √5 ≈ 2.24   → joins C2
Point (8,9):  d(C1) = √61 ≈ 7.81, d(C2) = √5 ≈ 2.24   → joins C2

Cluster 1: {(1,1), (2,1), (1,2)}
Cluster 2: {(8,8), (9,8), (8,9)}
```

### Step 3 — Update centroids

```
New Centroid 1 = mean of C1 points
              = ((1+2+1)/3, (1+1+2)/3)
              = (1.33, 1.33)

New Centroid 2 = mean of C2 points
              = ((8+9+8)/3, (8+8+9)/3)
              = (8.33, 8.33)
```

The centroids moved from (3,3) and (7,7) to (1.33, 1.33) and (8.33, 8.33) — closer to their actual cluster centres.

### Step 4 — Repeat

Try the assign step again. The same points are still nearest to the same (new) centroids, so the assignments don't change. **Convergence reached**.

### Step 5 — Evaluate

```
WCSS for this clustering:
  Σ all squared distances from each point to its centroid
  ≈ small value (since points are tight around centroids)
```

Looks like a great clustering.

---

## Why It Converges

Each iteration **either decreases or keeps the same** the total WCSS:

```
Assign step:  each point goes to its NEAREST centroid → WCSS can only decrease
Update step:  each centroid moves to the MEAN of its cluster → WCSS minimised for that assignment
```

Since WCSS can't decrease forever, the loop eventually stops.

⚠️ But: K-Means may converge to a **local minimum**, not the global one. The result depends on initialisation — see `8Initialization.md`.

---

## sklearn API

```python
from sklearn.cluster import KMeans

kmeans = KMeans(
    n_clusters=3,            # K
    init='k-means++',        # smart initialisation (default)
    n_init=10,               # try 10 different inits, keep the best
    max_iter=300,            # cap on iterations
    tol=1e-4,                # tolerance for convergence
    random_state=42
)

kmeans.fit(X)

kmeans.labels_              # cluster assignment for each point
kmeans.cluster_centers_     # final centroid positions
kmeans.inertia_             # final WCSS
kmeans.n_iter_              # number of iterations until convergence
```

Predict a new point:

```python
kmeans.predict(new_data)    # assigns to nearest existing centroid
```

---

## Key Decisions Before Running

| Decision | Discussed in |
|----------|--------------|
| Choosing K | `6ChoiceOfK.md` |
| Scaling features | `5Scaling.md` |
| Handling outliers | `7Outliers.md` |
| Initialization method | `8Initialization.md` |
| Stopping criteria | `9StoppingCriteria.md` |

---

## Summary

```
The algorithm = two-step loop:
   Assign points → nearest centroid
   Update centroids → mean of their points
   Repeat until stable

Convergence: WCSS can only decrease → loop terminates
Risk: local minimum → multiple inits with K-means++
```

> The math is simple. Almost all the practical challenges come from making the right preprocessing and parameter choices around it.
