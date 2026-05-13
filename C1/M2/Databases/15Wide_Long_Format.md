# SQL — Wide and Long Format

---

## What are they?

**Wide format** — one row per entity, variables spread across multiple columns.
**Long format** — one row per observation, variables and values in separate columns.

```
WIDE FORMAT                              LONG FORMAT
+--------+-------------+---------+-------+  +--------+-----------+-----------+
| mov_id | movie_title | genre_1 |genre_2|  | mov_id | attribute | value     |
+--------+-------------+---------+-------+  +--------+-----------+-----------+
| 101    | Inception   | Sci-Fi  | Drama |  | 101    | movie_title| Inception|
| 219    | Interstellar| Sci-Fi  | NULL  |  | 101    | genre_1   | Sci-Fi    |
+--------+-------------+---------+-------+  | 101    | genre_2   | Drama     |
                                            | 219    | movie_title|Interstellar|
                                            | 219    | genre_1   | Sci-Fi    |
                                            | (no genre_2 row — NULL skipped)|
                                            +--------+-----------+-----------+
```

---

## When to use each

| | Wide | Long |
|---|---|---|
| Readability | ✅ easier to read | ❌ harder to scan |
| Storage | ❌ NULLs waste space | ✅ NULL rows simply don't exist |
| Analysis | ✅ most SQL queries | ✅ time-series, repeated measures |
| Aggregation | ✅ standard GROUP BY | ✅ filter by attribute name |

**Key benefit of long format:** NULL values just don't have a row — no wasted storage. In wide format, `genre_2 = NULL` for mov_id 219 occupies a cell. In long format, that row simply doesn't exist.

---

## Long to Wide Conversion (Pivot)

Use `CASE WHEN` inside `MAX()` + `GROUP BY`.

### Syntax

```sql
SELECT
    <primary_key>,
    MAX(CASE WHEN attribute_col = 'col_1' THEN value_col ELSE NULL END) AS col_1,
    MAX(CASE WHEN attribute_col = 'col_2' THEN value_col ELSE NULL END) AS col_2,
    MAX(CASE WHEN attribute_col = 'col_3' THEN value_col ELSE NULL END) AS col_3
    -- one CASE per column in the wide table (excluding PK)
FROM long_table
GROUP BY <primary_key>;
```

### Example

```sql
SELECT
    mov_id,
    MAX(CASE WHEN attribute = 'movie_title' THEN value ELSE NULL END) AS movie_title,
    MAX(CASE WHEN attribute = 'genre_1'     THEN value ELSE NULL END) AS genre_1,
    MAX(CASE WHEN attribute = 'genre_2'     THEN value ELSE NULL END) AS genre_2
FROM movie_long
GROUP BY mov_id;
```

**How it works:**
```
For each mov_id group:
  CASE WHEN attribute = 'genre_1' THEN value  →  returns the value only for that attribute row
                                                   NULL for all other attribute rows
  MAX(...)  →  picks the one non-NULL value from the group (ignores NULLs)

Result: one row per mov_id with values spread into columns
```

```
Number of CASE statements = number of columns in wide table - 1 (excluding PK)
```

---

## Wide to Long Conversion (Unpivot)

Use `UNION ALL` — one `SELECT` per column being unpivoted.

### Syntax

```sql
(SELECT pk, 'col_1' AS attribute, col_1 AS value FROM wide_table)
UNION ALL
(SELECT pk, 'col_2' AS attribute, col_2 AS value FROM wide_table)
UNION ALL
(SELECT pk, 'col_N' AS attribute, col_N AS value FROM wide_table);
```

### Example

```sql
(SELECT mov_id, 'movie_title' AS attribute, movie_title AS value FROM movie_wide)
UNION ALL
(SELECT mov_id, 'genre_1'     AS attribute, genre_1     AS value FROM movie_wide)
UNION ALL
(SELECT mov_id, 'genre_2'     AS attribute, genre_2     AS value FROM movie_wide);
```

**How it works:**
```
Each SELECT takes one column and turns it into K rows (K = non-NULL values in that column)
UNION ALL stacks all SELECT results together

Total SELECT statements = N  (where wide table has N+1 columns including PK)
```

**UNION ALL not UNION:**
```
UNION     removes duplicates — could accidentally remove valid duplicate values
UNION ALL keeps all rows     — correct here, we want every row from every SELECT
```

---

## Side-by-side transformation

```
WIDE → LONG (unpivot):   each column becomes rows        UNION ALL of SELECTs
LONG → WIDE (pivot):     each attribute becomes a column  CASE WHEN + MAX + GROUP BY
```

---

## Gotchas

```
1. Long → Wide: use MAX() around CASE, not just CASE alone
   Without MAX(), GROUP BY would not collapse correctly

2. Wide → Long: use UNION ALL not UNION
   UNION deduplicates — may silently drop valid rows with same value

3. Long → Wide: number of CASE statements must exactly match
   the number of non-PK columns in the target wide table

4. Wide → Long: NULL values in wide table become rows with NULL value
   Filter them out if needed: WHERE value IS NOT NULL
   or just accept they won't exist in the long table naturally

5. Long format skips NULLs — storage advantage
   mov_id 219 has no genre_2 → no row exists → no wasted space
```
