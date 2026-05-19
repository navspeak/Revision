# RDD — Resilient Distributed Dataset

The **foundational data structure** in Spark. Everything else (DataFrames, Datasets, MLlib) is built on top of RDDs.

```
RDD = an IMMUTABLE, DISTRIBUTED collection of objects
    = your data, split into partitions across the cluster
    = can be processed in parallel
```

You don't use RDDs much in modern Spark code (DataFrames are higher-level and faster), but **understanding RDDs is essential for interviews** and for understanding how Spark works under the hood.

---

## What "RDD" Means

```
Resilient   →  fault-tolerant via LINEAGE (can rebuild lost partitions)
Distributed →  split across multiple machines
Dataset     →  collection of records (objects)
```

Each property is a key feature of Spark.

### Resilient (Fault Tolerance)

```
If a worker machine crashes mid-job:
   Spark KNOWS how to rebuild lost partitions
   from the original data + transformation history

This recipe is called the LINEAGE.
```

You don't need to checkpoint or back up — Spark replays the operations that produced the lost data.

### Distributed (Across Machines)

```
A 100 GB RDD might be split into 100 partitions of 1 GB each.
Each partition lives on a different machine (or multiple).
Operations run in parallel across all partitions.
```

### Dataset (Collection)

```
RDDs can hold ANY Python/Scala objects:
   integers, strings, tuples, custom classes, dictionaries
```

This flexibility (vs DataFrames' fixed schema) is RDD's main strength.

---

## Creating RDDs

Two main ways:

### From a Python collection (parallelise)

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("RDD Demo").getOrCreate()
sc = spark.sparkContext

data = [1, 2, 3, 4, 5, 6]
rdd = sc.parallelize(data)
```

Splits the data across the cluster.

### From a file

```python
rdd = sc.textFile("path/to/file.txt")    # one element per line
rdd = sc.wholeTextFiles("path/")          # entire file content
```

Reads from HDFS, S3, local files, etc.

---

## Transformations vs Actions

The **most important distinction** in Spark:

```
TRANSFORMATIONS:
   - return a NEW RDD
   - LAZY — don't execute immediately
   - just build the DAG (Directed Acyclic Graph) of operations

ACTIONS:
   - return a VALUE to the driver (or write to storage)
   - EAGER — trigger execution of the DAG
   - this is when computation actually happens
```

### Common Transformations

```python
rdd.map(lambda x: x * 2)         # apply function to each element
rdd.filter(lambda x: x > 5)      # keep elements matching condition
rdd.flatMap(lambda x: x.split()) # like map but flatten the output
rdd.distinct()                    # remove duplicates
rdd.union(other_rdd)              # combine two RDDs
rdd.groupBy(lambda x: x % 2)      # group by key function
rdd.reduceByKey(lambda a, b: a+b) # for (key, value) pairs
rdd.sortBy(lambda x: x)           # sort by key function
rdd.sample(False, 0.1)            # take a random sample
```

None of these run until you call an action.

### Common Actions

```python
rdd.collect()              # bring ALL data to driver (careful — OOM risk)
rdd.count()                 # number of elements
rdd.take(5)                 # first 5 elements (sample, no shuffle)
rdd.first()                 # first element
rdd.reduce(lambda a, b: a+b)  # aggregate to a single value
rdd.foreach(print)          # apply function for side effects
rdd.saveAsTextFile("out/")  # write to storage
```

These trigger actual execution.

---

## Worked Example

```python
data = [1, 2, 3, 4, 5, 6]
rdd = sc.parallelize(data)

# Build the DAG (lazy — nothing happens yet)
mapped_rdd = rdd.map(lambda x: x * 2)
filtered_rdd = mapped_rdd.filter(lambda x: x % 2 == 0)

# Trigger execution with an action
result = filtered_rdd.count()
print(result)   # 6
```

```
Step 1: parallelize([1,2,3,4,5,6])
        → RDD partitioned across cluster

Step 2: .map(*2)        → builds DAG: [parallelize → map]
Step 3: .filter(%2==0)  → builds DAG: [parallelize → map → filter]

Step 4: .count()        → ACTION triggers execution
        → results: 2, 4, 6, 8, 10, 12 (all even after ×2)
        → count = 6
```

Until `.count()`, Spark just remembered the operations to perform. The action triggers the whole pipeline.

---

## Why Lazy Evaluation Matters

```
Lazy = optimizer can see the WHOLE plan before executing
     → it can:
        - pipeline operations together
        - skip unnecessary work
        - choose optimal join strategies
        - reorder filters before joins
```

Without lazy evaluation, every step would execute immediately and you'd lose optimisation opportunities.

```python
# This LOOKS like 3 passes over the data...
rdd2 = rdd.filter(...).map(...).filter(...)
result = rdd2.count()

# But Spark does it in ONE PASS (fused operations)
```

---

## RDD Lineage — Fault Tolerance

Each RDD remembers its parent RDDs and how it was derived:

```
rdd1 = parallelize([1, 2, 3, 4])
rdd2 = rdd1.map(lambda x: x * 2)
rdd3 = rdd2.filter(lambda x: x > 4)

Lineage:
   rdd3 ← filter ← rdd2 ← map ← rdd1 ← parallelize(...)
```

If a worker crashes and loses a partition:

```
Spark looks at the lineage
   → recomputes ONLY the lost partition
   → replays: parallelize → map → filter for that partition
```

No data backup needed. **Lineage = the recipe.**

---

## Partitions

Each RDD is split into **partitions** — the unit of parallelism.

```python
rdd = sc.parallelize(data, numSlices=8)    # 8 partitions
rdd.getNumPartitions()                      # 8
```

```
1 partition = 1 task = 1 unit of parallel work
```

```
Too few partitions  → underutilising the cluster, low parallelism
Too many partitions → overhead from task scheduling
Sweet spot         → 2-4× number of cores in cluster
```

Repartitioning:

```python
rdd.repartition(10)    # increase or decrease (uses shuffle — expensive)
rdd.coalesce(4)         # decrease only (no full shuffle — cheaper)
```

---

## Key/Value Pair RDDs

Special operations for `(key, value)` pairs:

```python
pairs = sc.parallelize([("a", 1), ("b", 2), ("a", 3), ("b", 4)])

pairs.reduceByKey(lambda a, b: a + b)
# [("a", 4), ("b", 6)]   ← grouped by key, values summed

pairs.groupByKey()
# [("a", [1, 3]), ("b", [2, 4])]

pairs.sortByKey()
# [("a", 1), ("a", 3), ("b", 2), ("b", 4)]
```

`reduceByKey` is preferred over `groupByKey` — does pre-aggregation per partition, less data shuffled.

---

## Caching / Persistence

If you'll use an RDD multiple times, cache it:

```python
rdd.cache()              # store in memory
rdd.persist()             # storage level configurable (memory/disk/serialised)

rdd.unpersist()           # release the cache
```

Without caching:

```
rdd2 = rdd.map(...).filter(...)
rdd2.count()    # computes from rdd1
rdd2.first()    # RECOMPUTES from rdd1!
```

With caching:

```
rdd2 = rdd.map(...).filter(...).cache()
rdd2.count()    # computes and caches
rdd2.first()    # uses cached result
```

Huge speedup when reusing intermediate data.

---

## DAG — Directed Acyclic Graph

Behind the scenes, Spark builds a **DAG** of transformations:

```
rdd → map → filter → reduceByKey → count

   Stage 1 (no shuffle)            Stage 2 (after shuffle)
   ┌────────────────────────┐     ┌──────────────────────┐
   │ map → filter (pipelined)│ ──► │ reduceByKey         │
   └────────────────────────┘     └──────────────────────┘

When action triggers:
   1. DAG is optimised
   2. Stages identified (split at shuffle boundaries)
   3. Stages executed in order
   4. Within a stage, tasks run in parallel
```

DAG scheduler is one of Spark's key optimisations.

---

## RDD vs DataFrame

| | RDD | DataFrame |
|-|-----|-----------|
| **Level** | Low-level | High-level |
| **Schema** | None (any objects) | Strongly typed columns |
| **Speed** | Slower | Faster (Catalyst optimizer) |
| **API** | Functional (map, filter) | SQL-like (select, where, groupBy) |
| **Use case** | Custom logic, unstructured data | ETL, SQL, structured data |
| **Best for** | Fine-grained control | Most modern Spark code |

**Use DataFrames when you can. Drop down to RDDs when you can't.**

DataFrames are RDDs under the hood, but with extra structure that lets Spark optimise more aggressively.

---

## Common Interview Questions

```
Q: What is an RDD?
A: Resilient Distributed Dataset — Spark's foundational immutable, 
   partitioned, fault-tolerant collection.

Q: Difference between transformation and action?
A: Transformation = lazy, returns new RDD, builds DAG.
   Action = eager, triggers execution, returns value.

Q: What is lineage?
A: Sequence of transformations producing an RDD.
   Used to recompute lost partitions for fault tolerance.

Q: reduceByKey vs groupByKey — which is faster?
A: reduceByKey — pre-aggregates per partition, less data shuffled.

Q: When would you use cache?
A: When the same RDD is computed multiple times. Caches it in memory.

Q: RDD vs DataFrame?
A: RDD: low-level, untyped, flexible.
   DataFrame: high-level, schema, optimised by Catalyst.
   Prefer DataFrames in modern Spark.
```

---

## Summary

```
RDD = Resilient Distributed Dataset
    = immutable, partitioned, fault-tolerant collection

Three properties:
   Resilient → fault tolerance via lineage
   Distributed → across cluster machines
   Dataset → any Python objects

Operations:
   Transformations → lazy, build DAG (map, filter, reduceByKey)
   Actions → eager, trigger execution (count, collect, save)

Lazy evaluation:
   - Operations don't execute until an action
   - Enables global optimisation
   - DAG is built first, then optimised, then run

Modern Spark: prefer DataFrames; use RDDs for low-level control.
```

> RDDs are the foundation of Spark. Modern code uses DataFrames, but every Spark interview will test your understanding of RDDs, lazy evaluation, and lineage.
