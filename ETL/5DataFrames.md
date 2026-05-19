# PySpark DataFrames

A **distributed table** with named columns and a schema. The **primary API** for modern Spark.

```
DataFrame = a distributed version of a Pandas DataFrame
          = rows organised into typed columns
          = optimised by Spark's Catalyst engine
          = the de facto API for ETL in Spark
```

If you only learn one Spark API → learn DataFrames.

---

## Why DataFrames Over RDDs?

```
RDD:        you write the code → Spark executes literally
            no optimisation possible

DataFrame:  you describe WHAT you want
            Catalyst optimiser figures out HOW to do it efficiently
            
Result: DataFrames are 2-10× faster than equivalent RDD code.
```

You give up some flexibility (DataFrames need a schema) but gain massive performance.

---

## Creating DataFrames

### From a list of tuples

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

data = [("Alice", 29), ("Bob", 35), ("Charlie", 30)]
df = spark.createDataFrame(data, ["Name", "Age"])
df.show()
```

### From a file

```python
# CSV
df = spark.read.csv("data.csv", header=True, inferSchema=True)

# JSON
df = spark.read.json("data.json")

# Parquet (preferred for performance)
df = spark.read.parquet("data.parquet")
```

### From a Pandas DataFrame

```python
import pandas as pd
pdf = pd.DataFrame({"name": ["A", "B"], "age": [25, 30]})
df = spark.createDataFrame(pdf)
```

Useful when you want to start in Pandas and scale to Spark.

---

## Inspecting Data

```python
df.show(5)              # first 5 rows (printed nicely)
df.show(5, truncate=False)   # don't truncate long strings

df.printSchema()        # column names + types
# root
#  |-- Name: string (nullable = true)
#  |-- Age: long (nullable = true)

df.columns              # ["Name", "Age"]
df.count()              # number of rows
df.dtypes               # [("Name", "string"), ("Age", "bigint")]
df.describe().show()    # summary stats per numeric column
```

`show()` is your `head()`. `printSchema()` is your `dtypes`.

---

## Selecting Columns

```python
df.select("Name")                       # one column
df.select("Name", "Age")                # multiple columns
df.select(df.Name, df.Age + 1)          # expressions

from pyspark.sql.functions import col
df.select(col("Name"), col("Age") * 2)
```

`col()` is the idiomatic way to reference columns in expressions.

---

## Filtering Rows

```python
df.filter(df.Age > 30)
df.filter(col("Age") > 30)
df.filter("Age > 30")                    # SQL-like string

df.where(col("Age").between(25, 35))
df.where(col("Name").startswith("A"))
df.where(col("Name").isin(["Alice", "Bob"]))

# Combine conditions
df.filter((col("Age") > 25) & (col("Age") < 40))
df.filter((col("Age") < 25) | (col("Age") > 40))
```

Use `&`, `|`, `~` (NOT `and`, `or`, `not`) — same as Pandas boolean indexing.

---

## Adding / Renaming / Dropping Columns

```python
# Add a new column
df.withColumn("AgePlus10", col("Age") + 10)
df.withColumn("Adult", col("Age") >= 18)

# Rename a column
df.withColumnRenamed("Name", "FullName")

# Drop columns
df.drop("Age")
df.drop("Age", "Salary")
```

These return NEW DataFrames (immutable).

---

## Casting Types

```python
from pyspark.sql.types import IntegerType, StringType, DoubleType, TimestampType

df.withColumn("Age", col("Age").cast(IntegerType()))
df.withColumn("price", col("price").cast(DoubleType()))
df.withColumn("event_time", col("event_time").cast(TimestampType()))
```

Important for schema enforcement.

---

## Aggregations

```python
df.groupBy("city").count()
df.groupBy("city").agg({"salary": "mean", "age": "max"})

# Or with explicit functions
from pyspark.sql.functions import avg, sum, max, min, count, countDistinct

df.groupBy("city").agg(
    avg("salary").alias("avg_salary"),
    max("salary").alias("max_salary"),
    count("*").alias("num_employees")
)

# Global aggregations (no groupBy)
df.agg(avg("salary"), sum("salary"))
```

---

## Joining DataFrames

```python
# Inner join (default)
df1.join(df2, on="customer_id")

# Specify join type
df1.join(df2, on="customer_id", how="left")
# how options: inner, left, right, outer, semi, anti

# Join on multiple keys
df1.join(df2, on=["customer_id", "order_date"])

# Join on different column names
df1.join(df2, df1.customer_id == df2.cust_id)
```

Joins are expensive in distributed systems — they require shuffling. We'll cover optimisation (broadcast joins) in `10Optimization.md`.

---

## Sorting

```python
df.orderBy("age")                       # ascending
df.orderBy(col("age").desc())            # descending
df.orderBy("city", col("salary").desc())  # multi-column
```

---

## Handling Missing Values

```python
# Drop rows with any NaN
df.na.drop()                             # drop if ANY column has null
df.na.drop(how="all")                    # drop only if ALL columns null
df.na.drop(subset=["salary"])            # only consider "salary"

# Fill missing values
df.na.fill(0)                            # fill numeric nulls with 0
df.na.fill({"salary": 0, "city": "Unknown"})   # column-specific

# Replace values
df.na.replace("N/A", None, "category")    # replace "N/A" with null
```

---

## SQL Mode

PySpark lets you write SQL directly against DataFrames:

```python
# Register DataFrame as a table
df.createOrReplaceTempView("employees")

# Query with SQL
result = spark.sql("""
    SELECT city, AVG(salary) AS avg_salary
    FROM employees
    WHERE age > 25
    GROUP BY city
    ORDER BY avg_salary DESC
""")

result.show()
```

Especially useful if you're comfortable with SQL or migrating SQL queries to Spark.

---

## Writing DataFrames

```python
# CSV
df.write.csv("output.csv", header=True, mode="overwrite")

# Parquet (preferred for performance & schema preservation)
df.write.parquet("output.parquet", mode="overwrite")

# JSON
df.write.json("output.json", mode="overwrite")

# Modes:
# - overwrite: replace existing
# - append: add to existing
# - ignore: do nothing if exists
# - error: fail if exists (default)
```

### Partitioned writes

```python
df.write.partitionBy("year", "month").parquet("output/")
# Creates subdirectories: output/year=2024/month=01/...
```

Faster reads when filtering by partition columns.

---

## DataFrame Operations Are Lazy

Same as RDDs — transformations are lazy, actions trigger execution.

```python
df2 = df.filter(...).select(...).groupBy(...).agg(...)
# NOTHING happens yet!

df2.show()           # ACTION → triggers all the above
df2.count()          # ACTION
df2.write.parquet(...) # ACTION
```

Actions: `.show()`, `.count()`, `.collect()`, `.take()`, `.write.X()`, `.toPandas()`.

---

## Converting Between DataFrame and RDD/Pandas

```python
# DataFrame → RDD
rdd = df.rdd

# RDD → DataFrame
df = rdd.toDF(["name", "age"])

# DataFrame → Pandas (CAREFUL — pulls all data to driver)
pdf = df.toPandas()

# Pandas → DataFrame
df = spark.createDataFrame(pdf)
```

`toPandas()` is convenient for plotting / analysis at the end, but **don't do it on big data** — it brings everything to one machine.

---

## Performance Tips

```
✓ Use Parquet over CSV/JSON (columnar, compressed, schema preserved)
✓ Cache DataFrames you reuse (df.cache())
✓ Use broadcast joins for small tables (more in 10Optimization.md)
✓ Avoid .collect() and .toPandas() on big data
✓ Use .show() for inspection, not .collect()
✓ Filter early (filter before join, not after)
✓ Use built-in functions (faster than UDFs)
✓ Partition appropriately
```

---

## Common Functions

Built-in column functions from `pyspark.sql.functions`:

```python
from pyspark.sql.functions import (
    col, lit, when, expr,                    # column refs and conditionals
    upper, lower, trim, length, substring,   # string ops
    concat, concat_ws, split, regexp_extract,
    to_date, to_timestamp, date_format,      # date ops
    year, month, dayofweek, hour, minute,
    sum, avg, max, min, count, countDistinct, # aggregations
    when, otherwise,                          # case-like logic
    round, abs, sqrt, log, exp,               # math
    explode, array, struct, collect_list      # complex types
)

# Conditional column
df.withColumn("category",
    when(col("price") < 10, "cheap")
    .when(col("price") < 100, "medium")
    .otherwise("expensive")
)

# String cleaning
df.withColumn("name_clean", lower(trim(col("name"))))
```

Always prefer built-in functions over UDFs — they're optimised by Catalyst.

---

## Common Interview Questions

```
Q: DataFrame vs RDD?
A: DataFrame is higher-level, has a schema, optimised by Catalyst.
   Use DataFrames in modern Spark unless you need RDD's flexibility.

Q: Why is Parquet preferred?
A: Columnar storage → can read only needed columns.
   Compressed → smaller files.
   Schema preserved → no inferring on every read.

Q: How does Spark know how to read a CSV?
A: header=True reads first line as column names.
   inferSchema=True scans data to detect types (extra pass).
   Better: specify schema explicitly for production.

Q: When would you use SQL over the DataFrame API?
A: When SQL is more readable for the query.
   When team is more familiar with SQL.
   Both APIs produce identical plans — same performance.
```

---

## Summary

```
DataFrame = distributed table with named columns
          = primary API in modern Spark
          = optimised by Catalyst → faster than RDD

Key operations:
   select        →  pick columns
   filter / where →  filter rows
   withColumn     →  add / replace column
   groupBy + agg →  aggregate
   join          →  combine DataFrames
   orderBy       →  sort

Lazy execution:
   Transformations build a plan.
   Actions trigger execution (.show, .count, .write).

I/O:
   spark.read.parquet(...) / .csv(...) / .json(...)
   df.write.parquet(...) / .csv(...) / .json(...)
```

> DataFrames are 95% of what you'll write in modern PySpark. Master them and you can build production ETL pipelines.
