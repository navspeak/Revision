# Structure of a Decision Tree

A decision tree is a **hierarchy of nodes connected by branches**.

```
                    [Root Node]            ← entire dataset
                   BP > 120?
                    /     \
                  Yes      No
                  /         \
            [Leaf]      [Internal Node]   ← decision rule
            Disease      Age > 50?
                          /     \
                        Yes      No
                        /         \
                    [Leaf]      [Leaf]
                    Disease    Healthy
```

---

## Node Types

| Node | Role |
|------|------|
| **Root** | Topmost — represents the full dataset before any decision |
| **Internal** | Holds a decision rule (e.g. `Age > 50?`); has children |
| **Leaf** | Endpoint — produces the prediction |
| **Branch** | The path between a node and its child — outcome of the rule (yes/no) |

---

## How a Prediction Flows

A new data point **travels down the tree**, taking branches based on its feature values until it hits a leaf:

```
New patient: BP=130, Age=45

Root:    BP > 120?     → Yes   → go left
                                   ↓
                              [Leaf: Disease]

Prediction: Disease
```

The path from root to leaf is the **rule sequence** for that prediction.

---

## Tree Depth

The **depth** of a tree is the number of levels from root to leaf.

```
Depth 1 tree:               Deep tree:
   [Root]                      [Root]
   /    \                      /    \
 leaf  leaf                  ...    ...
                              /      \
                            ...      ...
                            many levels deep
```

- Shallow tree → captures broad patterns (may underfit)
- Deep tree → captures fine details (may overfit)

This trade-off is what pruning and hyperparameter tuning aim to balance.

---

## Decision Boundaries

Each path through the tree corresponds to a **region** in feature space — a rectangular box where the prediction is constant.

```
Feature space view:

  Age
   │  region 2     │
   │  (Healthy)    │
   │               │
   │ ──────────────┤───────────────
   │               │
   │  region 1     │  region 3
   │  (Disease)    │  (Disease)
   │               │
   └────────────────────────────── BP
                  BP=120
```

Linear models give a single straight line. Trees give **axis-aligned rectangles** — stitched together to form complex boundaries.

---

## Summary

```
Root      → starting point, all data
Internal  → splits — decision rules
Leaf      → endpoints — predictions
Path      → root-to-leaf rule sequence
Depth     → controls complexity & overfitting risk
```
