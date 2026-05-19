# Pandas / NumPy Axes — Mental Model

The classic confusion: `axis=0` "says rows" but the **result** is per-column. Most people get this wrong.

```
axis = the dimension that gets COLLAPSED / EATEN / disappears

NOT "the dimension you're keeping".
```

Once this clicks, everything makes sense.

---

## The Visual

A DataFrame has two axes:

```
        col0  col1  col2
row0   [  a    b    c  ]
row1   [  d    e    f  ]
row2   [  g    h    i  ]

axis=0 → ROW axis      (rows are indexed 0, 1, 2)
axis=1 → COLUMN axis    (columns are indexed 0, 1, 2)
```

When you operate **along** an axis, that axis is what gets traversed and removed.

---

## What Each Axis Does

### `axis=0` — Move DOWN through rows

```
df.sum(axis=0)

→ traverses rows: a, d, g (down col0)
                  b, e, h (down col1)
                  c, f, i (down col2)
→ collapses rows
→ result: ONE value per COLUMN
```

Output is **column-wise**, despite saying "axis=0" / "rows".

### `axis=1` — Move ACROSS through columns

```
df.sum(axis=1)

→ traverses columns: a, b, c (across row0)
                     d, e, f (across row1)
                     g, h, i (across row2)
→ collapses columns
→ result: ONE value per ROW
```

Output is **row-wise**.

---

## Concrete Example

```python
import pandas as pd

df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})
#    A  B  C
# 0  1  4  7
# 1  2  5  8
# 2  3  6  9
```

### `axis=0` (default for most aggregations)

```python
df.sum(axis=0)
# A     6      ← 1 + 2 + 3   (moved down column A)
# B    15      ← 4 + 5 + 6   (moved down column B)
# C    24      ← 7 + 8 + 9   (moved down column C)

→ output indexed by COLUMNS (rows collapsed)
```

### `axis=1`

```python
df.sum(axis=1)
# 0    12      ← 1 + 4 + 7   (moved across row 0)
# 1    15      ← 2 + 5 + 8   (moved across row 1)
# 2    18      ← 3 + 6 + 9   (moved across row 2)

→ output indexed by ROWS (columns collapsed)
```

---

## Why It Feels Backwards

People intuitively say:
> "I want a column-wise statistic → I should use the column axis → axis=1"

**That's wrong.** The axis is the **direction of movement**, not what you operate on.

```
Column-wise OPERATION   = traverse DOWN ROWS to compute each column's value
                        = axis=0
                        
Row-wise OPERATION       = traverse ACROSS COLUMNS to compute each row's value
                        = axis=1
```

---

## Three Mental Models That Fix This

### Model 1 — "The Dimension Being Eaten"

```
axis = which dimension gets COLLAPSED
     = which dimension's labels DISAPPEAR

axis=0 → rows (0, 1, 2) disappear → output indexed by columns
axis=1 → columns (A, B, C) disappear → output indexed by rows
```

The axis you pass = the axis that goes away.

### Model 2 — "Direction of Sliding"

Imagine a hand sliding through the DataFrame:

```
axis=0 → hand slides DOWN   (vertical sweep, through rows)
axis=1 → hand slides ACROSS (horizontal sweep, through columns)
```

### Model 3 — "Shape Math" (the most precise)

```
df.shape = (3, 3)   ← (axis 0 size, axis 1 size)

df.sum(axis=0)  →  axis 0 (rows) reduced  →  shape becomes (3,)
                                              the 3 = number of columns

df.sum(axis=1)  →  axis 1 (cols) reduced  →  shape becomes (3,)
                                              the 3 = number of rows
```

**The axis you pass is the one that DISAPPEARS from the shape.**

---

## Special Case — `df.apply`

`apply` is even more confusing because the function **receives** the surviving slice:

```python
df.apply(func, axis=0)
   → function gets ONE COLUMN at a time (a Series of the column's values)
   → "go through rows" = "see all rows of one column"
   → returns one value per COLUMN

df.apply(func, axis=1)
   → function gets ONE ROW at a time (a Series indexed by column names)
   → "go across columns" = "see all columns of one row"
   → returns one value per ROW
```

Same rule:

```
axis=0 → traverse rows → see one column at a time → result is per-column
axis=1 → traverse cols → see one row at a time   → result is per-row
```

### Example

```python
df.apply(lambda col: col.max() - col.min(), axis=0)
# A    2      ← max-min of column A
# B    2      ← max-min of column B
# C    2      ← max-min of column C

df.apply(lambda row: row['A'] + row['B'], axis=1)
# 0    5      ← row 0: A + B = 1 + 4
# 1    7      ← row 1: A + B = 2 + 5
# 2    9      ← row 2: A + B = 3 + 6
```

---

## NumPy Behaves the Same

```python
import numpy as np
arr = np.array([[1, 2, 3], [4, 5, 6]])    # shape (2, 3)

arr.sum(axis=0)
# array([5, 7, 9])    ← shape (3,) — axis 0 dropped
# (1+4, 2+5, 3+6)     ← summed DOWN each column

arr.sum(axis=1)
# array([6, 15])      ← shape (2,) — axis 1 dropped
# (1+2+3, 4+5+6)      ← summed ACROSS each row
```

Same logic everywhere — the axis number is the dimension being collapsed.

---

## Cheat Sheet

```
axis=0:
   - Direction: DOWN through rows (vertical)
   - Collapses: rows
   - Result: one value per COLUMN
   - Often called: "column-wise statistic"
   - Shape: (n_rows, n_cols) → (n_cols,)

axis=1:
   - Direction: ACROSS through columns (horizontal)
   - Collapses: columns
   - Result: one value per ROW
   - Often called: "row-wise statistic"
   - Shape: (n_rows, n_cols) → (n_rows,)

Master rule:
   The axis you pass is the one that DISAPPEARS.
```

---

## Common Operations

| Operation | axis=0 (default) | axis=1 |
|-----------|------------------|--------|
| `df.sum()` | Sum each column | Sum each row |
| `df.mean()` | Mean per column | Mean per row |
| `df.max()` | Max per column | Max per row |
| `df.count()` | Non-null count per col | Non-null count per row |
| `df.apply(f)` | Apply f to each col | Apply f to each row |
| `df.dropna()` | Drop rows with NaN | Drop columns with NaN |

⚠ **Watch out:** `dropna` is the exception that confuses people the other way around. `axis=0` (default) drops ROWS — the row axis is what's being **acted upon**, not collapsed. The convention here is "drop along this axis".

For most aggregations though, the "axis = dimension that disappears" rule holds.

---

## Quick Test

```python
df.shape                  # (3, 3)
df.sum(axis=0).shape       # (3,) — axis 0 gone
df.sum(axis=1).shape       # (3,) — axis 1 gone
df.mean(axis=0).shape      # (3,)
df.mean(axis=1).shape      # (3,)
```

If you can predict the output shape every time, you've internalised the model.

---

## The Confusion Resolved — Simply

```
The axis number tells Spark WHICH AXIS TO TRAVERSE.
Traversing an axis COLLAPSES it.
The OTHER axis SURVIVES.

axis=0 → traverse rows → rows gone → columns survive → result per-column
axis=1 → traverse cols → cols gone → rows survive → result per-row
```

---

## One-Liner to Remember

```
"The axis you pass is the one that gets DESTROYED."

axis=0 → rows destroyed → output is per-column
axis=1 → cols destroyed → output is per-row
```

That's it. Internalise this and `axis` stops feeling backwards forever.
