# Categorical Variables — K-Means Doesn't Like Them

K-Means is designed for **numerical data**. It computes means and uses Euclidean distances. Both operations **break down** for categorical features.

---

## Why K-Means Fails on Categoricals

### Means don't make sense

```
Feature: phone_brand ∈ {Android, Apple, Other}

Label encoding: Android=0, Apple=1, Other=2

5 customers with values: 0, 0, 1, 2, 1
Mean = (0+0+1+2+1) / 5 = 0.8

What does "0.8" mean? Between Android and Apple?
It's nonsense — categories aren't ordered.
```

The "mean" of categorical values has no real-world meaning.

### One-hot encoding doesn't fix it

```
One-hot:
   Android → [1, 0, 0]
   Apple   → [0, 1, 0]
   Other   → [0, 0, 1]

Mean of [1,0,0], [1,0,0], [0,1,0]:
   = [⅔, ⅓, 0]

What's [⅔, ⅓, 0]? Not any real category. The centroid is meaningless.
```

Worse — Euclidean distance over one-hot vectors gives equal distances between any pair of categories:

```
d(Android, Apple) = √(1+1) = √2
d(Android, Other) = √(1+1) = √2
d(Apple, Other)   = √(1+1) = √2
```

All categories look equally similar/different. K-Means can't extract useful structure.

---

## Alternatives — Use a Different Algorithm

When you have categorical features, K-Means is the wrong tool. Better options:

### K-Modes — Pure Categorical Clustering

Replaces:
- **Mean** → **Mode** (most frequent category)
- **Euclidean distance** → **Matching distance** (count of differing attributes)

```
Cluster with phone_brand values: [Android, Android, Apple, Android, Other]
Mode = Android   ← cluster centre

Matching distance:
   d(Android, Android) = 0
   d(Android, Apple)   = 1
   d(Android, Other)   = 1
```

Used when **all features are categorical**.

```python
# kmodes library (pip install kmodes)
from kmodes.kmodes import KModes

km = KModes(n_clusters=3, init='Cao', random_state=42)
km.fit(X_categorical)
```

### K-Prototypes — Mixed Data

Combines K-Means (for numeric) + K-Modes (for categorical):

```
Numerical features  → use mean and Euclidean distance
Categorical features → use mode and matching distance
Combine with a weight γ to balance their contributions
```

```python
from kmodes.kprototypes import KPrototypes

kp = KPrototypes(n_clusters=3, init='Cao', random_state=42)
kp.fit(X, categorical=[1, 3, 5])    # indices of categorical features
```

Useful when you have **both numeric and categorical** features (common in real data).

---

## Other Options for Categorical Clustering

### Frequency or target encoding (then K-Means)

Replace categorical values with statistics:

```
Frequency encoding:  category → its count in the dataset
Target encoding:     category → mean of some numerical target
```

This makes features numeric, allowing K-Means to run. But the encoded values may not capture the categorical structure well.

### Gower distance + Hierarchical clustering

**Gower distance** handles mixed types naturally — it computes per-feature distances and combines them.

```python
import gower
distance_matrix = gower.gower_matrix(X)

# Use the distance matrix with hierarchical clustering
from scipy.cluster.hierarchy import linkage, fcluster
Z = linkage(distance_matrix, method='average')
labels = fcluster(Z, t=3, criterion='maxclust')
```

This handles categorical features properly without forcing them into a numerical framework.

---

## Decision Guide

```
All features numerical              → K-Means (with scaling)
All features categorical            → K-Modes
Mixed features                      → K-Prototypes
Want maximum flexibility            → Hierarchical clustering with Gower distance
Categorical with order (ordinal)    → Can sometimes use K-Means after careful encoding
```

---

## Common Mistakes

### Forcing categorical into K-Means

```python
# Wrong — clustering on label-encoded categoricals
X['gender'] = X['gender'].map({'M': 0, 'F': 1})
KMeans().fit(X)           # treats 1 vs 0 as a meaningful distance
```

### Using one-hot in K-Means without justification

```python
# Marginal — one-hot can sometimes work, but inflates dimensionality
X = pd.get_dummies(X, columns=['city'])   # if city has 100 values → 100 new dimensions
KMeans().fit(X)
```

This works for low-cardinality categoricals (gender, yes/no) but is bad for high-cardinality (zip codes, city names).

---

## Summary

```
K-Means assumes numerical, continuous data.
Categorical features → no meaningful mean, no meaningful distance.

Alternatives:
   K-Modes        → all categorical features
   K-Prototypes   → mixed numerical + categorical
   Gower + hierarchical → flexible, mixed types

For high-cardinality categoricals → never use one-hot + K-Means
   → use K-Modes or K-Prototypes instead
```

> If your dataset has categorical features, **don't fight K-Means** — pick the right tool from the start.
