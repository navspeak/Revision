# PySpark — DataFrame API vs SQL Form

PySpark gives you **two equivalent ways** to express data transformations:

```
DataFrame API:    df.filter(col("age") > 18).groupBy("city").count()
SQL:              spark.sql("SELECT city, COUNT(*) FROM df WHERE age > 18 GROUP BY city")
```

```
Same execution plan. Same result. Same performance.
Different ergonomics — pick whichever reads better.
```

---

## Quick Glance — Same Query, Two Styles

```python
# DataFrame API
result = (df
    .filter(col("age") > 25)
    .groupBy("city")
    .agg(avg("salary").alias("avg_salary"))
    .orderBy(col("avg_salary").desc())
)

# SQL
result = spark.sql("""
    SELECT city, AVG(salary) AS avg_salary
    FROM employees
    WHERE age > 25
    GROUP BY city
    ORDER BY avg_salary DESC
""")
```

Both produce **identical results** with **identical performance**.

---

## How They Connect — Two Views of the Same Engine

```
                    ┌────────────────────┐
                    │   Your Spark Code   │
                    └──┬──────────────┬───┘
                       │              │
              DataFrame API         SQL
                       │              │
                       └──────┬───────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │  Catalyst Optimiser │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │   Physical Plan     │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │  Execution on JVM   │
                    └────────────────────┘
```

Both APIs **compile to the same plan**. The same Catalyst optimiser handles them.

---

## Setting Up — Register a DataFrame as a SQL Table

To use SQL on a DataFrame, register it as a **temporary view**:

```python
df.createOrReplaceTempView("employees")

# Now you can query it with SQL
result = spark.sql("SELECT * FROM employees WHERE age > 30")
```

```
createOrReplaceTempView    →  view available in this SparkSession only
createGlobalTempView       →  view available across SparkSessions
```

The view is just a label — no data is copied.

---

## Side-by-Side Operations

### SELECT (project columns)

```python
# DataFrame API
df.select("name", "age", "salary")

# SQL
spark.sql("SELECT name, age, salary FROM employees")
```

### FILTER / WHERE

```python
# DataFrame API
df.filter(col("age") > 25)
df.where(col("age") > 25)            # same thing
df.filter("age > 25")                 # SQL string also works

# SQL
spark.sql("SELECT * FROM employees WHERE age > 25")
```

### Combined SELECT + FILTER

```python
# DataFrame API
df.select("name", "salary").filter(col("age") > 25)

# SQL
spark.sql("SELECT name, salary FROM employees WHERE age > 25")
```

### GROUP BY + AGGREGATE

```python
from pyspark.sql.functions import avg, count, max, sum

# DataFrame API
df.groupBy("city").agg(
    avg("salary").alias("avg_salary"),
    count("*").alias("num_employees")
)

# SQL
spark.sql("""
    SELECT city,
           AVG(salary)  AS avg_salary,
           COUNT(*)     AS num_employees
    FROM employees
    GROUP BY city
""")
```

### ORDER BY

```python
# DataFrame API
df.orderBy(col("salary").desc())
df.orderBy("salary", ascending=False)

# SQL
spark.sql("SELECT * FROM employees ORDER BY salary DESC")
```

### LIMIT

```python
# DataFrame API
df.limit(10)

# SQL
spark.sql("SELECT * FROM employees LIMIT 10")
```

### DISTINCT

```python
# DataFrame API
df.distinct()
df.select("city").distinct()

# SQL
spark.sql("SELECT DISTINCT city FROM employees")
```

### JOINS

```python
# DataFrame API
employees.join(departments, on="dept_id", how="inner")
employees.join(departments, employees.dept_id == departments.id, how="left")

# SQL
spark.sql("""
    SELECT e.*, d.dept_name
    FROM employees e
    INNER JOIN departments d ON e.dept_id = d.id
""")
```

### CASE / WHEN

```python
from pyspark.sql.functions import when

# DataFrame API
df.withColumn("tier",
    when(col("salary") > 100000, "high")
    .when(col("salary") > 50000, "medium")
    .otherwise("low")
)

# SQL
spark.sql("""
    SELECT *,
           CASE
               WHEN salary > 100000 THEN 'high'
               WHEN salary >  50000 THEN 'medium'
               ELSE 'low'
           END AS tier
    FROM employees
""")
```

### Window Functions

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, row_number

window = Window.partitionBy("dept").orderBy(col("salary").desc())

# DataFrame API
df.withColumn("rank", rank().over(window))

# SQL
spark.sql("""
    SELECT *,
           RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rank
    FROM employees
""")
```

### UNION

```python
# DataFrame API
df1.union(df2)

# SQL
spark.sql("SELECT * FROM table1 UNION ALL SELECT * FROM table2")
```

### Subqueries

```python
# DataFrame API
high_earners = df.filter(col("salary") > 100000)
result = high_earners.groupBy("city").count()

# SQL (with subquery)
spark.sql("""
    SELECT city, COUNT(*) AS num
    FROM (SELECT * FROM employees WHERE salary > 100000)
    GROUP BY city
""")
```

### COMMON TABLE EXPRESSIONS (CTE)

```python
# DataFrame API — chain DataFrames
high_earners = df.filter(col("salary") > 100000)
result = high_earners.groupBy("city").count()

# SQL — use WITH
spark.sql("""
    WITH high_earners AS (
        SELECT * FROM employees WHERE salary > 100000
    )
    SELECT city, COUNT(*) AS num
    FROM high_earners
    GROUP BY city
""")
```

---

## Full Side-by-Side Comparison Table

| Task | DataFrame API | SQL |
|------|--------------|-----|
| Select columns | `df.select("a", "b")` | `SELECT a, b FROM ...` |
| Filter rows | `df.filter(col("x") > 5)` | `WHERE x > 5` |
| Add column | `df.withColumn("z", expr)` | (in `SELECT`) |
| Drop column | `df.drop("c")` | (omit from `SELECT`) |
| Group + aggregate | `df.groupBy(...).agg(...)` | `GROUP BY ...` |
| Order | `df.orderBy(...)` | `ORDER BY ...` |
| Limit | `df.limit(n)` | `LIMIT n` |
| Distinct | `df.distinct()` | `SELECT DISTINCT ...` |
| Join | `df1.join(df2, on=..., how=...)` | `JOIN ... ON ...` |
| Case | `when(c, v).otherwise(...)` | `CASE WHEN ... END` |
| Window | `.over(Window.partitionBy(...).orderBy(...))` | `OVER (PARTITION BY ... ORDER BY ...)` |
| Union | `df1.union(df2)` | `UNION ALL` |
| Subquery | nested DataFrame variables | `(SELECT ...) AS ...` |
| CTE | nested DataFrame variables | `WITH x AS (SELECT ...)` |

---

## When to Use Which

### Prefer DataFrame API when:

```
✓ Building reusable transformations as Python functions
✓ Composing pipelines step by step
✓ Want IDE autocomplete and type hints
✓ Need conditional logic in transformations (Python if/for)
✓ Prefer Python conventions and refactoring tools
```

```python
# Example — easy to compose programmatically
def filter_active_users(df, min_orders=5):
    return df.filter(col("order_count") >= min_orders)

def add_customer_tier(df):
    return df.withColumn("tier",
        when(col("total_spend") > 10000, "platinum")
        .when(col("total_spend") > 5000, "gold")
        .otherwise("standard")
    )

result = (df
    .pipe(filter_active_users)
    .pipe(add_customer_tier)
    .groupBy("tier").count()
)
```

### Prefer SQL when:

```
✓ Team is more familiar with SQL
✓ Complex query with multiple joins and CTEs
✓ Translating existing SQL queries to Spark
✓ Want a "literate" query that reads top-to-bottom
✓ Need to share with non-Python analysts
✓ Using SQL editor / BI tool integration
```

```sql
-- Example — readable for complex query
WITH active_users AS (
    SELECT user_id, total_spend, order_count
    FROM orders
    WHERE order_count >= 5
),
tiered_users AS (
    SELECT *,
           CASE
               WHEN total_spend > 10000 THEN 'platinum'
               WHEN total_spend >  5000 THEN 'gold'
               ELSE 'standard'
           END AS tier
    FROM active_users
)
SELECT tier, COUNT(*) AS num
FROM tiered_users
GROUP BY tier
```

---

## Mixing Both Styles

You can **freely mix** them in one pipeline:

```python
# Start with DataFrame API
df_clean = (df
    .filter(col("status") == "active")
    .dropna(subset=["email"])
)

# Register and continue with SQL
df_clean.createOrReplaceTempView("active_users")

# Use SQL for a complex window query
result = spark.sql("""
    SELECT user_id,
           RANK() OVER (PARTITION BY country ORDER BY total_spend DESC) AS rank,
           total_spend
    FROM active_users
    WHERE total_spend > 0
""")

# Back to DataFrame API
final = result.filter(col("rank") <= 10)
```

Use whichever is clearer for each step.

---

## Performance Comparison

```
DataFrame API:  → compiles to a logical plan
                → Catalyst optimises
                → generates physical plan

SQL:             → parses to a logical plan
                → Catalyst optimises (SAME optimiser!)
                → generates physical plan
```

**Same optimiser. Same plan. Same speed.** No performance difference between the two styles.

You can verify by comparing `.explain()` output:

```python
df.filter(col("age") > 25).explain()
spark.sql("SELECT * FROM df WHERE age > 25").explain()
# Both show the same physical plan
```

---

## SQL String Inside DataFrame API

You can embed SQL **fragments** inside DataFrame code via `expr()`:

```python
from pyspark.sql.functions import expr

# Without expr — pure DataFrame API
df.withColumn("tier",
    when(col("salary") > 100000, "high")
    .when(col("salary") > 50000, "medium")
    .otherwise("low")
)

# With expr — embed a SQL CASE expression
df.withColumn("tier", expr("""
    CASE
        WHEN salary > 100000 THEN 'high'
        WHEN salary >  50000 THEN 'medium'
        ELSE 'low'
    END
"""))
```

`expr()` accepts any SQL expression string. Useful for complex cases where pure-API is cumbersome.

---

## Common Gotchas

### SQL string filters need different operators

```python
# DataFrame API — Python operators
df.filter(col("name") == "Alice")
df.filter(col("status").isNull())

# SQL string — SQL operators
df.filter("name = 'Alice'")            # = not ==
df.filter("status IS NULL")            # IS NULL not isNull()
```

### Strings need quoting in SQL

```python
df.filter("name = 'Alice'")            # ← string needs quotes
df.filter("age > 25")                  # ← number doesn't
```

### Column aliases

```python
# DataFrame API — use .alias()
df.select(col("salary").alias("annual_pay"))

# SQL — use AS
spark.sql("SELECT salary AS annual_pay FROM employees")
```

### Temp view vs database table

```python
df.createOrReplaceTempView("my_view")
# This is a TEMP VIEW — exists only for this SparkSession.
# It's NOT a database table — it disappears when the session ends.
```

---

## Common SQL Functions in Both APIs

| SQL function | DataFrame API |
|-------------|--------------|
| `UPPER(x)` | `upper(col("x"))` |
| `LOWER(x)` | `lower(col("x"))` |
| `TRIM(x)` | `trim(col("x"))` |
| `LENGTH(x)` | `length(col("x"))` |
| `SUBSTRING(x, start, len)` | `substring(col("x"), start, len)` |
| `COALESCE(x, y)` | `coalesce(col("x"), col("y"))` |
| `CAST(x AS INT)` | `col("x").cast("integer")` |
| `IS NULL` | `col("x").isNull()` |
| `IS NOT NULL` | `col("x").isNotNull()` |
| `IN (1, 2, 3)` | `col("x").isin([1, 2, 3])` |
| `LIKE '%abc%'` | `col("x").like("%abc%")` |
| `NOW()` | `current_timestamp()` |
| `DATE_FORMAT(x, fmt)` | `date_format(col("x"), fmt)` |

Both APIs expose the same underlying functions.

---

## Worked Real-World Example

Task: top 3 highest-paid employees per department.

### DataFrame API

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, col

window = Window.partitionBy("dept").orderBy(col("salary").desc())

result = (df
    .withColumn("rank", rank().over(window))
    .filter(col("rank") <= 3)
    .select("dept", "name", "salary", "rank")
    .orderBy("dept", "rank")
)
```

### SQL

```python
df.createOrReplaceTempView("employees")

result = spark.sql("""
    SELECT dept, name, salary, rank
    FROM (
        SELECT *,
               RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rank
        FROM employees
    )
    WHERE rank <= 3
    ORDER BY dept, rank
""")
```

Both produce identical results. Pick whichever reads better for the team.

---

## Decision Guide

```
Use DataFrame API when:
   ✓ Building programmatic / reusable pipelines
   ✓ Conditional logic in transformations
   ✓ Composing with Python (loops, functions, classes)
   ✓ IDE autocomplete matters
   ✓ Step-by-step debugging
   
Use SQL when:
   ✓ Complex multi-CTE queries
   ✓ Team / stakeholders know SQL better
   ✓ Translating SQL queries from existing systems
   ✓ Want a "complete" query in one block
   ✓ Document-style query that reads like a report

Mix freely:
   ✓ Use whichever is clearest for each step
   ✓ DataFrame API for transformation pipelines
   ✓ SQL for complex analytical queries
```

---

## Summary

```
PySpark = TWO equivalent APIs:

1. DataFrame API (programmatic Python)
   df.filter(col("x") > 5).groupBy("y").count()

2. SQL (declarative query)
   spark.sql("SELECT y, COUNT(*) FROM t WHERE x > 5 GROUP BY y")

Same:
   ✓ Catalyst optimiser
   ✓ Execution engine
   ✓ Performance
   ✓ Result

Different:
   - Ergonomics (Python chaining vs SQL syntax)
   - Familiarity to team
   - Composability vs declarative readability

You can MIX them freely in one program.
Use whichever reads better for each task.
```

> The DataFrame API and SQL form are **two windows into the same engine**. Master both, switch fluidly, and write clearer Spark code.
