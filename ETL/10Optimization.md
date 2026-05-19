# PySpark Optimisation

How to make Spark jobs **faster and cheaper**. Core techniques every PySpark engineer must know.

```
The 4 levers of Spark optimisation:
   1. Partitioning   →  parallelism and data layout
   2. Caching         →  avoid recomputation
   3. Joins           →  minimise shuffle (broadcast small tables)
   4. Operations      →  use built-ins, filter early, avoid UDFs
```

---

## 1. Partitioning

Partitions = unit of parallelism. Each partition is processed by ONE task.

```
Too few partitions  →  underutilising cluster (some cores idle)
Too many partitions →  scheduling overhead, small tasks
Sweet spot          →  2-4× number of cores in cluster
```

### Inspect Partitions

```python
df.rdd.getNumPartitions()    # how many partitions?
```

### Change Partition Count

```python
df.repartition(100)           # increase or decrease (full shuffle - expensive)
df.coalesce(10)                # DECREASE only (no full shuffle - cheap)
```

```
repartition:
   - can increase or decrease
   - full shuffle: expensive
   - useful when data is skewed

coalesce:
   - can only DECREASE
   - no full shuffle: cheap
   - useful before writing (reduce small output files)
```

### Partition by Column (Write-Time)

```python
df.write.partitionBy("year", "month").parquet("output/")
# Creates: output/year=2024/month=01/, output/year=2024/month=02/, ...
```

**Benefits:**
- Faster reads when filtering on partition columns (partition pruning)
- Smaller files per partition → easier to manage

### Avoid Data Skew

```
Skew: one partition has WAY more data than others.
   → that one task takes 10× longer → blocks everything

Causes:
   - groupBy on a column with one dominant value
   - join keys with one value much more common
   - skewed data sources

Fixes:
   - Add salt to skewed keys
   - Use broadcast join if one side is small
   - Pre-aggregate before joining
```

---

## 2. Caching / Persistence

If you'll use a DataFrame multiple times, **cache it**:

```python
df.cache()             # store in memory
df.persist()            # configurable: memory, disk, or both

df.count()              # FIRST action — populates cache
df.show()               # subsequent actions use cache → fast

df.unpersist()           # release the cache
```

### When to Cache

```
✓ DataFrame used in multiple downstream queries
✓ Expensive computations you want to reuse
✓ Iterative algorithms (ML training, graph algorithms)

✗ Single-use DataFrames (cache adds overhead for no benefit)
✗ Very large data that doesn't fit in memory
```

### Storage Levels

```python
from pyspark import StorageLevel

df.persist(StorageLevel.MEMORY_ONLY)            # default cache()
df.persist(StorageLevel.MEMORY_AND_DISK)        # spill to disk if needed
df.persist(StorageLevel.MEMORY_ONLY_SER)        # serialised, smaller, slower
df.persist(StorageLevel.DISK_ONLY)              # disk only
```

`MEMORY_AND_DISK` is a safer default — won't OOM if cache is too big.

### Cache vs Checkpoint

```
Cache       →  in-memory, fast, lineage preserved
Checkpoint  →  written to reliable storage (S3, HDFS), lineage TRUNCATED
              → useful for iterative jobs to break long lineages
```

```python
spark.sparkContext.setCheckpointDir("/tmp/checkpoints")
df.checkpoint()
```

---

## 3. Joins — The Most Expensive Operation

Joins typically cause shuffles. Optimising them is critical.

### Default: Shuffle Join (Sort-Merge)

```python
df_big.join(df_other, on="customer_id")
# Both sides shuffled to align partitions by join key
```

```
Both DataFrames are partitioned by the join key
   → expensive shuffle
   → both written to disk and read across network
```

### Broadcast Join — When One Side Is Small

If one DataFrame fits in memory of every executor, **broadcast** it:

```python
from pyspark.sql.functions import broadcast

df_big.join(broadcast(df_small), on="customer_id")
```

```
df_small is SENT TO EVERY EXECUTOR
   → no shuffle of df_big needed
   → much faster

Rule of thumb: broadcast tables < a few hundred MB
```

Spark sometimes auto-broadcasts (controlled by `spark.sql.autoBroadcastJoinThreshold`, default 10MB), but explicit `broadcast()` is more reliable.

### Join Strategy Selection

```python
# Inspect join type chosen
df_big.join(df_small, on="id").explain()
# Look for: BroadcastHashJoin (good) vs SortMergeJoin (default shuffle)
```

### Tips for Joins

```
✓ Broadcast the smaller side if possible
✓ Filter BEFORE joining (reduces data shuffled)
✓ Pre-aggregate before joining
✓ Use the SAME partition count on both sides
✓ Repartition by join key if doing many joins
✗ Don't join on null-heavy or skewed keys without handling
```

---

## 4. Operation-Level Optimisations

### Filter Early

```python
# BAD: filter after expensive join
df1.join(df2, on="id").filter(col("date") > "2024-01-01")

# GOOD: filter before join
df1.filter(col("date") > "2024-01-01").join(df2, on="id")
```

Catalyst will often do this automatically (predicate pushdown), but writing it explicitly is clearer.

### Project Only What You Need

```python
# BAD: read all columns
df = spark.read.parquet("data.parquet")
df.filter(...).count()

# GOOD: select only needed columns
df = spark.read.parquet("data.parquet").select("name", "age", "city")
df.filter(...).count()
```

Saves I/O, memory, and shuffle size. Especially big win with Parquet (columnar).

### Use Built-in Functions, Not UDFs

```python
# BAD: UDF
@udf(StringType())
def upper_str(s):
    return s.upper()

df.withColumn("upper_name", upper_str(col("name")))

# GOOD: built-in
from pyspark.sql.functions import upper
df.withColumn("upper_name", upper(col("name")))   # 10× faster
```

Built-ins are optimised by Catalyst. UDFs (especially Python UDFs) are slow.

### Avoid collect() and toPandas() on Big Data

```python
# DANGEROUS — brings ALL data to driver → OOM
results = df.collect()
pdf = df.toPandas()

# SAFE — inspect or aggregate first
df.show(5)
df.take(100)
df.groupBy("category").count().toPandas()   # aggregate first
```

---

## 5. File Format Choices

Already covered in `6FileFormats.md` — quick recap:

```
Parquet    →  columnar, compressed, schema-embedded → DEFAULT for big data
CSV / JSON →  for input/output edges of pipeline
```

Switching from CSV to Parquet alone can speed up jobs **5-10×**.

---

## 6. Adaptive Query Execution (AQE)

Spark 3.0+ feature: optimises queries **at runtime** based on actual data statistics.

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

AQE can:
- Switch from sort-merge join to broadcast join mid-execution
- Coalesce shuffle partitions dynamically
- Handle skewed data automatically

Enabled by default in Spark 3.2+. **Free performance.**

---

## 7. Memory Tuning

```python
spark = SparkSession.builder \
    .config("spark.executor.memory", "8g") \
    .config("spark.executor.cores", "4") \
    .config("spark.executor.instances", "10") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()
```

```
executor.memory     →  memory per executor (8-16 GB common)
executor.cores       →  CPU cores per executor (4-5 common)
executor.instances   →  number of executors
driver.memory        →  memory for driver (avoid heavy collect())
```

More executors with moderate memory > fewer huge executors (better parallelism, faster recovery).

---

## 8. Inspect with explain()

```python
df.explain()                  # physical plan
df.explain(True)               # full plan (logical + physical)
df.explain("formatted")        # readable
df.explain("cost")              # with cost estimates
```

Look for:
- `BroadcastHashJoin` (good) vs `SortMergeJoin` (default)
- `Exchange` (shuffle — minimise these)
- `Filter` placement (push-down successful?)
- `Scan parquet` (with `PushedFilters` — good)

---

## Real-World Job Tuning Checklist

```
1. Use Parquet (not CSV/JSON) for storage
2. Filter and project early
3. Broadcast small tables in joins
4. Cache DataFrames used multiple times
5. Partition output by frequently-filtered columns
6. Avoid UDFs (use built-ins)
7. Enable AQE (Spark 3.0+)
8. Right-size partitions (2-4× cores)
9. Avoid skew (salt heavy keys if needed)
10. Watch the Spark UI for slow stages
```

---

## The Spark UI

Spark provides a web UI (usually port 4040) showing:

```
Jobs       →  list of all jobs and their durations
Stages     →  stage breakdown, tasks per stage, skew
Storage     →  cached DataFrames and their memory usage
Environment →  configuration
Executors   →  resource utilisation per executor
SQL         →  query plans (for DataFrame operations)
```

**Always check the UI** when debugging slow jobs — it tells you exactly where time is being spent.

---

## Common Interview Questions

```
Q: How do you optimise a slow PySpark job?
A: Cache repeated DataFrames, broadcast small tables in joins,
   filter early, use Parquet, project only needed columns,
   tune partition count.

Q: What is broadcast join and when to use it?
A: Send the small table to every executor (no shuffle).
   Use when one side fits in memory (< few hundred MB).

Q: What is data skew and how to handle it?
A: One partition has way more data than others → slow task blocks job.
   Fixes: salt keys, broadcast join, pre-aggregate, AQE skewJoin.

Q: cache vs persist?
A: cache() = persist(MEMORY_ONLY).
   persist() takes a StorageLevel for fine control.

Q: repartition vs coalesce?
A: repartition: full shuffle, increase or decrease count.
   coalesce: no full shuffle, decrease only (cheaper).

Q: Why prefer built-ins over UDFs?
A: Built-ins run in JVM, optimised by Catalyst.
   Python UDFs serialise data JVM ↔ Python → slow.
```

---

## Summary

```
PySpark optimisation = minimise expensive operations:

1. PARTITIONING
   - Right number of partitions (2-4× cores)
   - Partition output by filter columns
   - Avoid skew

2. CACHING
   - Cache DataFrames used multiple times
   - Use MEMORY_AND_DISK for safety
   - Unpersist when done

3. JOINS
   - BROADCAST small tables (game-changer)
   - Filter before joining
   - Same partition count on both sides

4. OPERATIONS
   - Use built-in functions, not UDFs
   - Filter and project EARLY
   - Avoid collect() / toPandas() on big data

5. FILE FORMAT
   - Parquet > CSV / JSON for performance

6. AQE (Spark 3.0+)
   - Enables runtime optimisation
   - Often free 2-3× speedup
```

> Optimisation is the difference between a job that runs in 30 minutes and one that runs in 3 hours. These techniques apply to nearly every PySpark workload.
