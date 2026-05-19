# PySpark — `withColumn` in DataFrame API vs SQL

SQL doesn't have a `withColumn` verb — adding/replacing a column happens **inside the SELECT** statement.

```
DataFrame API:  df.withColumn("new_col", expression)
SQL:             SELECT *, expression AS new_col FROM ...
```

Every `withColumn` has a SQL equivalent — it just lives **inside SELECT** instead of being a separate step.

---

## The Basic Pattern

```python
# DataFrame API
df.withColumn("total", col("qty") * col("price"))
```

```sql
-- SQL equivalent
SELECT *, qty * price AS total
FROM orders
```

The `SELECT *` keeps the original columns; `, expression AS new_col` adds the new one.

---

## Side-by-Side — Common Cases

### 1. Add a New Column

```python
# DataFrame API
df.withColumn("total", col("qty") * col("price"))
```

```sql
-- SQL
SELECT *, qty * price AS total FROM orders
```

### 2. Replace an Existing Column

```python
# DataFrame API — same column name replaces it
df.withColumn("price", col("price") * 1.1)
```

```sql
-- SQL — explicitly list each column, replace the one you change
SELECT
    order_id,
    qty,
    price * 1.1 AS price,    -- replaced
    customer
FROM orders
```

In SQL, you have to **list the columns explicitly** when replacing — there's no `*` shortcut for "everything except this column" in standard SQL.

### 3. Conditional Column (CASE)

```python
# DataFrame API
from pyspark.sql.functions import when

df.withColumn("tier",
    when(col("salary") > 100000, "high")
    .when(col("salary") > 50000, "medium")
    .otherwise("low")
)
```

```sql
-- SQL
SELECT *,
       CASE
           WHEN salary > 100000 THEN 'high'
           WHEN salary >  50000 THEN 'medium'
           ELSE 'low'
       END AS tier
FROM employees
```

### 4. String Transformation

```python
# DataFrame API
from pyspark.sql.functions import lower, trim

df.withColumn("email", lower(trim(col("email"))))
```

```sql
-- SQL
SELECT
    order_id,
    name,
    LOWER(TRIM(email)) AS email,   -- replaces email
    age
FROM users
```

### 5. Type Casting

```python
# DataFrame API
df.withColumn("price", col("price").cast("double"))
```

```sql
-- SQL
SELECT
    order_id,
    qty,
    CAST(price AS DOUBLE) AS price,
    customer
FROM orders
```

### 6. Multiple New Columns At Once

```python
# DataFrame API — chain
df = (df
    .withColumn("total", col("qty") * col("price"))
    .withColumn("discount", col("total") * 0.1)
    .withColumn("net", col("total") - col("discount"))
)
```

```sql
-- SQL — all in one SELECT
SELECT *,
       qty * price                          AS total,
       (qty * price) * 0.1                   AS discount,
       (qty * price) - (qty * price * 0.1)   AS net
FROM orders

-- OR cleaner with CTEs:
WITH step1 AS (
    SELECT *, qty * price AS total FROM orders
),
step2 AS (
    SELECT *, total * 0.1 AS discount FROM step1
)
SELECT *, total - discount AS net FROM step2
```

DataFrame chaining is **cleaner for derived columns** that build on each other. SQL needs CTEs or you repeat expressions.

---

## The Key Difference

```
DataFrame API:    withColumn ADDS to the existing DataFrame
                  Original columns kept automatically.
                  
SQL:               SELECT *, expr AS name      → keeps all + adds
                   SELECT col1, col2, expr AS name → only what you list
                   You CONTROL exactly which columns survive.
```

The SQL version is more explicit but more verbose for "just add this column".

---

## When SQL Is Less Convenient

```python
# DataFrame API — add 10 new columns programmatically
for c in cols_to_add:
    df = df.withColumn(c, expr_for(c))
```

In SQL, you'd have to write all 10 expressions in one giant SELECT, or chain CTEs. The DataFrame API is **more programmatic** here.

---

## Replace Column in SQL Without Listing All Others

SQL has no built-in "replace column X, keep all others" syntax. Workarounds:

### Option 1 — List All Columns Explicitly

```sql
SELECT
    order_id,
    qty,
    price * 1.1 AS price,
    customer
FROM orders
```

Tedious for wide tables.

### Option 2 — Use a CTE with a Temporary Name

```sql
WITH updated AS (
    SELECT *, price * 1.1 AS new_price FROM orders
)
SELECT
    order_id, qty, new_price AS price, customer
FROM updated
```

Still verbose.

### Option 3 — `* EXCEPT` (Spark 3.4+ / Databricks SQL)

```sql
SELECT * EXCEPT(price), price * 1.1 AS price
FROM orders
```

`* EXCEPT` removes specific columns from `*` — much cleaner. **Not portable** to all SQL dialects, but works in Spark.

---

## Mixed Approach — DataFrame API for Adding, SQL for Querying

A common production pattern:

```python
# Use DataFrame API to ADD derived columns
df = (df
    .withColumn("year", year(col("date")))
    .withColumn("month", month(col("date")))
    .withColumn("total", col("qty") * col("price"))
)

# Register for SQL
df.createOrReplaceTempView("orders")

# Use SQL for complex querying
result = spark.sql("""
    SELECT year, month,
           SUM(total) AS revenue,
           COUNT(*)   AS num_orders
    FROM orders
    GROUP BY year, month
    ORDER BY year, month
""")
```

```
DataFrame API → cleaner for ADDING columns and feature engineering
SQL           → cleaner for COMPLEX queries and aggregations
```

Mix freely.

---

## Summary Table — `withColumn` ↔ SQL

| Goal | DataFrame API | SQL |
|------|--------------|-----|
| Add a column | `df.withColumn("c", expr)` | `SELECT *, expr AS c FROM ...` |
| Replace a column | `df.withColumn("c", new_expr)` | Re-list columns OR `* EXCEPT(c), new_expr AS c` |
| Add multiple | chain `.withColumn` calls | one big SELECT or CTEs |
| Add conditional | `.withColumn("x", when(...).otherwise(...))` | `CASE WHEN ... END AS x` |
| Cast type | `.withColumn("x", col("x").cast(...))` | `CAST(x AS ...) AS x` |
| String clean | `.withColumn("x", lower(trim(col("x"))))` | `LOWER(TRIM(x)) AS x` |
| Drop & add | `.withColumn(...).drop("old")` | Just omit `old` from `SELECT` |

---

## Common Misconception

```
✗ "SQL doesn't have withColumn so it can't do that"
   → WRONG. SQL just doesn't have it as a SEPARATE STEP.
   → New columns are part of SELECT.

✓ Every withColumn has a SQL equivalent.
   → Just expressed differently — inside SELECT.
```

---

## Quick Mental Model

```
DataFrame's .withColumn = imperative ("DO this transformation")
SQL's SELECT             = declarative ("HERE is the shape I want")

Same end result, different style:
   DataFrame:  step → step → step → final
   SQL:        describe the final state in one expression
```

---

## Worked Comparison

Task: from `orders` table, add `total = qty × price`, classify by size, drop the `qty` column.

### DataFrame API

```python
from pyspark.sql.functions import col, when

result = (df
    .withColumn("total", col("qty") * col("price"))
    .withColumn("size",
        when(col("total") > 1000, "large")
        .when(col("total") > 100, "medium")
        .otherwise("small")
    )
    .drop("qty")
)
```

### SQL

```sql
SELECT
    order_id,
    customer,
    price,
    qty * price AS total,
    CASE
        WHEN qty * price > 1000 THEN 'large'
        WHEN qty * price > 100  THEN 'medium'
        ELSE 'small'
    END AS size
FROM orders
```

Both produce identical results. Notice the DataFrame version can reuse `col("total")` for the next computation, but SQL would need a CTE or repeat the expression.

---

## Summary

```
withColumn in DataFrame API ≡ inline expression in SQL's SELECT.

DataFrame API:
   df.withColumn("new", expression)
   → ADDS new column, KEEPS others

SQL:
   SELECT *, expression AS new FROM tab          → adds while keeping all
   SELECT col1, col2, new_expr AS old_col FROM tab → replace by listing
   SELECT * EXCEPT(old_col), new_expr AS old_col   → Spark/Databricks shortcut
```

> SQL doesn't have a `withColumn` verb because it has `SELECT`. Anything you do with `withColumn` becomes part of the SELECT expression. The DataFrame API just makes it feel like a discrete, step-by-step operation.
