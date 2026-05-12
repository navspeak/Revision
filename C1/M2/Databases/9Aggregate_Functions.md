# SQL — Aggregate Functions

Aggregate functions operate on a **set of rows** and return a **single value**.

```
COUNT  SUM  AVG  MIN  MAX
```

---

## Setup — Sample Tables

```
EMPLOYEE
+--------+--------+---------+--------+----------+
| emp_id | name   | dept_id | salary | join_year|
+--------+--------+---------+--------+----------+
| E01    | Alice  | D01     | 70000  | 2020     |
| E02    | Bob    | D01     | 50000  | 2019     |
| E03    | Carol  | D02     | 90000  | 2021     |
| E04    | Dave   | D02     | 60000  | 2020     |
| E05    | Eve    | D03     | NULL   | 2022     |
+--------+--------+---------+--------+----------+
```

---

## COUNT

```sql
COUNT(*)        -- counts every row, NULLs included
COUNT(1)        -- counts every row, NULLs included  (same as COUNT(*))
COUNT(column)   -- counts only non-NULL values in that column

SELECT COUNT(*)       FROM employee;    -- 5
SELECT COUNT(1)       FROM employee;    -- 5
SELECT COUNT(salary)  FROM employee;    -- 4  (Eve's salary is NULL, skipped)
SELECT COUNT(dept_id) FROM employee;    -- 5  (no NULLs in dept_id)

-- Count distinct values
SELECT COUNT(DISTINCT dept_id) FROM employee;   -- 3
```

**Gotcha:** `COUNT(*)` ≠ `COUNT(column)` when NULLs are present.

**`COUNT(*)` vs `COUNT(1)`:** identical result — `1` is a constant, every row evaluates it as non-NULL so every row is counted. No performance difference in modern databases. Prefer `COUNT(*)` — standard SQL, clearer intent.

---

## SUM

```sql
SELECT SUM(salary) FROM employee;           -- 270000  (NULL ignored)
SELECT SUM(salary) FROM employee WHERE dept_id = 'D01';  -- 120000
```

**Gotcha:** `SUM` ignores NULL — does not treat it as 0.

---

## AVG

```sql
SELECT AVG(salary) FROM employee;           -- 67500  (270000 / 4, NULL excluded)
```

**Gotcha:** AVG ignores NULL rows entirely — denominator is 4, not 5.
If you want NULL treated as 0:
```sql
SELECT AVG(COALESCE(salary, 0)) FROM employee;   -- 54000  (270000 / 5)
```

---

## MIN / MAX

```sql
SELECT MIN(salary) FROM employee;    -- 50000
SELECT MAX(salary) FROM employee;    -- 90000
SELECT MIN(name)   FROM employee;    -- Alice  (alphabetical)
SELECT MAX(name)   FROM employee;    -- Eve

SELECT MIN(join_year), MAX(join_year) FROM employee;   -- 2019, 2022
```

---

## GROUP BY

Groups rows with the same value and applies the aggregate per group.

```sql
-- Total salary per department
SELECT dept_id, SUM(salary) AS total_salary
FROM employee
GROUP BY dept_id;

-- dept_id | total_salary
-- D01     | 120000
-- D02     | 150000
-- D03     | NULL

-- Count employees per department
SELECT dept_id, COUNT(*) AS headcount
FROM employee
GROUP BY dept_id;

-- Average salary per join year
SELECT join_year, ROUND(AVG(salary), 2) AS avg_salary
FROM employee
GROUP BY join_year
ORDER BY join_year;
```

**Rules:**
```
Every column in SELECT must be either:
  1. Inside an aggregate function   SUM(salary)
  2. In the GROUP BY clause         dept_id

You CANNOT select a non-aggregated column that is not in GROUP BY.
```

---

## HAVING

Filters **groups** after aggregation. `WHERE` filters rows before aggregation.

```sql
-- Departments with total salary > 100000
SELECT dept_id, SUM(salary) AS total_salary
FROM employee
GROUP BY dept_id
HAVING SUM(salary) > 100000;

-- Departments with more than 1 employee
SELECT dept_id, COUNT(*) AS headcount
FROM employee
GROUP BY dept_id
HAVING COUNT(*) > 1;
```

**WHERE vs HAVING:**
```sql
-- WHERE  — filters rows BEFORE grouping   (cannot use aggregate functions)
-- HAVING — filters groups AFTER grouping  (can use aggregate functions)

-- Find depts where avg salary > 60000, only for employees hired after 2019
SELECT dept_id, AVG(salary)
FROM employee
WHERE join_year > 2019          -- ← filters rows first
GROUP BY dept_id
HAVING AVG(salary) > 60000;    -- ← filters groups after
```

---

## Query Execution Order

```
1. FROM       — which table
2. WHERE      — filter rows
3. GROUP BY   — group remaining rows
4. HAVING     — filter groups
5. SELECT     — compute output columns
6. ORDER BY   — sort
7. LIMIT      — restrict rows returned
```

**Why this matters:**
```sql
-- WRONG — cannot use alias in HAVING (alias defined in SELECT, step 5)
SELECT dept_id, SUM(salary) AS total
FROM employee
GROUP BY dept_id
HAVING total > 100000;          -- ✗ 'total' not yet defined at HAVING step

-- CORRECT
HAVING SUM(salary) > 100000;   -- ✓ repeat the expression
```

---

## Quick Reference

| Function | Ignores NULL? | Works on text? |
|---|---|---|
| `COUNT(*)` | ❌ counts all | N/A |
| `COUNT(col)` | ✅ | ✅ |
| `SUM` | ✅ | ❌ |
| `AVG` | ✅ (denominator excludes NULLs) | ❌ |
| `MIN` | ✅ | ✅ (alphabetical) |
| `MAX` | ✅ | ✅ (alphabetical) |

---

## Practice Questions

**Q1.** How many employees have a salary recorded?
```sql
SELECT COUNT(salary) FROM employee;    -- 4  (not 5 — Eve is NULL)
```

**Q2.** What is the average salary including employees with no salary (treat as 0)?
```sql
SELECT AVG(COALESCE(salary, 0)) FROM employee;   -- 54000
```

**Q3.** Which departments have more than one employee?
```sql
SELECT dept_id, COUNT(*) AS headcount
FROM employee
GROUP BY dept_id
HAVING COUNT(*) > 1;
```

**Q4.** Find the highest paid employee in each department.
```sql
SELECT dept_id, MAX(salary) AS max_salary
FROM employee
GROUP BY dept_id;
```

**Q5.** Count employees per join year, only for years with more than 1 employee, sorted newest first.
```sql
SELECT join_year, COUNT(*) AS cnt
FROM employee
GROUP BY join_year
HAVING COUNT(*) > 1
ORDER BY join_year DESC;
```

---

## Tricky Interview Questions

**Q1. What is the difference between COUNT(*) and COUNT(1)?**
```
COUNT(*)  — counts all rows
COUNT(1)  — counts all rows (1 is a non-NULL constant, same result)
Both are identical in all major databases. COUNT(*) is preferred for clarity.
```

**Q2. Why does AVG give a different result than SUM/COUNT?**
```sql
SELECT AVG(salary)              FROM employee;   -- 67500  (270000 / 4)
SELECT SUM(salary) / COUNT(*)   FROM employee;   -- 54000  (270000 / 5)

AVG ignores NULLs in both numerator AND denominator.
SUM/COUNT(*) includes the NULL row in COUNT → different denominator.
Use SUM/COUNT(*) when you want NULLs treated as 0.
```

**Q3. Can you use WHERE and HAVING in the same query?**
```sql
-- Yes — they filter at different stages
SELECT dept_id, AVG(salary)
FROM employee
WHERE join_year > 2019          -- removes rows before grouping
GROUP BY dept_id
HAVING AVG(salary) > 60000;    -- removes groups after aggregation
```

**Q4. What does GROUP BY on multiple columns do?**
```sql
SELECT dept_id, join_year, COUNT(*) AS cnt
FROM employee
GROUP BY dept_id, join_year;
-- creates one group per unique (dept_id + join_year) combination
-- D01 + 2020 is a different group from D01 + 2019
```

**Q5. Can you GROUP BY a column not in SELECT?**
```sql
-- Yes — GROUP BY does not require the column to appear in SELECT
SELECT COUNT(*) AS cnt
FROM employee
GROUP BY dept_id;    -- groups by dept_id but doesn't show it
-- valid but confusing — avoid in practice
```

**Q6. What happens when you SUM a column that is all NULL?**
```sql
SELECT SUM(salary) FROM employee WHERE dept_id = 'D99';
-- Returns NULL, not 0
-- Use COALESCE to handle: COALESCE(SUM(salary), 0)
```

**Q7. Find departments where the max salary is greater than twice the min salary.**
```sql
SELECT dept_id
FROM employee
GROUP BY dept_id
HAVING MAX(salary) > 2 * MIN(salary);
```

**Q8. Why can't you use an aggregate function in a WHERE clause?**
```sql
-- WRONG:
SELECT * FROM employee WHERE salary > AVG(salary);   -- ✗ error

-- WHY: WHERE runs before GROUP BY/aggregation (step 2 vs step 4)
--      AVG hasn't been computed yet when WHERE is evaluated

-- CORRECT — use a subquery:
SELECT * FROM employee
WHERE salary > (SELECT AVG(salary) FROM employee);
```
