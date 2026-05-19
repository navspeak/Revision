# User Defined Functions (UDF)

UDFs let you apply **custom Python logic** to PySpark columns when built-in functions aren't enough.

```
Built-in functions (preferred)  →  fast, optimised by Catalyst
UDF (your custom Python)        →  flexible, but SLOWER (Python ↔ JVM serialisation)
```

**Use built-ins when possible. Use UDFs only when you must.**

---

## When You Need a UDF

```
✗ Standard transformations             →  use built-in functions
✗ String / date manipulation            →  use built-in regexp_*, to_date, etc.
✗ Conditional values                    →  use when().otherwise()

✓ Custom business logic                 →  UDF
✓ Complex multi-step calculations       →  UDF
✓ Integration with Python libraries     →  UDF (NLP libraries, etc.)
```

---

## Defining a Simple UDF

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# Plain Python function
def classify_by_petal_length(petal_length):
    if petal_length < 2.0:
        return "Small"
    elif 2.0 <= petal_length < 5.0:
        return "Medium"
    else:
        return "Large"

# Register as a UDF — specify return type
classify_udf = udf(classify_by_petal_length, StringType())

# Apply to a column
df_classified = df.withColumn(
    "petal_size",
    classify_udf(col("petal_length"))
)
```

**Three steps:**
1. Write a normal Python function
2. Wrap it with `udf()` and declare the return type
3. Use it like any column function

---

## With the @udf Decorator

Cleaner syntax:

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(StringType())
def classify_by_petal_length(petal_length):
    if petal_length < 2.0:
        return "Small"
    elif petal_length < 5.0:
        return "Medium"
    return "Large"

df.withColumn("size", classify_by_petal_length(col("petal_length")))
```

---

## Return Types

PySpark needs to know what type your UDF returns:

```python
from pyspark.sql.types import (
    StringType, IntegerType, DoubleType, BooleanType,
    TimestampType, DateType, ArrayType, MapType, StructType
)

@udf(IntegerType())
def double_age(age):
    return age * 2

@udf(BooleanType())
def is_adult(age):
    return age >= 18

@udf(ArrayType(StringType()))
def split_name(full_name):
    return full_name.split()
```

If you don't specify, PySpark assumes `StringType()`.

---

## UDF with Multiple Columns

```python
@udf(DoubleType())
def compute_total(quantity, unit_price):
    return quantity * unit_price

df.withColumn("total",
    compute_total(col("quantity"), col("unit_price"))
)
```

UDF can take any number of column arguments.

---

## Why UDFs Are Slow

```
Built-in functions:
   - Implemented in Scala/Java
   - Run inside the JVM (where Spark lives)
   - Optimised by Catalyst (vectorised, code-generated)

Python UDFs:
   - For each row, data is serialised from JVM → Python
   - Python computes
   - Result serialised back to JVM
   - SLOW for large data
```

Typical slowdown: **2-10× slower than built-in equivalent**.

---

## Better: Pandas UDFs (Vectorised)

PySpark 2.3+ added **Pandas UDFs** — much faster because they process batches at a time, not row-by-row.

```python
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import IntegerType
import pandas as pd

@pandas_udf(IntegerType())
def double_age(ages: pd.Series) -> pd.Series:
    return ages * 2

df.withColumn("age_doubled", double_age(col("age")))
```

```
Regular UDF:
   row-by-row → serialise each value → Python → serialise back

Pandas UDF:
   batch of rows → entire pandas Series sent at once → process vectorised → return
   → 10-100× faster than regular UDF
```

Use Pandas UDFs when you need custom logic at scale.

---

## Using UDF in SQL

You can register a UDF for SQL queries:

```python
spark.udf.register("classify_petal", classify_by_petal_length, StringType())

# Now usable in SQL
spark.sql("""
    SELECT petal_length, classify_petal(petal_length) AS size
    FROM iris
""").show()
```

Useful for teams that prefer SQL.

---

## Common Pitfalls

### 1. Null handling

```python
@udf(StringType())
def upper_name(name):
    return name.upper()              # CRASHES on null!

# Fix: handle nulls
@udf(StringType())
def upper_name(name):
    return name.upper() if name is not None else None
```

Always check for `None` in your UDF logic.

### 2. Forgetting return type

```python
# WRONG - assumes StringType
@udf
def double(x):
    return x * 2                     # int * 2 = int but returned as STRING

# RIGHT
@udf(IntegerType())
def double(x):
    return x * 2
```

### 3. Performance

```
Bad:
   @udf(StringType())
   def upper_str(s):
       return s.upper()
   df.withColumn("upper", upper_str(col("name")))

Good (built-in):
   from pyspark.sql.functions import upper
   df.withColumn("upper", upper(col("name")))
```

For simple operations, ALWAYS prefer built-in functions.

---

## When NOT to Use UDF — Built-in Alternatives

| Task | UDF (bad) | Built-in (good) |
|------|-----------|-----------------|
| Uppercase string | `udf(lambda s: s.upper())` | `upper(col)` |
| Length | `udf(lambda s: len(s))` | `length(col)` |
| Multiply | `udf(lambda x: x * 2)` | `col * 2` |
| If-then-else | UDF with `if` | `when().otherwise()` |
| Date parsing | UDF with `datetime` | `to_date(col, fmt)` |
| Regex | UDF with `re` | `regexp_extract` / `regexp_replace` |

The built-in alternative is **always faster** — use it when possible.

---

## When UDFs Are Right

```
✓ Business logic that's truly custom
   classify_customer_tier(spend, tenure, support_tickets)

✓ Integration with Python libraries
   sentiment_score(text)  # uses NLP library
   geocode(address)        # uses geocoding API

✓ Complex calculations not expressible as built-ins
   custom risk score, etc.

✓ Bridge to existing Python code
   reusing functions from data science team
```

Use them deliberately, not as a default.

---

## UDF Performance Comparison

For a 1 million row DataFrame:

```
Built-in upper(col):           ~0.3 seconds
Pandas UDF (batched):          ~0.8 seconds
Regular Python UDF:            ~12 seconds  (40× slower)
```

The cost of Python serialisation is real. For big data, **prefer built-ins → pandas UDFs → regular UDFs** in that order.

---

## Complete Example

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType, DoubleType

spark = SparkSession.builder.getOrCreate()

# Sample data
df = spark.createDataFrame(
    [("rose", 4.5), ("daisy", 1.8), ("sunflower", 8.0)],
    ["flower", "petal_length"]
)

# UDF for classification
@udf(StringType())
def classify_size(length):
    if length is None:
        return None
    if length < 2.0:
        return "Small"
    elif length < 5.0:
        return "Medium"
    return "Large"

# UDF for computed feature
@udf(DoubleType())
def normalised_length(length):
    if length is None:
        return None
    return length / 10.0

# Apply
result = df.withColumn("size", classify_size(col("petal_length"))) \
           .withColumn("norm_length", normalised_length(col("petal_length")))

result.show()
# +---------+-------------+------+-----------+
# |   flower|petal_length |  size|norm_length|
# +---------+-------------+------+-----------+
# |    rose|         4.5  |Medium|      0.45 |
# |   daisy|         1.8  | Small|      0.18 |
# |sunflower|        8.0  | Large|      0.80 |
# +---------+-------------+------+-----------+
```

---

## Summary

```
UDF = User Defined Function — apply custom Python to a column

Types:
   @udf(returnType) → regular UDF (slow but simple)
   @pandas_udf(returnType) → vectorised, MUCH faster

When to use:
   ✓ Custom business logic
   ✓ Integration with Python libraries
   ✓ Complex calculations
   
When NOT to use:
   ✗ When built-in function exists (upper, length, regexp_*, etc.)
   ✗ Simple conditionals (use when().otherwise())
   ✗ Arithmetic (use column operators)

Performance:
   Built-in (Catalyst-optimised)  →  fastest
   Pandas UDF (vectorised)         →  fast
   Python UDF (row-by-row)         →  slow
```

> UDFs are an escape hatch for the cases built-ins can't handle. Use them when needed, but always check for a built-in alternative first — it'll be 10× faster.
