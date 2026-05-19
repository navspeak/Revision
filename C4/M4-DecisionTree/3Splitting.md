# How Decision Trees Split

The whole tree-building process boils down to one question repeated at every node:

> **What is the best feature and the best condition to divide this data?**

Each split aims to produce **subgroups more homogeneous than the parent**.

---

## Splitting on Categorical Features

### Binary features (yes/no, M/F)

Straightforward — only one split possible:

```
Sex?
   ├── Male  → left subgroup
   └── Female → right subgroup
```

### Categorical with multiple levels

For a feature like `Weather ∈ {Sunny, Rainy, Cloudy}`, the algorithm tries subsets:

```
Possible splits:
  Sunny    vs  {Rainy, Cloudy}
  Rainy    vs  {Sunny, Cloudy}
  Cloudy   vs  {Sunny, Rainy}
```

It picks the split that best separates the target.

---

## Splitting on Numerical Features

For continuous features, the tree picks a **threshold**:

```
Sort the data points by the feature value.
For each pair of adjacent points, the midpoint is a candidate threshold.

Age: [25, 30, 41, 45, 50, 58, 62]
Candidate thresholds: 27.5, 35.5, 43, 47.5, 54, 60
```

Each threshold creates two groups:

```
Age > 43?
   ├── Yes (45, 50, 58, 62)
   └── No  (25, 30, 41)
```

The algorithm tries every candidate and keeps the threshold that gives the best split.

---

## Splitting with Multiple Predictors

In real data you have many features. At each node the tree:

1. Considers **every feature**
2. For each feature, evaluates **every possible split**
3. Picks the (feature, condition) pair that gives the **clearest division**

```
At root:
  Feature 1 (BP): best split at BP > 120  → score X
  Feature 2 (Age): best split at Age > 50 → score Y
  Feature 3 (Sex): Male vs Female         → score Z

  Pick the one with the best score
```

The result: the first split might be on BP, the second on Age, the third on Sex — the tree adapts naturally to the data.

---

## What Makes a Split "Good"?

Not all splits are equally useful:

```
Bad split:                       Good split:
  Parent: 50% Yes, 50% No        Parent: 50% Yes, 50% No
     /                \              /                \
  50% Yes, 50% No   ...           95% Yes, 5% No    90% No, 10% Yes
  (no improvement)                (much purer subgroups)
```

We need a **numerical measure of how good a split is**. Two such measures for classification:

- **Gini index** → next file
- **Entropy / Information Gain** → next file

For regression:

- **Variance reduction** → later file

---

## Greedy Search

The tree picks the **best split at each node** without looking ahead. This is called a **greedy** strategy:

```
At each step: pick the locally-best split
No backtracking, no global optimisation
```

Not guaranteed to give the globally best tree — but efficient and works well in practice.

---

## Summary

```
Categorical feature → group categories
Numerical feature   → pick a threshold
Multiple features   → try all features × all splits, pick best
Strategy            → greedy (best at each step)
Quality measured by → Gini / Entropy / Variance reduction
```
