# SQL — Joins

---

## Types of Joins

```
INNER JOIN      — only matching rows from both tables
LEFT JOIN       — all left rows + matching right (NULL if no match)
RIGHT JOIN      — all right rows + matching left (NULL if no match)
FULL OUTER JOIN — all rows from both (NULL where no match)
CROSS JOIN      — every combination (cartesian product)
SELF JOIN       — table joined with itself
```

`JOIN` without a keyword = `INNER JOIN`.

---

## Setup — Sample Tables

```
EMPLOYEE                           DEPARTMENT
+--------+-------+---------+       +---------+-----------+
| emp_id | name  | dept_id |       | dept_id | dept_name |
+--------+-------+---------+       +---------+-----------+
| E01    | Alice | D01     |       | D01     | Engg      |
| E02    | Bob   | D02     |       | D02     | Mktg      |
| E03    | Carol | NULL    |       | D03     | HR        |
| E04    | Dave  | D04     |       +---------+-----------+
+--------+-------+---------+
```

---

## INNER JOIN

Returns only rows where there is a match in **both** tables.

```sql
SELECT e.name, d.dept_name
FROM employee e
INNER JOIN department d ON e.dept_id = d.dept_id;

-- Result:
-- Alice | Engg
-- Bob   | Mktg
-- Carol and Dave excluded (no match)
```

---

## LEFT JOIN

Returns **all rows from the left table** + matched rows from right. NULL where no match.

```sql
SELECT e.name, d.dept_name
FROM employee e
LEFT JOIN department d ON e.dept_id = d.dept_id;

-- Result:
-- Alice | Engg
-- Bob   | Mktg
-- Carol | NULL   ← no dept, still included
-- Dave  | NULL   ← D04 doesn't exist, still included
```

---

## RIGHT JOIN

Returns **all rows from the right table** + matched rows from left. NULL where no match.

```sql
SELECT e.name, d.dept_name
FROM employee e
RIGHT JOIN department d ON e.dept_id = d.dept_id;

-- Result:
-- Alice | Engg
-- Bob   | Mktg
-- NULL  | HR    ← no employee in HR, still included
```

---

## FULL OUTER JOIN

Returns **all rows from both tables**. NULL where no match on either side.

```sql
SELECT e.name, d.dept_name
FROM employee e
FULL OUTER JOIN department d ON e.dept_id = d.dept_id;

-- Result:
-- Alice | Engg
-- Bob   | Mktg
-- Carol | NULL
-- Dave  | NULL
-- NULL  | HR

-- MySQL does not support FULL OUTER JOIN — running it gives:
-- ERROR 1064 (42000): You have an error in your SQL syntax
```

**Problem — MySQL throws a syntax error:**
```sql
-- This fails in MySQL:
SELECT e.name, d.dept_name
FROM employee e
FULL OUTER JOIN department d ON e.dept_id = d.dept_id;
-- ERROR 1064: syntax error at 'FULL OUTER JOIN'
```

**Fix — emulate with UNION of LEFT + RIGHT:**
```sql
-- LEFT JOIN gets: all employees + matched departments (Carol/Dave get NULL dept)
SELECT e.name, d.dept_name
FROM employee e
LEFT JOIN department d ON e.dept_id = d.dept_id

UNION

-- RIGHT JOIN gets: all departments + matched employees (HR gets NULL employee)
SELECT e.name, d.dept_name
FROM employee e
RIGHT JOIN department d ON e.dept_id = d.dept_id;

-- UNION deduplicates — rows that matched in both (Alice, Bob) appear only once
-- Result:
-- Alice | Engg
-- Bob   | Mktg
-- Carol | NULL   ← from LEFT JOIN
-- Dave  | NULL   ← from LEFT JOIN
-- NULL  | HR     ← from RIGHT JOIN
```

**Why UNION works:**
```
LEFT JOIN   →  all left rows  + matches   (covers: matched + unmatched left)
RIGHT JOIN  →  all right rows + matches   (covers: matched + unmatched right)
UNION       →  deduplicates the matched rows that appear in both
Result      →  everything from both sides = FULL OUTER JOIN
```

**UNION vs UNION ALL here:**
```
UNION     →  removes duplicates  ✓ use this (matched rows appear in both joins)
UNION ALL →  keeps duplicates    ✗ matched rows would appear twice
```

---

## CROSS JOIN

Returns every combination of rows — no join condition.

```sql
SELECT e.name, d.dept_name
FROM employee e
CROSS JOIN department d;

-- 4 employees × 3 departments = 12 rows
-- Alice-Engg, Alice-Mktg, Alice-HR, Bob-Engg, Bob-Mktg ...
```

**Use cases:**
```
Generate all combinations    — sizes × colours
Attach a single scalar value — cross join a 1-row CTE to make value available in WHERE
```

**Gotcha:** Large tables → row explosion. 1000 × 1000 = 1,000,000 rows.

---

## SELF JOIN

A table joined with **itself**. Requires two aliases.

```sql
-- Find employees in the same department
SELECT a.name AS emp1, b.name AS emp2, a.dept_id
FROM employee a
JOIN employee b ON a.dept_id = b.dept_id
WHERE a.emp_id < b.emp_id;   -- avoid duplicates and self-pairing
```

**Pattern — compare two rows from the same table:**

```sql
-- Students with same salary as their roommate
SELECT st.student_name
FROM student st
JOIN roommate rm    ON st.student_id  = rm.student_id
JOIN salary   st_sa ON st.student_id  = st_sa.student_id   -- student's salary
JOIN salary   rm_sa ON rm.roommate_id = rm_sa.student_id   -- roommate's salary
WHERE st_sa.salary = rm_sa.salary
ORDER BY st.student_id;
```

```
salary joined twice with two aliases:
  st_sa  →  student's salary row
  rm_sa  →  roommate's salary row
Any time you need to compare two rows from the same table → self-join with two aliases
```

---

## ON vs USING

```sql
-- ON — explicit, works always
JOIN department d ON e.dept_id = d.dept_id

-- USING — shorthand, column name must be identical in both tables
JOIN department d USING(dept_id)
```

| | `ON` | `USING` |
|---|---|---|
| Column names same | ✅ | ✅ required |
| Column names differ | ✅ | ❌ |
| Chained 3+ joins | ✅ safe | ⚠️ can cause ambiguity |
| Result | dept_id appears twice | dept_id merged into one column |

**Gotcha — USING in chained joins:**
```sql
-- If id_2 exists in BOTH table_1 and table_2:
FROM table_1 a
JOIN table_2 b USING(id)      -- id merged, but id_2 from a AND b both remain
JOIN table_3 c USING(id_2)    -- ✗ ambiguous — two id_2 on left side

-- Fix:
JOIN table_3 c ON a.id_2 = c.id_2   -- explicit, no ambiguity
```

Rule: `USING` safe for simple two-table joins. Use `ON` when chaining 3+ tables.

---

## Visual Summary

```
A = {1,2,3}   B = {2,3,4}

INNER JOIN     →  {2,3}          only overlap
LEFT JOIN      →  {1,2,3}        all of A
RIGHT JOIN     →  {2,3,4}        all of B
FULL OUTER     →  {1,2,3,4}      everything
CROSS JOIN     →  all combinations (A × B)
```

---

## Common Mistakes

```
1. Forgetting ORDER BY when question asks for ordered output
2. Using wrong column name  (student_name not name)
3. CROSS JOIN on large tables — row explosion
4. USING with shared column names across 3+ tables → ambiguity error
5. FULL OUTER JOIN in MySQL — not supported, use UNION of LEFT + RIGHT
6. Self-join without WHERE a.id < b.id → gets duplicate pairs
```
