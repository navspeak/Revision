# Unsupervised Learning

Until now, every model has needed **labels** to learn:

```
Supervised:    X (features) + y (target) → model
Unsupervised:  X (features only)         → model finds structure
```

Unsupervised learning lets a machine **discover patterns in data without being told what to look for**.

---

## The Wandering-City Analogy

```
You arrive in a new city with no map.
You walk around and notice:
   - this neighbourhood looks residential
   - that area has restaurants and bars
   - over there, mostly offices

You've grouped the city into clusters — without anyone telling you the labels.
```

Unsupervised learning does the same with data. It explores, notices similarities, and forms natural groupings.

---

## Why It Matters

Many real-world problems have **no labels**:

```
You have 10,000 customers and want to find natural segments
   → no one has pre-labelled them — clustering finds groups

You have surveillance logs and want to spot anomalies
   → no one knows which are normal vs suspicious — unsupervised learning finds outliers

You have a million documents and want to organise them by topic
   → no topic labels — clustering / topic modelling reveals structure
```

In all these cases, **the structure is in the data — you just need an algorithm to expose it**.

---

## Supervised vs Unsupervised

| Aspect | Supervised | Unsupervised |
|--------|------------|--------------|
| Data | Labelled (X + y) | Unlabelled (X only) |
| Goal | Predict y for new X | Find hidden structure in X |
| Examples | Spam detection, price prediction | Customer segmentation, anomaly detection |
| Evaluation | Direct — compare predictions to true labels | Indirect — no ground truth |
| Typical metrics | Accuracy, R², F1 | Silhouette score, WCSS |

The big practical difference: with supervised learning you can **measure accuracy directly**. With unsupervised learning, since you don't have labels, **evaluation is judgement-heavy** — does the result make sense for the problem?

---

## Three Main Branches of Unsupervised Learning

### 1. Clustering

Group similar data points together.

```
Customer segmentation
Image segmentation
Document grouping
```

K-Means is the most popular example. **This module focuses on clustering.**

### 2. Dimensionality Reduction

Reduce the number of features while keeping the important information.

```
PCA (Principal Component Analysis)
t-SNE, UMAP
Autoencoders
```

Often used as a preprocessing step before clustering or visualisation.

### 3. Association Learning

Find rules and relationships between items.

```
"Customers who bought X also bought Y"  → recommendation systems
Market basket analysis
```

---

## Why It's Harder Than Supervised Learning

```
✗ No labels means no direct "right answer"
✗ Evaluation requires domain knowledge — "do these clusters mean anything?"
✗ Many algorithms — DBSCAN, K-Means, hierarchical, GMM — all give different results
✗ Choice of hyperparameters (like K) has no obvious correct value
✗ Sensitive to feature scaling, outliers, and data distribution
```

But despite these challenges, unsupervised learning is **essential for data exploration**. Often you don't know what patterns exist — clustering reveals them.

---

## Summary

```
Supervised   → "learn from examples"        (with labels)
Unsupervised → "discover patterns yourself" (no labels)

Clustering is the most common form of unsupervised learning.
K-Means is the most popular clustering algorithm.
```

> Next up: how K-Means actually works.
