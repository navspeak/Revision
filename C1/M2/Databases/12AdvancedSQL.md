# SQL — Advanced: CASE, Window Functions, LEAD/LAG, Ranking

---

## Setup — Sample Table

```
EMPLOYEE
+--------+--------+---------+--------+------------+
| emp_id | name   | dept_id | salary | join_date  |
+--------+--------+---------+--------+------------+
| E01    | Alice  | D01     | 70000  | 2020-01-15 |
| E02    | Bob    | D01     | 50000  | 2019-03-10 |
| E03    | Carol  | D02     | 90000  | 2021-06-01 |
| E04    | Dave   | D02     | 60000  | 2020-08-20 |
| E05    | Eve    | D01     | 80000  | 2022-02-14 |
| E06    | Frank  | D03     | 55000  | 2021-11-30 |
+--------+--------+---------+--------+------------+
```

---

## CASE Statement

Conditional logic inside SQL — like if/else.

### Simple CASE

```sql
-- Simple CASE — matches a value
SELECT name,
    CASE dept_id
        WHEN 'D01' THEN 'Engineering'
        WHEN 'D02' THEN 'Marketing'
        WHEN 'D03' THEN 'HR'
        ELSE 'Unknown'
    END AS dept_name
FROM employee;
```

### Searched CASE

```sql
-- Searched CASE — evaluates conditions
SELECT name, salary,
    CASE
        WHEN salary >= 80000 THEN 'High'
        WHEN salary >= 60000 THEN 'Mid'
        ELSE                      'Low'
    END AS salary_band
FROM employee;

-- Result:
-- Alice  70000  Mid
-- Bob    50000  Low
-- Carol  90000  High
-- Dave   60000  Mid
-- Eve    80000  High
-- Frank  55000  Low
```

### CASE in GROUP BY / ORDER BY

```sql
-- Count per salary band
SELECT
    CASE
        WHEN salary >= 80000 THEN 'High'
        WHEN salary >= 60000 THEN 'Mid'
        ELSE 'Low'
    END AS salary_band,
    COUNT(*) AS cnt
FROM employee
GROUP BY salary_band;   -- alias used here

-- Sort by custom order
SELECT name, salary
FROM employee
ORDER BY
    CASE
        WHEN salary >= 80000 THEN 1
        WHEN salary >= 60000 THEN 2
        ELSE 3
    END;

-- With tiebreaker — deterministic within each band
ORDER BY
    CASE
        WHEN salary >= 80000 THEN 1
        WHEN salary >= 60000 THEN 2
        ELSE 3
    END,
    salary DESC;
```

**`ORDER BY CASE` vs `ORDER BY salary DESC`:**

For contiguous numeric bands, `ORDER BY salary DESC` produces the same grouping AND gives deterministic within-band order:
```
salary DESC:  90000, 81000, 80000, 69000, 68000, 700, 68
CASE order:   High(any order), Mid(any order), Low(any order)
→ same groups, but salary DESC is more predictable within each group
```

**Use `CASE` when bands are non-contiguous or non-numeric** — salary DESC breaks down:
```
Rule: High = salary >= 80000 OR salary < 100  (VIPs and interns first)

salary DESC:  90000, 81000, 80000, 69000, 68000, 700, 68  ← 68, 700 at the bottom ✗
CASE order:   90000, 81000, 80000, 68, 700, 69000, 68000  ← 68, 700 jump to top   ✓
```

```
ORDER BY salary DESC  →  pure numeric, simple, deterministic — use when bands are contiguous ranges
ORDER BY CASE         →  arbitrary business rules, non-contiguous, non-numeric priority
```

**How does `GROUP BY salary_band` work if SELECT runs after GROUP BY?**

```
Standard execution order:
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT

GROUP BY runs at step 3, SELECT alias is defined at step 5
→ In standard SQL, GROUP BY salary_band should fail — alias not yet defined
```

**MySQL is an exception** — it allows SELECT aliases in GROUP BY as a convenience extension.
MySQL internally expands the alias back to the full CASE expression before executing.

```sql
-- What MySQL actually runs:
GROUP BY
    CASE
        WHEN salary >= 80000 THEN 'High'
        WHEN salary >= 60000 THEN 'Mid'
        ELSE 'Low'
    END

-- Standard SQL / PostgreSQL / SQL Server require this explicitly:
-- You must repeat the full CASE expression in GROUP BY
```

| Clause | MySQL alias allowed? | Standard SQL / PostgreSQL / SQL Server |
|---|---|---|
| `GROUP BY alias` | ✅ MySQL extension | ❌ must repeat expression |
| `HAVING alias` | ❌ | ❌ must repeat expression |
| `ORDER BY alias` | ✅ | ✅ (ORDER BY runs after SELECT) |

---

## Window Functions

Perform calculations **across a set of rows related to the current row** — without collapsing rows like GROUP BY does.

```
Aggregate (GROUP BY)  →  collapses rows into one per group
Window function       →  keeps all rows, adds a calculated column alongside
```

### Syntax

```sql
function_name() OVER (
    PARTITION BY column    -- divide into groups (optional)
    ORDER BY column        -- order within each group (optional)
    ROWS/RANGE BETWEEN ... -- frame definition (optional)
)
```

---

## OVER and PARTITION BY

```sql
-- Total salary per department (without GROUP BY — all rows kept)
SELECT
    name,
    dept_id,
    salary,
    SUM(salary) OVER (PARTITION BY dept_id) AS dept_total
FROM employee;

-- Result:
-- Alice  D01  70000  200000   ← sum of D01 (70+50+80)
-- Bob    D01  50000  200000
-- Eve    D01  80000  200000
-- Carol  D02  90000  150000   ← sum of D02 (90+60)
-- Dave   D02  60000  150000
-- Frank  D03  55000  55000
```

```sql
-- Running total within each department (ORDER BY adds cumulative sum)
SELECT
    name,
    dept_id,
    salary,
    SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary) AS running_total
FROM employee;

-- Output (ORDER BY salary ASC default — lowest cumulates first within each dept):
-- name   dept_id  salary  running_total
-- Bob    D01      50000   50000          ← D01 starts
-- Alice  D01      70000   120000         ← 50000 + 70000
-- Eve    D01      80000   200000         ← 50000 + 70000 + 80000
-- Dave   D02      60000   60000          ← D02 resets
-- Carol  D02      90000   150000         ← 60000 + 90000
-- Frank  D03      55000   55000          ← D03 resets
```

```
PARTITION BY dept_id  →  running total resets at each new department
ORDER BY salary ASC   →  lowest salary cumulates first within partition
No ORDER BY           →  shows full partition sum on every row (not cumulative)

-- To cumulate highest first:
SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary DESC)
-- D01: Eve(80000) → Eve+Alice(150000) → Eve+Alice+Bob(200000)
```

```sql
-- Grand total alongside every row (no PARTITION BY = whole table is one window)
SELECT name, salary,
    SUM(salary) OVER () AS grand_total,
    ROUND(salary * 100.0 / SUM(salary) OVER (), 2) AS pct_of_total
FROM employee;

-- Grand total = 70000+50000+90000+60000+80000+55000 = 405000
-- name   salary  grand_total  pct_of_total
-- Alice  70000   405000       17.28
-- Bob    50000   405000       12.35
-- Carol  90000   405000       22.22
-- Dave   60000   405000       14.81
-- Eve    80000   405000       19.75
-- Frank  55000   405000       13.58
--                             99.99  ← rounding difference

-- OVER() = no PARTITION BY, no ORDER BY → entire table is one window → 405000 on every row
```

**PARTITION BY vs GROUP BY — direct comparison:**

```sql
-- GROUP BY — 3 rows, individual columns lost
SELECT dept_id, SUM(salary) AS dept_total
FROM employee
GROUP BY dept_id;
-- D01  200000
-- D02  150000
-- D03  55000

-- PARTITION BY — 6 rows, all individual columns kept
SELECT name, dept_id, salary,
    SUM(salary) OVER (PARTITION BY dept_id) AS dept_total
FROM employee;
-- Alice  D01  70000  200000
-- Bob    D01  50000  200000
-- Eve    D01  80000  200000
-- Carol  D02  90000  150000
-- Dave   D02  60000  150000
-- Frank  D03  55000  55000
```

| | `GROUP BY` | `OVER (PARTITION BY)` |
|---|---|---|
| Rows returned | One per group | All original rows kept |
| Individual columns | Lost | ✅ still accessible |
| Aggregate value | One per group | Repeated on every row in group |
| Use when | Summary only | Summary alongside detail |

**Classic use case — salary as % of department total:**
```sql
-- Impossible with GROUP BY alone (individual rows are gone)
-- Easy with window function:
SELECT name, salary,
    ROUND(salary * 100.0 / SUM(salary) OVER (PARTITION BY dept_id), 2) AS pct_of_dept
FROM employee;
-- Alice  70000  35.0%  (70000/200000)
-- Bob    50000  25.0%
-- Eve    80000  40.0%
-- With GROUP BY you'd need a JOIN or subquery to bring the total back to each row
```

---

## Aggregate Functions with Window Functions

Four key variations — same function, different OVER clause, different result:

```sql
-- 1. PARTITION BY only — sum for entire partition, same value on every row in group
SUM(salary) OVER (PARTITION BY dept_id) AS dept_total
-- D01 rows all show 200000, D02 rows all show 150000

-- 2. PARTITION BY + ORDER BY — running total within partition (cumulative)
SUM(salary) OVER (PARTITION BY dept_id ORDER BY join_date) AS running_dept_total
-- D01: Bob=50000, Bob+Alice=120000, Bob+Alice+Eve=200000

-- 3. ORDER BY only, no PARTITION BY — running total across whole table
SUM(salary) OVER (ORDER BY join_date) AS running_total_so_far
-- cumulative sum of all employees ordered by join date

-- 4. Empty OVER() — grand total, same value on every row
SUM(salary) OVER () AS grand_total
-- every row shows the same number: sum of all salaries
```

**Visual summary — what changes:**

```
OVER (PARTITION BY dept_id)                 →  group total,    resets per partition
OVER (PARTITION BY dept_id ORDER BY date)   →  running total,  resets per partition
OVER (ORDER BY date)                        →  running total,  across whole table
OVER ()                                     →  grand total,    one value for all rows
```

**Key point:** `OVER()` is what makes it a window function — even with no PARTITION BY or ORDER BY. Without `OVER()` it would be a plain aggregate that collapses rows. With `OVER()` all individual rows are preserved.

```sql
-- Plain aggregate — collapses to 1 row
SELECT SUM(salary) FROM employee;               -- 405000

-- Window function — all rows kept, value repeated
SELECT name, SUM(salary) OVER () FROM employee; -- 6 rows, each showing 405000
```

---

## ROW_NUMBER

Assigns a unique sequential number to each row within the window.

```sql
SELECT
    name, dept_id, salary,
    ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS row_num
FROM employee;

-- D01: Eve(1), Alice(2), Bob(3)
-- D02: Carol(1), Dave(2)
-- D03: Frank(1)
```

---

## Ranking Functions

**Why not just ORDER BY + LIMIT?**
```
LIMIT is rigid — only top/bottom N rows
RANK lets you get middle ranges: rank 50–100 in a 1000-product listing
RANK is also portable across databases; LIMIT syntax varies
```

---

### RANK()

Assigns rank — **ties get the same rank, next rank skips** (1,1,3).

```sql
RANK() OVER (ORDER BY expr [ASC|DESC])
```

```sql
SELECT name, salary,
    RANK() OVER (ORDER BY salary DESC) AS rnk
FROM employee;

-- No ties:           Ties example:
-- Carol  90000  1    Andrew  495  1
-- Eve    80000  2    Tom     495  1   ← tie, both rank 1
-- Alice  70000  3    Tobey   492  3   ← skips 2, gap
-- Dave   60000  4
-- Frank  55000  5    If 10 students scored 495 → Tobey's rank = 11
-- Bob    50000  6
```

---

### DENSE_RANK()

Assigns rank — **ties get the same rank, next rank does NOT skip** (1,1,2).

```sql
DENSE_RANK() OVER (ORDER BY expr [ASC|DESC])
```

```sql
-- Ties example:
-- Andrew  495  1
-- Tom     495  1   ← tie, both rank 1
-- Tobey   492  2   ← no gap, next is 2 not 3

-- If 10 students scored 495 → Tobey's DENSE_RANK = 2 still
```

---

### PERCENT_RANK()

Relative rank as a percentage between 0 and 1 — useful for percentiles.

```sql
PERCENT_RANK() OVER (ORDER BY expr [ASC|DESC])

-- Formula: (rank - 1) / (total rows - 1)
```

```sql
SELECT name, salary,
    ROUND(PERCENT_RANK() OVER (ORDER BY salary), 4) AS pct_rank
FROM employee;

-- Bob    50000  0.0    ← lowest (0th percentile)
-- Frank  55000  0.2
-- Dave   60000  0.4
-- Alice  70000  0.6
-- Eve    80000  0.8
-- Carol  90000  1.0    ← highest (100th percentile)
```

**Use case:** top 10% of customers = `PERCENT_RANK() >= 0.9`

---

### ROW_NUMBER()

Assigns unique sequential numbers — no ties ever.

```sql
ROW_NUMBER() OVER (ORDER BY expr [ASC|DESC])
```

```sql
SELECT name, salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num
FROM employee;
-- always 1,2,3,4,5,6 — even if salaries are equal
```

**Use cases:**
- Top 10 selling products (guaranteed exactly 10 rows)
- Top 3 winners in a race (no shared positions)
- Deduplicate rows (keep row_num = 1 per group)

---

### RANK vs DENSE_RANK vs ROW_NUMBER — side by side

```
Marks: 495, 495, 492, 490

Name    Marks  ROW_NUMBER  RANK  DENSE_RANK
Andrew  495    1           1     1
Tom     495    2           1     1     ← tie: ROW_NUMBER differs, RANK/DENSE same
Tobey   492    3           3     2     ← RANK skips 2, DENSE_RANK does not
Alice   490    4           4     3
```

| Function | Ties | Gap after tie | Always unique |
|---|---|---|---|
| `ROW_NUMBER` | Different numbers | N/A | ✅ |
| `RANK` | Same number | ✅ yes | ❌ |
| `DENSE_RANK` | Same number | ❌ no | ❌ |
| `PERCENT_RANK` | Same percentage | ❌ no | ❌ |

---

## LEAD and LAG

Fetch values from **next** or **previous** rows without a self-join.

### LAG — look back

```sql
-- LAG(column, offset, default)
SELECT
    name,
    join_date,
    salary,
    LAG(salary, 1, 0) OVER (ORDER BY join_date) AS prev_salary
FROM employee;

-- Bob    2019  50000  0        ← no previous row, default 0
-- Alice  2020  70000  50000
-- Dave   2020  60000  70000
-- Carol  2021  90000  60000
-- Frank  2021  55000  90000
-- Eve    2022  80000  55000
```

### LEAD — look ahead

```sql
-- LEAD(column, offset, default)
SELECT
    name,
    join_date,
    salary,
    LEAD(salary, 1, 0) OVER (ORDER BY join_date) AS next_salary
FROM employee;

-- Bob    2019  50000  70000
-- Alice  2020  70000  60000
-- Dave   2020  60000  90000
-- Carol  2021  90000  55000
-- Frank  2021  55000  80000
-- Eve    2022  80000  0        ← no next row, default 0
```

### Practical use — salary change from previous employee

```sql
SELECT
    name,
    salary,
    LAG(salary)  OVER (ORDER BY salary) AS prev_salary,
    salary - LAG(salary) OVER (ORDER BY salary) AS diff
FROM employee;
```

### LEAD/LAG within partitions

```sql
-- Compare to previous colleague in same department
SELECT
    name, dept_id, salary,
    LAG(salary) OVER (PARTITION BY dept_id ORDER BY salary) AS prev_in_dept
FROM employee;
```

---

## Quick Reference

| Function | What it does |
|---|---|
| `CASE WHEN` | Conditional logic, classify rows |
| `ROW_NUMBER()` | Unique sequential number per row |
| `RANK()` | Rank with gaps after ties |
| `DENSE_RANK()` | Rank without gaps after ties |
| `PERCENT_RANK()` | Relative rank 0.0 to 1.0 |
| `LAG(col, n)` | Value from n rows before current |
| `LEAD(col, n)` | Value from n rows after current |
| `SUM() OVER()` | Running/partitioned sum |
| `PARTITION BY` | Divide window into groups |
| `ORDER BY` inside OVER | Defines row order within window |

---

## Gotchas

```
1. Window functions cannot be used in WHERE — use a subquery or CTE:
   -- WRONG:
   WHERE RANK() OVER (ORDER BY salary) = 1

   -- CORRECT:
   WITH ranked AS (
       SELECT name, RANK() OVER (ORDER BY salary DESC) AS rnk FROM employee
   )
   SELECT name FROM ranked WHERE rnk = 1;

2. PARTITION BY is optional — omitting it means the whole table is one window

3. ORDER BY inside OVER ≠ ORDER BY at query level
   They are independent — one sorts the window, the other sorts the output

4. RANK vs DENSE_RANK — always clarify in interviews which behaviour is needed
   "Top 3 salaries" with ties: DENSE_RANK gives true top 3, RANK may give fewer

5. LAG/LEAD default value — always provide a default (3rd arg) to avoid NULL
   LAG(salary, 1, 0)  →  returns 0 instead of NULL for first row
```
