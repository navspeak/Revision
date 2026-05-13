# SQL — Advanced Part 2: Ranking Advanced, Frame Clauses, LEAD/LAG Deep Dive

---

## Setup — Sample Table

```
SALES
+---------+------------+-------+
| sale_id | sale_date  | sales |
+---------+------------+-------+
| 21      | 2024-01-01 | 100   |
| 21      | 2024-01-02 | 150   |
| 21      | 2024-01-03 | 120   |
| 21      | 2024-01-04 | 200   |
| 22      | 2024-01-01 | 80    |
| 22      | 2024-01-02 | 90    |
| 22      | 2024-01-03 | 110   |
+---------+------------+-------+
```

---

## RANK vs DENSE_RANK

The only difference is what happens **after a tie**.

```
Score   RANK   DENSE_RANK
100       1        1
 90       2        2
 90       2        2      ← tie
 80       4        3      ← RANK skips 3, DENSE_RANK doesn't
 70       5        4
```

| | RANK | DENSE_RANK |
|---|---|---|
| After a tie | Skips next rank (gap) | Continues from next number |
| Use when | Gap is meaningful | Contiguous tiers needed |
| Example | Sports leaderboard, Olympics | Salary bands, top-N tiers |

**The `WHERE rnk <= 3` trap:**
```
Score   RANK   DENSE_RANK
100       1        1
 90       2        2
 90       2        2
 80       4        3   ← RANK skips to 4 → WHERE rank <= 3 misses this row
                          DENSE_RANK = 3 → WHERE dense_rank <= 3 includes it
```

Use `DENSE_RANK` when filtering top N tiers — `RANK` can silently exclude the Nth tier if there's a tie above it.

**Nth highest salary — always use DENSE_RANK:**
```
salary  RANK   DENSE_RANK
 90000    1        1
 80000    2        2
 80000    2        2      ← tie
 70000    4        3      ← RANK jumps to 4

WHERE rank = 3         -- returns nothing (3 doesn't exist)
WHERE dense_rank = 3   -- returns 70000 ✓
```

```sql
WITH ranked AS (
    SELECT salary,
        DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employee
)
SELECT salary FROM ranked WHERE rnk = 3;   -- 3rd highest
```

`DENSE_RANK` guarantees every integer 1 to N exists — `WHERE dense_rank = N` always finds the Nth distinct value. With `RANK`, tied rows consume the next number so rank N may not exist.

---

## Ranking requires ORDER BY inside OVER

Without `ORDER BY`, ranking has no basis — all rows get rank 1.

```sql
-- ✗ No ORDER BY — all rows get rank 1, pointless
RANK() OVER ()

-- ✓ ORDER BY gives ranking a basis
RANK() OVER (ORDER BY salary DESC)

-- ✓ With PARTITION BY — still needs ORDER BY to rank within each group
RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC)
```

Contrast with aggregation functions where `ORDER BY` is optional:

```
SUM()   OVER (PARTITION BY dept_id)   ✓ makes sense — sum the group
AVG()   OVER (PARTITION BY dept_id)   ✓ makes sense — avg the group
RANK()  OVER (PARTITION BY dept_id)   ✗ rank by what? all get 1
```

Aggregation functions collapse the partition — no ordering needed. Ranking functions are inherently about sequence — `ORDER BY` is required.

---

## Ranking with PARTITION BY

Rank resets within each partition — gives top N per group.

```sql
-- Top batsmen per team
RANK() OVER (PARTITION BY team ORDER BY batting_avg DESC)

-- Top salary per department
SELECT name, dept_id, salary,
    RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dept_rank
FROM employee;

-- D01: Eve(1), Alice(2), Bob(3)
-- D02: Carol(1), Dave(2)        ← rank resets for D02
-- D03: Frank(1)
```

```
Without PARTITION BY  →  one ranking across entire table
With PARTITION BY     →  separate ranking within each group (rank 1 exists in every group)
```

**Use case — find top 3 per partition:**
```sql
WITH ranked AS (
    SELECT name, dept_id, salary,
        RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
    FROM employee
)
SELECT * FROM ranked WHERE rnk <= 3;
```

---

## Ranking with Multiple Columns (Tie-breaker)

Use multiple columns in ORDER BY to break ties.

```sql
RANK() OVER (ORDER BY marks DESC, math_marks DESC)
```

```
Name    Marks  Math  RANK(Marks)  RANK(Marks, Math)
Andrew  495    98    1            2   ← tie broken, Tom has higher math
Tom     495    100   1            1   ← wins tie-break
Tobey   492    100   3            3
```

Adding a second column to ORDER BY breaks the tie — Andrew and Tom now have unique ranks.

---

## Named Windows

When the same window definition repeats multiple times, define it once with a name.

```sql
-- Without named window — repetitive:
SELECT name,
    RANK()       OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk,
    DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dense_rnk,
    ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS row_num
FROM employee;

-- With named window — cleaner:
SELECT name,
    RANK()       OVER w AS rnk,
    DENSE_RANK() OVER w AS dense_rnk,
    ROW_NUMBER() OVER w AS row_num
FROM employee
WINDOW w AS (PARTITION BY dept_id ORDER BY salary DESC);
```

```
WINDOW w AS (...)  →  defines the window once
OVER w             →  references it by name
```

---

## Frame Clauses

By default `ORDER BY` inside `OVER` gives a running total (rows up to and including current row). Frames let you define a **specific sliding window** of rows to operate on instead.

### Syntax

```sql
func() OVER (
    PARTITION BY expr
    ORDER BY expr
    ROWS BETWEEN <lower_bound> AND <upper_bound>
)
```

### Bound Options

```
UNBOUNDED PRECEDING   — from the first row of the partition
N PRECEDING           — N rows before the current row
CURRENT ROW           — the current row
N FOLLOWING           — N rows after the current row
UNBOUNDED FOLLOWING   — until the last row of the partition
```

### Frame Examples

```sql
-- 3-row moving average (current + 2 preceding)
SELECT sale_date, sales,
    AVG(sales) OVER (
        ORDER BY sale_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3
FROM sales;

-- Window slides:
-- Row 1: only row 1              avg(100)          = 100
-- Row 2: rows 1-2                avg(100,150)       = 125
-- Row 3: rows 1-3                avg(100,150,120)   = 123.3
-- Row 4: rows 2-4                avg(150,120,200)   = 156.7  ← window slid
```

```sql
-- From 2 rows before to end of partition
ROWS BETWEEN 2 PRECEDING AND UNBOUNDED FOLLOWING

-- From start of partition to 1 row after current
ROWS BETWEEN UNBOUNDED PRECEDING AND 1 FOLLOWING

-- Only current row and next row
ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING
```

### Default Frame Behaviour

```
With ORDER BY (no frame specified):
  default = RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  → running total up to current row

Without ORDER BY (no frame specified):
  default = ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  → entire partition (same as OVER(PARTITION BY x) with no ORDER BY)
```

```sql
-- These two are identical:
SUM(sales) OVER (ORDER BY sale_date)
SUM(sales) OVER (ORDER BY sale_date RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

### ROWS vs RANGE

```
ROWS   — physical rows, counts by position
RANGE  — logical range, includes all rows with same ORDER BY value (handles ties)
```

**No ties — identical behaviour:**
```
sale_date   sales   ROWS running total   RANGE running total
2024-01-01  100     100                  100
2024-01-02  150     250                  250
2024-01-03  120     370                  370
2024-01-04  200     570                  570
```

**With ties — they diverge:**
```
sale_date   sales
2024-01-01  100
2024-01-02  150   ← same date
2024-01-02  120   ← same date (tie)
2024-01-03  200
```

```
sale_date   sales   ROWS running total        RANGE running total
2024-01-01  100     100                        100
2024-01-02  150     250  ← up to this row      370  ← RANGE includes BOTH Jan-02 rows
2024-01-02  120     370  ← up to this row      370  ← same value, same group
2024-01-03  200     570                        570
```

```
ROWS: each physical row is its own boundary
      Jan-02 row 1 → sum = 100+150 = 250
      Jan-02 row 2 → sum = 100+150+120 = 370

RANGE: all rows with same sale_date = "current"
       both Jan-02 rows treated as one group → both get sum = 100+150+120 = 370
```

**When to use which:**
```
ROWS   — almost always correct for sliding windows (moving avg etc.)
         predictable, position-based

RANGE  — when ties should be grouped together
         default with ORDER BY — can surprise you if ties exist

Be explicit with ROWS BETWEEN when ORDER BY column has duplicate values
```

### DESC reverses the frame

```sql
-- With DESC, "PRECEDING" means rows that come AFTER in natural order
ORDER BY sale_date DESC
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
-- takes the 2 rows with later dates + current row
```

---

## LEAD and LAG — Deep Dive

### Syntax

```sql
LEAD(return_value, offset, default) OVER (PARTITION BY ... ORDER BY ...)
LAG (return_value, offset, default) OVER (PARTITION BY ... ORDER BY ...)
```

```
return_value  — column to fetch from
offset        — how many rows forward (LEAD) or back (LAG). Default = 1
default       — value when no row exists (NULL if not specified)
```

---

### LEAD — fetch from next row

```sql
SELECT sale_id, sale_date, sales,
    LEAD(sales) OVER (ORDER BY sale_date) AS sales_next_day
FROM sales;

-- sale_id  sale_date   sales  sales_next_day
-- 21       2024-01-01  100    150    ← next row's value
-- 21       2024-01-02  150    120
-- 21       2024-01-03  120    200
-- 21       2024-01-04  200    NULL   ← no next row
-- 22       2024-01-01  80     90
-- 22       2024-01-02  90     110
-- 22       2024-01-03  110    NULL   ← no next row
```

---

### LAG — fetch from previous row

```sql
SELECT sale_id, sale_date, sales,
    LAG(sales, 2) OVER (ORDER BY sale_date) AS sales_2_days_ago
FROM sales;

-- sale_date   sales  sales_2_days_ago
-- 2024-01-01  100    NULL   ← no 2nd previous row
-- 2024-01-02  150    NULL   ← no 2nd previous row
-- 2024-01-03  120    100    ← 2 rows back
-- 2024-01-04  200    150
```

---

### LEAD/LAG with PARTITION BY

Shifting resets at the start of each partition — the first row of a new partition has no "previous" row within it.

```sql
SELECT sale_id, sale_date, sales,
    LAG(sales, 2) OVER (
        PARTITION BY sale_id
        ORDER BY sale_date
    ) AS sales_2_days_ago_by_id
FROM sales;

-- sale_id  sale_date   sales  sales_2_days_ago_by_id
-- 21       2024-01-01  100    NULL   ← partition 21 starts
-- 21       2024-01-02  150    NULL
-- 21       2024-01-03  120    100
-- 21       2024-01-04  200    150
-- 22       2024-01-01  80     NULL   ← partition 22 starts, resets
-- 22       2024-01-02  90     NULL
-- 22       2024-01-03  110    80
```

---

### Practical use — day-on-day change

```sql
SELECT sale_date, sales,
    LAG(sales) OVER (ORDER BY sale_date)              AS prev_day,
    sales - LAG(sales) OVER (ORDER BY sale_date)      AS day_change,
    ROUND(
        (sales - LAG(sales) OVER (ORDER BY sale_date))
        * 100.0 / LAG(sales) OVER (ORDER BY sale_date)
    , 2)                                               AS pct_change
FROM sales
WHERE sale_id = 21;
```

---

## Summary

### Frame clause cheat sheet

| Frame | Meaning |
|---|---|
| `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` | Running total from start |
| `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` | 3-row sliding window |
| `ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING` | From current to end |
| `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` | Entire partition |
| `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` | 3-row centred window |

### LEAD/LAG cheat sheet

| | LEAD | LAG |
|---|---|---|
| Direction | Forward (next rows) | Backward (previous rows) |
| NULL appears | Last N rows | First N rows |
| Default offset | 1 | 1 |
| With PARTITION BY | Resets at partition boundary | Resets at partition boundary |

---

## Gotchas

```
1. Frame only makes sense with ORDER BY inside OVER
   Without ORDER BY, frame = whole partition anyway

2. ROWS vs RANGE matters when there are ties in ORDER BY column
   ROWS = physical position, RANGE = logical value grouping

3. LAG/LEAD with PARTITION BY — NULL resets at every partition boundary
   Not a bug — LAG looks back within the partition only

4. Default frame with ORDER BY is RANGE not ROWS
   Can give unexpected results with ties — be explicit with ROWS BETWEEN

5. DESC in ORDER BY flips what PRECEDING and FOLLOWING mean
```