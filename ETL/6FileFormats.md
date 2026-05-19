# File Formats — CSV, JSON, Parquet

Three common formats in data engineering. **Parquet is the modern default for big data.** Know when to use each.

```
CSV     → human-readable, universal, but slow and bloated
JSON    → semi-structured, flexible, common for APIs / logs
Parquet → COLUMNAR, compressed, fast — built for analytics
```

---

## CSV — Comma-Separated Values

```
name,age,city
Alice,29,NYC
Bob,35,LA
```

### Reading

```python
df = spark.read.csv("file.csv", header=True, inferSchema=True)
```

```
header=True        → first line is column names
inferSchema=True   → scan file to detect types (slow, extra pass)
```

### Pros

```
✓ Universal — every tool can read it
✓ Human-readable
✓ Easy to debug
✓ Works with simple text editors
```

### Cons

```
✗ No schema — types must be inferred or guessed
✗ Row-based — must read every row even if you need 1 column
✗ Verbose — no compression by default
✗ No nested types
✗ Date / number formats are ambiguous
✗ Slow for large datasets
```

Use CSV for: small files, data interchange with non-engineers, simple debugging.

---

## JSON — JavaScript Object Notation

```json
{"name": "Alice", "age": 29, "city": "NYC"}
{"name": "Bob", "age": 35, "city": "LA"}
```

### Reading

```python
df = spark.read.json("file.json")
```

By default, Spark expects **one JSON record per line** (JSONL/NDJSON format).

### Pros

```
✓ Supports nested / hierarchical data
✓ Self-describing (keys are visible)
✓ Common for APIs, logs, MongoDB exports
✓ Flexible schema (different records can have different fields)
```

### Cons

```
✗ Verbose — keys repeat for every record
✗ Still text-based — slow vs binary
✗ Schema inference is expensive
✗ Larger file sizes than CSV (often)
```

Use JSON for: log files, API responses, semi-structured event data, MongoDB exports.

---

## Parquet — The Big Data Standard

**Columnar** binary format optimised for analytics. Developed by Twitter + Cloudera, now standard across the ecosystem.

### Reading

```python
df = spark.read.parquet("file.parquet")
```

No `header` or `inferSchema` needed — Parquet **embeds the schema** in the file itself.

### What "Columnar" Means

```
Row-based (CSV, JSON):
   record 1: [name, age, city]
   record 2: [name, age, city]
   record 3: [name, age, city]
   → entire rows stored together

Columnar (Parquet):
   column "name": [Alice, Bob, Carol, ...]
   column "age":  [29, 35, 30, ...]
   column "city": [NYC, LA, NYC, ...]
   → entire columns stored together
```

### Why Columnar Is Faster

```
Analytics queries typically read FEW columns from MANY rows.

CSV:    must read every byte of every row → wasted I/O
Parquet: read only the needed columns → much less I/O
```

For "SELECT name, age FROM big_table" — Parquet skips reading "city" entirely.

### Pros

```
✓ COLUMNAR — read only needed columns
✓ COMPRESSED — typically 5-10× smaller than CSV
✓ EMBEDDED SCHEMA — types preserved, no inference needed
✓ FAST — built for analytical queries
✓ Supports COMPLEX TYPES (arrays, structs, maps)
✓ Supports PARTITIONING (skip files based on directory structure)
✓ Push-down filters (Spark can filter at file level)
✓ Standard across Spark, Hive, Snowflake, Athena, DuckDB
```

### Cons

```
✗ NOT human-readable (binary)
✗ Harder to debug with text tools
✗ Must use a Parquet-aware library
```

**Use Parquet for: nearly all production big data work.** CSV / JSON are for input/output edges of pipelines.

---

## Speed Comparison (Typical)

For a 1 GB dataset:

```
Read time:
   CSV     →  60 seconds  (parse text + infer types)
   JSON    →  90 seconds  (parse + parse keys)
   Parquet →  5 seconds   (binary, schema embedded)

File size (same data):
   CSV     →  1 GB
   JSON    →  1.5 GB  (keys repeated)
   Parquet →  150 MB  (columnar + compressed)

Query "SELECT one_column FROM big_file":
   CSV     →  must read entire file
   Parquet →  reads only that one column → 10× faster
```

10× smaller files + 10× faster reads = huge wins at scale.

---

## Side-by-Side

| | CSV | JSON | Parquet |
|-|-----|------|---------|
| **Format** | Text, row-based | Text, row-based | Binary, columnar |
| **Schema** | None (inferred) | Inferred | EMBEDDED |
| **Compression** | None (built-in) | None (built-in) | Yes (snappy, gzip, etc.) |
| **Nested data** | No | Yes | Yes |
| **Human-readable** | Yes | Yes | No |
| **Read speed** | Slow | Slow | Fast |
| **File size** | Large | Larger | Small |
| **Spark optimisation** | Limited | Limited | Excellent (predicate pushdown) |
| **Use case** | Small files, interchange | API/log data | Production analytics |

---

## Other Big Data Formats

Beyond Parquet, there's also:

```
ORC (Optimised Row Columnar)
   - similar to Parquet, common in Hive
   - slightly different compression strategy

Avro
   - row-based but compact binary
   - excellent for streaming (Kafka)
   - schema evolution support

Delta Lake / Iceberg / Hudi
   - lakehouse formats built ON TOP OF Parquet
   - add ACID transactions, time travel, schema evolution
```

For batch ETL: **Parquet**.
For streaming: **Avro** is common.
For modern lakehouses: **Delta / Iceberg** (which use Parquet under the hood).

---

## Reading Schemas

```python
df.printSchema()
# root
#  |-- name: string (nullable = true)
#  |-- age: long (nullable = true)
#  |-- city: string (nullable = true)
```

For Parquet, the schema is read from the file metadata. For CSV/JSON, Spark either:
- Infers it (scan extra pass)
- Or uses one you provide explicitly

### Explicit schema for CSV (faster, safer)

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("name", StringType()),
    StructField("age", IntegerType()),
    StructField("city", StringType())
])

df = spark.read.csv("file.csv", header=True, schema=schema)
```

Avoid `inferSchema=True` in production — it requires an extra full file scan.

---

## Converting Between Formats

A common ETL task — read messy CSV/JSON, write clean Parquet:

```python
# Read raw CSV (slow but simple format)
df = spark.read.csv("raw.csv", header=True, inferSchema=True)

# ... clean / transform ...

# Write Parquet (fast, compressed, schema-preserved)
df.write.parquet("output/", mode="overwrite")
```

This is the standard pattern: **CSV / JSON in → Parquet out**.

---

## Partitioned Parquet

For really big datasets, partition by a column:

```python
df.write.partitionBy("year", "month").parquet("output/")

# Creates directory structure:
# output/year=2024/month=01/part-xxxxx.parquet
# output/year=2024/month=02/part-xxxxx.parquet
# ...
```

When reading:

```python
df = spark.read.parquet("output/")
df.filter(col("year") == 2024).show()
# Spark reads ONLY the year=2024 directories — massive speedup
```

This is called **partition pruning** — one of Parquet's biggest performance wins.

---

## Code Example — Reading Multiple Formats

```python
from pyspark.sql import SparkSession
import time

spark = SparkSession.builder.appName("FileTypeComparison").getOrCreate()

# CSV
csv_df = spark.read.option("header", "true").csv("Iris.csv")
csv_df.printSchema()

# JSON
json_df = spark.read.json("Iris.json")
json_df.printSchema()

# Parquet
parquet_df = spark.read.parquet("Iris.parquet")
parquet_df.printSchema()

# Time the reads
for fmt, path in [("CSV", "Iris.csv"), ("JSON", "Iris.json"), ("Parquet", "Iris.parquet")]:
    start = time.time()
    if fmt == "CSV":
        spark.read.option("header", "true").csv(path).count()
    elif fmt == "JSON":
        spark.read.json(path).count()
    else:
        spark.read.parquet(path).count()
    print(f"{fmt}: {time.time() - start:.2f}s")
```

For small files, the difference is small. For GB-scale data, Parquet wins easily.

---

## Common Interview Questions

```
Q: Why prefer Parquet over CSV?
A: Columnar storage + compression + embedded schema =
   smaller files, faster reads, especially for analytics queries.

Q: What does "columnar" mean and why does it help?
A: Data stored column-by-column, not row-by-row.
   Queries that read few columns from many rows are 10× faster.

Q: How does partition pruning work?
A: Parquet files in directories named "key=value".
   Spark uses filter to skip directories that don't match.

Q: When should you use inferSchema=True?
A: Almost never in production — it requires an extra scan.
   Better: define explicit schema, or use Parquet (schema embedded).
```

---

## Summary

```
CSV     →  text, row-based, universal, slow for big data
JSON    →  text, row-based, handles nesting, common for APIs
Parquet →  BINARY, COLUMNAR, COMPRESSED, SCHEMA-EMBEDDED
          → 10× smaller, 10× faster, standard for production

Rule:
   Edges of pipeline (input/output) → CSV / JSON if needed
   Inside the pipeline                → Parquet always
```

> Parquet is the format of big data. Master it and you'll write faster, cheaper, more reliable pipelines.
