# K-Means Basics — Distance and Centroids

K-Means is the simplest, most popular clustering algorithm.

```
Divide data into K clusters.
Each cluster's centre = its CENTROID.
Points are assigned to the NEAREST centroid.
```

That's it conceptually. The whole algorithm is built on two ideas:

1. **Distance** — how to measure similarity
2. **Centroid** — what represents each cluster

---

## Distance as Similarity

K-Means uses **distance** to decide which points belong to which cluster. The shorter the distance, the more similar.

The default is **Euclidean distance** — straight-line distance between two points, like measuring with a ruler.

```
d(x, y) = √( Σ(xᵢ − yᵢ)² )    over all features i
```

### Example with 2 features

```
Point A: (3, 5)
Point B: (6, 9)

d(A, B) = √((6−3)² + (9−5)²)
        = √(9 + 16)
        = √25
        = 5
```

Two points 5 units apart. Whichever centroid is closest to A — A joins that cluster.

### Generalises to any dimension

```
3 features:  d = √((x₁−y₁)² + (x₂−y₂)² + (x₃−y₃)²)
n features:  d = √( Σᵢ₌₁ⁿ (xᵢ−yᵢ)² )
```

---

## Centroid — The Cluster Centre

A centroid is the **mean position** of all points in a cluster. For each feature, take the average across the points.

```
Cluster has 4 points:
   (2, 3)
   (4, 4)
   (3, 5)
   (5, 4)

Centroid = (mean of x, mean of y)
        = ((2+4+3+5)/4,  (3+4+5+4)/4)
        = (3.5, 4.0)
```

The centroid represents the **typical point** in the cluster. It's not necessarily a real data point — it's a synthetic centre.

---

## How They Work Together

The K-Means loop:

```
1. Assign each point to the nearest centroid (using Euclidean distance)
2. Move each centroid to the mean of its assigned points
3. Repeat
```

Each iteration:
- Distance tells the points where to go
- Centroids reposition themselves based on what arrived

The centroids slowly migrate until they sit at "natural" cluster centres in the data.

---

## Visual Intuition

```
Initial random centroids:        After convergence:

   .  .   *   .                    .  .   . 
  .  .  . .  .                    .  .  . .  .
  *  .  .  .                     *  .   .  .
   .  .  . *                       .  .  .   
   .  *  .                          .   .  
                                    *

  Centroids randomly placed       Centroids settle at cluster centres
```

---

## Why "K"-Means?

```
K = number of clusters (you choose this)
   K=2 → split data into 2 groups
   K=3 → 3 groups
   K=10 → 10 groups

Means = each cluster represented by the MEAN of its points (its centroid)
```

So "K-Means" literally translates to "K cluster centroids, each defined by the mean of its members".

---

## Limitations of the Centroid Idea

Since centroids are **averages**:

```
✗ They may not capture cluster SHAPE well (assumes spherical)
✗ Affected by outliers (mean shifts toward extreme values)
✗ Don't represent irregular or elongated clusters
```

These limitations show up in later sections (`7Outliers.md`, `12OtherClustering.md`).

---

## Summary

```
Distance     → Euclidean = straight-line distance through feature space
Centroid     → mean position of all points in a cluster
K            → number of clusters (you decide)

K-Means cycles:
   1. Assign points to nearest centroid
   2. Move centroids to the new means
   3. Repeat until stable
```

> Distance and centroid — those two ideas drive everything in K-Means.
