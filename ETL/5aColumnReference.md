# PySpark — String vs `col()` for Column References

A common source of confusion in PySpark: when do you write `"event_type"` vs `col("event_type")`?

```
"event_type"     →  just a Python STRING — text
col("event_type") →  a COLUMN OBJECT — a piece of a Spark query plan
```

Functions like `trim()`, `lower()`, `upper()` **need a Column object**, not a string. A plain string doesn't carry the metadata Spark needs to build the execution plan.

---

## What Each Thing Actually Is

```python
from pyspark.sql.functions import col

print(type("event_type"))       # <class 'str'>
print(type(col("event_type")))  # <class 'pyspark.sql.column.Column'>
```

```
"event_type":
   → just text. Python doesn't know it's a column.

col("event_type"):
   → a Spark Column EXPRESSION
   → "give me a reference to the column named 'event_type'"
   → carries metadata Spark uses to build the query plan
```

These are **different things**. PySpark functions that build expressions only accept the Column type.

---

## The Failing Example

```python
from pyspark.sql.functions import lower, trim

# ✗ This DOESN'T work as you expect
df.withColumn("event_type", lower(trim("event_type")))
```

This errors out:

```
TypeError: Column is not iterable
```

Because `lower("event_type")` tries to lowercase the literal Python string `"event_type"` → `"event_type"`. That's not what you want — you want to lowercase the **column's values**.

```python
# ✓ Correct — wrap with col()
df.withColumn("event_type", lower(trim(col("event_type"))))
```

---

## Where `"event_type"` (Plain String) DOES Work

Some PySpark methods are smart enough to accept either:

```python
# These BOTH work — strings are interpreted as column names
df.select("event_type")          # ✓
df.select(col("event_type"))     # ✓

df.groupBy("event_type")          # ✓
df.groupBy(col("event_type"))     # ✓

df.orderBy("event_type")          # ✓
df.orderBy(col("event_type"))     # ✓

df.drop("event_type")             # ✓

# First arg of withColumn — column NAME (string is fine)
df.withColumn("event_type", lower(col("event_type")))
#             ^^^^^^^^^^^^^                ^^^^^^^^^^^^^
#             string is OK                Column REQUIRED
```

```
INSIDE EXPRESSIONS (lower, trim, when, isNull, ==, etc.):
   ✓ col("name")
   ✗ "name"  (won't work)

FOR COLUMN NAMES (select, groupBy, drop, withColumn's first arg):
   ✓ "name"  (works fine)
   ✓ col("name")  (also works)
```

---

## The Rule of Thumb

```
"event_type"  is OK when:
   - It's the NAME of a column to select / group / sort by
   - You're labelling, not computing

col("event_type")  is REQUIRED when:
   - You're inside a function that takes a COLUMN EXPRESSION
     (trim, lower, when, isNull, isin, &, |, +, -, *, /, ==, etc.)
   - You're transforming or comparing column values
```

---

## Visual — Where Each Belongs

```python
df.withColumn("event_type",        lower(trim(col("event_type"))))
#             ──────────────         ─────────────────────────────
#             column NAME            column EXPRESSION
#             (string is OK)         (must be a Column object)
```

The first argument **names** the column to create or replace.
The second argument is the **expression** that produces the new values — and expressions must be Column objects.

---

## Why Spark Designed It This Way

```
A plain string  →  has no operations defined on it
                   "event_type" + 1 → makes no sense
                                       (Python TypeError)

A Column object →  has Spark operations defined on it
                   col("event_type") + 1  → "add 1 to every value in the column"
                   col("a") > col("b")    → "compare a > b row-wise"
                   col("a").isNull()      → "where a is null"
```

The `Column` class implements all those operators. Plain strings don't.

---

## Examples Showing Why Column Is Needed

```python
# Boolean condition on a column
df.filter(col("price") > 100)              # ← col() needed
df.filter("price > 100")                   # ← OR use a SQL-string (different syntax)

# Equality comparison
df.where(col("name") == "Alice")           # ← col() needed
df.where("name = 'Alice'")                  # ← SQL-string alternative

# Arithmetic
df.withColumn("total", col("qty") * col("price"))   # ← col() needed
   # "qty" * "price" would just multiply two Python strings (nonsense)

# Calling column methods
df.filter(col("name").isNull())             # ← col() needed
df.filter(col("category").isin(["a", "b"])) # ← col() needed

# Using when().otherwise() for conditionals
from pyspark.sql.functions import when
df.withColumn("tier",
    when(col("salary") > 100000, "high")
    .when(col("salary") > 50000, "medium")
    .otherwise("low")
)
```

In all these cases, you need a Column object so Spark can build the right expression in the plan.

---

## Three Ways to Reference a Column

All produce a Column object:

```python
from pyspark.sql.functions import col

col("event_type")    # explicit — works in any context
df["event_type"]     # dictionary-style — works the same way
df.event_type         # attribute — works but breaks with spaces / reserved words
```

```
col(name):    safest, most explicit, always works
df[name]:     idiomatic, works in expressions
df.name:      works but has edge cases (column names with spaces, hyphens,
              or matching DataFrame methods like .count, .show — avoid)
```

When in doubt, use `col()` — it always works.

---

## The SQL-String Alternative

Spark also accepts SQL-string expressions in some places:

```python
from pyspark.sql.functions import expr

# SQL-string version
df.filter("price > 100")
df.withColumn("upper_name", expr("upper(name)"))
df.withColumn("total", expr("qty * price"))

# Equivalent Column-expression version
df.filter(col("price") > 100)
df.withColumn("upper_name", upper(col("name")))
df.withColumn("total", col("qty") * col("price"))
```

Both produce the same plan. Use whichever reads better. Column expressions get better IDE autocomplete and are easier to refactor; SQL strings are more concise.

---

## Common Gotchas

### Confusing string with Column

```python
# ✗ Trying to use a string in an expression
df.filter("price" > 100)
# Comparing Python string with int → TypeError or weird behaviour

# ✓ Use col()
df.filter(col("price") > 100)

# ✓ Or SQL-string filter (entire expression as string)
df.filter("price > 100")
```

### Forgetting col() with built-in functions

```python
# ✗ lower() gets a string, not a column
df.withColumn("name", lower("name"))   # lowercases the literal "name"

# ✓ lower() gets the column
df.withColumn("name", lower(col("name")))
```

### Modifying in place (DataFrames are immutable)

```python
# ✗ Original df not changed
df.withColumn("new_col", col("a") + col("b"))
# This RETURNS a new DataFrame but you didn't capture it

# ✓ Reassign
df = df.withColumn("new_col", col("a") + col("b"))
```

---

## Aggregation Functions Are Lenient — Accept Either

Functions like `avg`, `sum`, `count`, `max`, `min`, `mean` accept **either a string or a Column**:

```python
from pyspark.sql.functions import avg, sum, count, col

avg("salary")          # ✓ works — string accepted
avg(col("salary"))     # ✓ also works — Column accepted

sum("amount")          # ✓
sum(col("amount"))     # ✓

count("user_id")       # ✓
count(col("user_id"))  # ✓
```

Internally, when you pass a string, PySpark calls `col(name)` for you. Both produce identical execution plans.

### So Why Use One Over the Other?

It's a **style choice**. The shortest valid form is usually idiomatic:

```python
result = (df
    .filter(col("age") > 25)                        # col() because of >
    .groupBy("city")                                  # string OK — just a name
    .agg(avg("salary").alias("avg_salary"))           # string OK — simple agg
    .orderBy(col("avg_salary").desc())                # col() needed for .desc()
)
```

This isn't inconsistent — it's using the **shortest valid form** in each spot.

```
"salary" inside avg()     →  no operation on the column → string works
col("avg_salary").desc()  →  .desc() is a Column METHOD → col() required
col("age") > 25           →  > is a Column OPERATOR → col() required
```

### When `col()` IS Required Even Inside Aggregations

The moment you **operate** on the column before aggregating:

```python
# String alone — can't modify the column
avg("salary")                          # ✓ — straight aggregation

# Need col() because you're DOING something to the column
avg(col("salary") * 1.1)               # ✓ — arithmetic needs col()
sum(when(col("dept") == "eng", col("salary")))   # ✓ — condition needs col()
count(col("status").isNotNull())       # ✓ — method call needs col()
```

```
Rule:
   "name" alone   →  string works in agg functions
   col("name") + operation  →  col() always required
```

### Recommendation

```
Use STRINGS when:
   - just naming a column (groupBy, orderBy, drop, simple agg)

Use col() when:
   - operating on column values (>, <, *, +, etc.)
   - calling Column methods (.alias, .desc, .isin, .isNull)

Mix freely — both are idiomatic PySpark.
```

---

## Mental Model

```
Strings are LABELS (names).
Columns are EXPRESSIONS (operations on data).

Use a string when you're naming a column.
Use a Column when you're computing FROM a column.

   "event_type"        →  the LABEL of a column
   col("event_type")   →  the column itself, ready to be operated on
```

---

## Working Cleaning Example — Annotated

The original snippet, fully decoded:

```python
from pyspark.sql.functions import lower, trim, col

df_cleaned = df.withColumn("event_type",    lower(trim(col("event_type")))) \
               .withColumn("category_code", lower(trim(col("category_code")))) \
               .withColumn("brand",          lower(trim(col("brand"))))
```

Each piece:

```
"event_type" (1st arg of withColumn)  →  STRING, the name of the column to write
col("event_type") (inside lower)      →  COLUMN, the values to operate on
trim(col(...))                        →  Column expression — trimmed values
lower(trim(col(...)))                  →  Column expression — lowercased + trimmed
```

Strings **name** the column. Column objects **describe the computation**.

---

## Quick Reference Table

| Context | Accepts string? | Needs `col()`? |
|---------|-----------------|----------------|
| `df.select("x")` | ✓ | optional |
| `df.groupBy("x")` | ✓ | optional |
| `df.orderBy("x")` | ✓ | optional |
| `df.drop("x")` | ✓ | optional |
| `df.withColumn("x", expr)` | ✓ for name | ✓ for expression |
| `lower(...)`, `upper(...)`, `trim(...)` | ✗ | ✓ |
| `when(condition, value)` | ✗ for condition | ✓ |
| `col("a") + col("b")` | ✗ | ✓ |
| `col("x") > 5` | ✗ | ✓ |
| `col("x").isNull()` | ✗ | ✓ |
| `col("x").isin([...])` | ✗ | ✓ |
| `df.filter("x > 5")` | ✓ (SQL string) | optional |
| `df.filter(col("x") > 5)` | n/a | ✓ |

---

## Summary

```
Two kinds of column reference:

   "event_type"        →  Python string. Used for column NAMES.
   col("event_type")   →  Spark Column object. Used in EXPRESSIONS.

Rules:
   ✓ Use strings for: select, groupBy, orderBy, drop, withColumn's name arg
   ✓ Use col() inside: lower, trim, when, isNull, isin, +, -, *, ==, >, etc.

In short:
   Strings name a column.
   col() lets you OPERATE on a column.
```

> When you're operating on column **values**, you always need `col()` (or an equivalent — `df["x"]`, `df.x`). Strings are for **labels only**.
