# M6 — K-Means Clustering

So far you've studied **supervised** models — linear regression, logistic regression, decision trees, ensembles. Each needed labels (y) to learn.

**K-Means** is your first **unsupervised** algorithm. There are no labels. The model finds **natural groupings** in the data on its own.

```
Supervised   → input X + labels y → predict y for new data
Unsupervised → input X only → discover hidden structure
```

---

## Why Clustering?

```
Customer segmentation     → group similar buyers without prior categories
Image segmentation        → group pixels by colour
Anomaly detection         → find points that don't fit any cluster
Document grouping         → cluster articles by topic
Healthcare                → group patients by symptom patterns
```

The principle: **similar things tend to cluster together** — and unsupervised algorithms surface those clusters for us.

---

## What K-Means Does

```
K-Means partitions data into K clusters.

Each cluster has a CENTROID — its centre point.
Each data point is assigned to the NEAREST centroid.
Centroids are iteratively refined until clusters stabilise.
```

The result: K groups, each compact and well-separated from the others.

---

## Learning Objectives

By the end of this module you should be able to:

- Explain the motivation for clustering and why it's central to unsupervised learning
- Describe the mechanics of K-means — centroid updates, inertia, convergence
- Identify practical considerations: feature scaling, choice of K, outliers, high dimensionality
- Implement K-means in Python and interpret the resulting clusters
- Appreciate why clustering is one of the most widely used pattern-discovery methods

---

## Module Agenda

| # | Topic | Key ideas |
|---|-------|-----------|
| 1 | Unsupervised Learning | What it is, supervised vs unsupervised |
| 2 | K-Means Basics | Distance, centroids, similarity |
| 3 | Cluster Quality | WCSS / inertia, silhouette score, good vs bad |
| 4 | Algorithm | Step-by-step working process |
| 5 | Feature Scaling | Why distance-based methods need scaling |
| 6 | Choice of K | Elbow method, silhouette analysis |
| 7 | Outliers | Why they hurt, how to handle |
| 8 | Initialization | Random vs K-means++ |
| 9 | Stopping Criteria | When to terminate |
| 10 | Dimensionality | Curse of dimensions, PCA |
| 11 | Categorical Data | K-modes, K-prototypes |
| 12 | Other Clustering | DBSCAN, hierarchical, GMM, fuzzy |
| 13 | Applications | Marketing, healthcare, technology |

---

## Files

| File | Content |
|------|---------|
| `1Unsupervised.md` | Intro to unsupervised learning, supervised vs unsupervised |
| `2KMeansBasics.md` | Distance as similarity, centroids, cluster centres |
| `3ClusterQuality.md` | WCSS, inertia, silhouette, good vs bad clusters |
| `4Algorithm.md` | Working process step by step |
| `5Scaling.md` | Feature scaling — why and how |
| `6ChoiceOfK.md` | Elbow method, silhouette score, domain knowledge |
| `7Outliers.md` | Sensitivity to outliers, handling strategies |
| `8Initialization.md` | Random vs K-means++ |
| `9StoppingCriteria.md` | Convergence rules, max_iter |
| `10Dimensionality.md` | Curse of dimensionality, PCA |
| `11Categorical.md` | K-modes, K-prototypes |
| `12OtherClustering.md` | Hierarchical, DBSCAN, GMM, fuzzy |
| `13Applications.md` | Marketing, healthcare, tech, security |
| `KMeansClustering.ipynb` | Hands-on demo — synthetic + real data |
