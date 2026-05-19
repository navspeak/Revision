# Data Cleaning in PySpark

Real data is messy — duplicates, NULLs, "N/A" strings, inconsistent casing, wrong types. PySpark provides robust tools to clean it before transformations.

```
Clean data pipeline:
   Raw input → CASING/TRIM → NULLs → TYPE CASTS → VALIDATION → Clean output
```

---

## Standard Cleaning Steps

```
1. Standardise text (trim whitespace, lowercase)
2. Replace placeholder values (e.g., "N/A", "unknown") with null
3. Handle nulls (fill or drop)
4. Cast types correctly
5. Remove duplicates
6. Validate ranges and constraints
```

Each step builds on the previous.

---

## Trimming and Casing

```python
from pyspark.sql.functions import lower, upper, trim, col

# Trim whitespace, lowercase
df_cleaned = df.withColumn("event_type", lower(trim(col("event_type")))) \
               .withColumn("category_code", lower(trim(col("category_code")))) \
               .withColumn("brand", lower(trim(col("brand"))))
```

```
Before:  "  Apple iPhone "   "APPLE"   "apple "
After:   "apple iphone"      "apple"   "apple"
```

Always trim + standardise case early — prevents joins from missing matches due to whitespace or case differences.

---

## Replacing Placeholder Values with NULL

Real-world data often uses strings like "N/A", "unknown", "-", "null", "" instead of true nulls:

```python
from pyspark.sql.functions import when

for col_name in ["category_code", "brand"]:
    df_cleaned = df_cleaned.withColumn(
        col_name,
        when(col(col_name).isin("N/A", "unknown", ""), None).otherwise(col(col_name))
    )
```

Now `null` is a true null — recognised by `isNull()`, `na.fill()`, etc.

---

## Filling Missing Values

```python
# Fill ALL nulls in numeric columns with 0
df.na.fill(0)

# Column-specific fills
df.na.fill({
    "salary": 0,
    "city": "Unknown",
    "brand": "no_brand"
})

# Fill with statistics
mean_age = df.agg({"age": "mean"}).first()[0]
df.na.fill({"age": mean_age})
```

---

## Dropping Missing Values

```python
df.na.drop()                             # drop rows with ANY null
df.na.drop(how="all")                    # drop rows where ALL are null
df.na.drop(subset=["salary", "age"])     # drop if these specific cols are null
df.na.drop(thresh=3)                     # keep rows with at least 3 non-null values
```

Use `drop` when missing rows can't be filled meaningfully.

---

## Type Casting

```python
from pyspark.sql.types import TimestampType, DoubleType, IntegerType

df_typed = df_filled.withColumn("event_time", col("event_time").cast(TimestampType())) \
                    .withColumn("price", col("price").cast(DoubleType())) \
                    .withColumn("user_id", col("user_id").cast(IntegerType()))

df_typed.printSchema()
```

```
Common casts:
   StringType    →  IntegerType / DoubleType  for numeric strings
   StringType    →  TimestampType / DateType   for date strings
   IntegerType    →  StringType                  for IDs that shouldn't be numeric
```

Always cast types explicitly — relying on `inferSchema` is brittle.

### When Cast Fails

```python
# If "price" has non-numeric values like "free", they become NULL after cast
df.withColumn("price", col("price").cast(DoubleType()))
# "free" → null
```

Cast errors silently produce nulls — check with `df.filter(col("price").isNull())`.

---

## Removing Duplicates

```python
# Drop exact duplicates across all columns
df.dropDuplicates()

# Drop duplicates based on subset of columns
df.dropDuplicates(["customer_id", "order_date"])

# Equivalent
df.distinct()                # drops exact full-row duplicates only
```

`dropDuplicates(subset)` is more flexible — useful for "one row per customer".

---

## Conditional Column Modification

The `when().otherwise()` pattern for case-like logic:

```python
from pyspark.sql.functions import when

df.withColumn("price_bracket",
    when(col("price") < 10, "cheap")
    .when(col("price") < 100, "medium")
    .when(col("price") < 1000, "expensive")
    .otherwise("luxury")
)
```

Chain `.when()` calls and end with `.otherwise()` for the default.

---

## String Cleaning Functions

```python
from pyspark.sql.functions import (
    upper, lower, trim, ltrim, rtrim,
    length, substring,
    concat, concat_ws, split,
    regexp_extract, regexp_replace
)

# Length
df.withColumn("name_len", length(col("name")))

# Substring
df.withColumn("first3", substring(col("name"), 1, 3))   # 1-indexed in Spark!

# Concatenate
df.withColumn("full_name", concat(col("first"), lit(" "), col("last")))
df.withColumn("address", concat_ws(", ", col("street"), col("city"), col("zip")))

# Split (returns array)
df.withColumn("words", split(col("description"), " "))

# Regex extract / replace
df.withColumn("year", regexp_extract(col("date_str"), r"(\d{4})", 1))
df.withColumn("clean_phone", regexp_replace(col("phone"), r"[^0-9]", ""))
```

---

## Date / Timestamp Functions

```python
from pyspark.sql.functions import (
    to_date, to_timestamp, date_format,
    year, month, dayofweek, dayofmonth, hour, minute,
    current_date, current_timestamp,
    datediff, date_add, date_sub, months_between
)

# Parse string to date
df.withColumn("date", to_date(col("date_str"), "yyyy-MM-dd"))

# Extract parts
df.withColumn("year", year(col("event_time")))
df.withColumn("month", month(col("event_time")))
df.withColumn("hour", hour(col("event_time")))

# Format
df.withColumn("date_fmt", date_format(col("event_time"), "yyyy-MM-dd HH:mm"))

# Date arithmetic
df.withColumn("days_since", datediff(current_date(), col("event_date")))
df.withColumn("next_week", date_add(col("event_date"), 7))
```

---

## Detecting Outliers

Simple approach using percentiles:

```python
from pyspark.sql.functions import expr

# Compute Q1 and Q3
quantiles = df.approxQuantile("price", [0.25, 0.75], 0.01)
Q1, Q3 = quantiles
IQR = Q3 - Q1

# Filter out outliers
df_clean = df.filter(
    (col("price") >= Q1 - 1.5 * IQR) & (col("price") <= Q3 + 1.5 * IQR)
)
```

`approxQuantile` is fast — doesn't require a full sort.

---

## Filtering

```python
# Range filters
df.filter((col("age") >= 18) & (col("age") <= 65))
df.filter(col("salary").between(40000, 100000))

# String filters
df.filter(col("email").contains("@"))
df.filter(col("name").startswith("A"))
df.filter(~col("status").isin(["banned", "deleted"]))   # NOT in

# Null filters
df.filter(col("email").isNotNull())
df.filter(col("email").isNull())
```

Filters can be chained — Spark optimises into a single predicate.

---

## Complete Cleaning Pipeline Example

```python
from pyspark.sql.functions import lower, trim, col, when
from pyspark.sql.types import TimestampType, DoubleType

# Start with raw data
df_raw = spark.read.csv("data.csv", header=True, inferSchema=True)

# 1. Trim + lowercase strings
df = df_raw.withColumn("event_type", lower(trim(col("event_type")))) \
           .withColumn("brand", lower(trim(col("brand"))))

# 2. Replace placeholders with null
for c in ["category_code", "brand"]:
    df = df.withColumn(c, when(col(c).isin("N/A", "unknown", ""), None).otherwise(col(c)))

# 3. Fill missing values
df = df.na.fill({"price": 0, "brand": "no_brand"})

# 4. Cast types
df = df.withColumn("event_time", col("event_time").cast(TimestampType())) \
       .withColumn("price", col("price").cast(DoubleType()))

# 5. Remove duplicates
df = df.dropDuplicates(["user_id", "event_time", "event_type"])

# 6. Filter invalid records
df = df.filter(col("price") >= 0)

# 7. Cache (will use multiple times downstream)
df.cache()

# 8. Inspect
df.printSchema()
df.show(5)
```

---

## When to Convert to Pandas for Analysis

For VISUALISATION or DEEP analysis, convert a SAMPLE or AGGREGATED result to Pandas:

```python
# Aggregate first to reduce data size
summary = df.groupBy("category").agg(
    avg("price").alias("avg_price"),
    count("*").alias("count")
)

# Convert summary (small) to Pandas
pdf = summary.toPandas()

# Now plot with seaborn / matplotlib
import seaborn as sns
sns.barplot(data=pdf, x="category", y="avg_price")
```

**NEVER `.toPandas()` on the full big dataset** — it pulls everything to the driver.

---

## Common Mistakes

```
✗ Forgetting to trim strings before deduplication
   "  alice  " and "alice" are different → use trim

✗ Filtering after a join
   filter BEFORE joining — much faster

✗ Not handling type cast failures
   "price" = "free" silently becomes null
   → validate after casting

✗ Using udf when built-in function exists
   built-ins are much faster (optimised by Catalyst)

✗ Calling .collect() on big data
   → OOM on driver

✗ Not caching reused DataFrames
   → recomputed every time downstream
```

---

## Summary

```
PySpark cleaning toolkit:

String standardisation:
   lower(), upper(), trim(), regexp_replace()

Null handling:
   when().otherwise() to convert placeholders → null
   df.na.fill(value) or {col: value}
   df.na.drop(subset=[...])

Type casting:
   col("x").cast(IntegerType / DoubleType / TimestampType / ...)

Duplicate removal:
   df.dropDuplicates(subset=[...])

Filtering:
   df.filter(col("x") > 0)
   df.filter(col("status").isin([...]))

Conditional logic:
   when(condition, value).when(...).otherwise(default)

Always cache cleaned dataset if used multiple times: df.cache()
```

> Clean data is the bedrock of any pipeline. The same cleaning patterns repeat across projects — master them and you can handle any dataset.
