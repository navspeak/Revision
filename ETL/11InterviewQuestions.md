# Common ETL / PySpark Interview Questions

The most-asked questions for ETL and PySpark roles, with concise model answers.

---

## ETL Concepts

### Q1. What is ETL and why does it matter?

```
ETL = Extract, Transform, Load.

Foundation of data engineering:
   - Pulls data from sources (databases, APIs, files, streams)
   - Cleans / standardises / enriches it
   - Loads it into a warehouse / lake / database for analytics

Without ETL, data is scattered, inconsistent, unusable for analytics or ML.
```

### Q2. Full extraction vs incremental extraction?

```
Full extraction:
   Re-pull EVERYTHING every time.
   Pro: simple, complete.
   Con: slow, expensive at scale.
   Use: small datasets, initial loads, reference tables.

Incremental extraction:
   Pull only NEW or UPDATED records since last run.
   Pro: efficient, scales.
   Con: more complex (track timestamps or CDC).
   Use: large transactional systems (orders, transactions).

Example:
   Bank transactions table with millions of rows daily
   → incremental: pull only today's records
```

### Q3. Batch vs streaming loading?

```
Batch:
   Periodic loads (hourly, daily).
   Simple, efficient for large volumes.
   Stale data between loads.
   Use: reporting, monthly analytics.

Streaming:
   Real-time as data arrives.
   Fresh, low latency.
   Complex, expensive.
   Use: fraud detection, live dashboards, IoT, trading.

Industries needing streaming:
   - Finance (fraud, trading)
   - Healthcare (patient monitoring)
   - E-commerce (live recommendations)
   - IoT / manufacturing (sensor data)
```

### Q4. ETL vs ELT — what's the difference?

```
ETL: Transform happens BEFORE Load (in the ETL tool).
   Used when target system has limited compute.

ELT: Transform happens AFTER Load (in the target warehouse).
   Modern approach with powerful warehouses (Snowflake, BigQuery).
   Load raw → use SQL to transform in-place.

The line blurs — both achieve the same goal.
```

---

## PySpark Basics

### Q5. Why use PySpark over Pandas?

```
Pandas:
   ✓ Fast for small data (fits in RAM)
   ✗ Crashes on data > RAM
   ✗ Single machine only

PySpark:
   ✓ Distributes data across cluster (any size)
   ✓ Parallel execution across many machines
   ✓ Fault tolerance via RDD lineage
   ✓ In-memory computation (faster than Hadoop)
   ✓ Cloud-native (S3, ADLS, GCS)
   ✗ Overhead for small data (slower than Pandas there)

Rule of thumb:
   < 10 GB → Pandas
   > 10 GB → PySpark
```

### Q6. Spark vs Hadoop MapReduce?

```
Hadoop MapReduce:
   - Disk-based: writes intermediate results to disk between every step
   - Slow for multi-step jobs
   - Verbose Java API

Spark:
   - In-memory: keeps data in RAM between operations
   - 10-100× faster than MapReduce
   - Rich APIs (DataFrame, SQL, MLlib, Streaming)
   - Better fault tolerance (RDD lineage)

Both run on YARN, HDFS, S3.
```

---

## RDD Concepts

### Q7. What is an RDD?

```
RDD = Resilient Distributed Dataset.

   Resilient   → fault-tolerant via LINEAGE (recompute on failure)
   Distributed → split into PARTITIONS across cluster
   Dataset      → IMMUTABLE collection of objects

Spark's foundational data structure.
Modern Spark code uses DataFrames (built on RDDs) but understanding
RDDs is essential.
```

### Q8. Transformation vs Action?

```
Transformation:
   - Returns a NEW RDD/DataFrame
   - LAZY — doesn't execute immediately, just builds the DAG
   - Examples: map, filter, select, groupBy, join

Action:
   - Returns a VALUE to the driver (or writes to storage)
   - EAGER — TRIGGERS execution of the DAG
   - Examples: count, collect, show, take, save, write.parquet

Critical distinction:
   rdd.map(...).filter(...)  → nothing happens yet
   rdd.count()                → NOW everything runs
```

### Q9. What is lazy evaluation? Why does it matter?

```
Lazy evaluation:
   Transformations don't execute immediately.
   Spark builds a PLAN (DAG) instead.
   Action triggers actual computation.

Why it matters:
   ✓ Spark sees the WHOLE plan before executing
   ✓ Can OPTIMISE the plan (predicate pushdown, projection pruning,
      pipelining, join reordering)
   ✓ SKIP unnecessary work
   ✓ Pipeline operations into a single pass

Without lazy: every step executes literally — no global optimisation.
With lazy: Spark is 10× faster on typical workloads.
```

### Q10. What is RDD lineage?

```
Lineage = the SEQUENCE OF TRANSFORMATIONS that produced an RDD.

Each RDD remembers its parent RDDs and how it was derived.

If a partition is lost (worker crash):
   Spark looks at lineage
   → recomputes ONLY the lost partition
   → no data replication, no backup needed

This is how Spark achieves fault tolerance.
```

### Q11. reduceByKey vs groupByKey — which is better?

```
groupByKey:
   - Shuffles ALL values per key to one location
   - Then aggregates
   - Lots of data transferred

reduceByKey:
   - Pre-aggregates LOCALLY in each partition first
   - Then shuffles only the partial aggregates
   - Much less data transferred → much faster

Always prefer reduceByKey when possible.

Example: counting occurrences
   reduceByKey(lambda a, b: a + b)   ← efficient
```

---

## DataFrames

### Q12. RDD vs DataFrame?

```
RDD:
   - Low-level API
   - No schema (any Python objects)
   - You write the code, Spark executes literally
   - More flexible but slower

DataFrame:
   - High-level API (like Pandas)
   - Typed columns with schema
   - Catalyst optimiser rewrites your query
   - 2-10× faster than equivalent RDD code

Modern Spark: use DataFrames unless you need RDD's flexibility.
```

### Q13. What is the Catalyst optimiser?

```
Spark's SQL/DataFrame optimiser.

When you write df.filter(...).join(...).select(...):
   1. Builds a LOGICAL PLAN
   2. Applies optimisation rules:
      - Predicate pushdown (filter before join)
      - Projection pruning (read only needed columns)
      - Constant folding (5+3 → 8)
      - Join reordering
   3. Generates PHYSICAL PLAN (specific operators)
   4. Compiles to optimised bytecode (whole-stage codegen)

You don't write optimisations — Catalyst does it automatically.
This is why DataFrames are faster than RDDs.
```

---

## Spark Architecture

### Q14. Driver vs Executors?

```
Driver:
   - Your application's main process
   - Creates SparkSession, defines transformations
   - Schedules and coordinates work
   - ONE per Spark application

Executors:
   - Worker processes on cluster nodes
   - Run TASKS on data partitions
   - Each has own JVM and memory
   - MANY per application

Cluster manager (YARN/Mesos/K8s) allocates executors.
```

### Q15. Job, Stage, Task — what's the hierarchy?

```
Job   = triggered by ONE action
   │
   ├── Stage 1  = group of tasks WITHOUT a shuffle (pipelined)
   │   ├── Task 1  = process ONE partition
   │   ├── Task 2  = process another partition
   │   └── ...
   │
   ├── Stage 2  = starts AFTER a shuffle
   │   ├── Task 1
   │   └── ...

Stage boundaries: SHUFFLES (groupBy, join, distinct, orderBy, repartition).
```

### Q16. What is a shuffle and why is it expensive?

```
Shuffle = redistributing data across partitions / network.

Triggered by: groupBy, reduceByKey, join, distinct, orderBy.

Why expensive:
   - Data WRITTEN to disk on source executors
   - Data READ across the network by destination executors
   - Serialisation cost
   - Disk I/O cost

Optimisations:
   ✓ Broadcast joins (avoid shuffle)
   ✓ Pre-aggregate before joining
   ✓ reduceByKey (less data shuffled) over groupByKey
```

### Q17. How does Spark handle node failure?

```
Spark uses LINEAGE for fault tolerance.

Each RDD/DataFrame remembers HOW it was created from previous RDDs.

On node failure:
   1. Cluster manager detects failure
   2. Driver checks lineage of lost partitions
   3. Recomputes only the lost partitions on other executors
   4. Job continues

No data replication or checkpointing needed.
```

---

## Optimisation

### Q18. How do you optimise a slow PySpark job?

```
1. CACHE DataFrames used multiple times
2. BROADCAST small tables in joins
3. FILTER EARLY (push filters before joins)
4. Use PARQUET (not CSV/JSON)
5. SELECT only needed columns
6. Use BUILT-IN functions (avoid UDFs)
7. RIGHT-SIZE partitions (2-4× cluster cores)
8. Enable ADAPTIVE QUERY EXECUTION (AQE)
9. Avoid .collect() / .toPandas() on big data
10. Check the SPARK UI to find bottleneck stages
```

### Q19. What is a broadcast join?

```
Broadcast join:
   Send a SMALL DataFrame to EVERY executor.
   Each executor joins it with its local partition of the big DataFrame.
   NO SHUFFLE needed → much faster than sort-merge join.

When to use:
   - One side of join < few hundred MB

Code:
   from pyspark.sql.functions import broadcast
   df_big.join(broadcast(df_small), on="customer_id")

Spark sometimes auto-broadcasts (controlled by autoBroadcastJoinThreshold).
```

### Q20. What is data skew? How to handle?

```
Data skew:
   One partition has WAY more data than others.
   Causes: keys with one dominant value, skewed source data.
   Symptom: one task takes 10× longer → blocks the entire stage.

Fixes:
   - Salt the keys (add random prefix to spread out)
   - Use broadcast join if one side is small
   - Pre-aggregate before joining
   - Enable AQE with skewJoin handling (Spark 3.x):
       spark.sql.adaptive.skewJoin.enabled = true
```

### Q21. cache() vs persist() vs checkpoint()?

```
cache():
   In-memory storage.
   Equivalent to persist(MEMORY_ONLY).
   Lineage preserved (re-derivable if cache lost).

persist(StorageLevel):
   Configurable storage:
      MEMORY_ONLY        →  fast, may OOM
      MEMORY_AND_DISK    →  spill to disk if full
      DISK_ONLY          →  no memory used
      _SER suffix         →  serialised (smaller, slower)

checkpoint():
   Written to RELIABLE storage (S3, HDFS).
   Lineage TRUNCATED.
   Use for long iterative jobs to break lineage chain.
```

### Q22. repartition vs coalesce?

```
repartition(n):
   Increase OR decrease partition count.
   Causes a FULL SHUFFLE (expensive).
   Useful for redistributing skewed data.

coalesce(n):
   Decrease only.
   No FULL shuffle (combines existing partitions).
   Much cheaper.
   Common use: reduce small output files before writing.

Use coalesce when reducing.
Use repartition when redistribution is needed.
```

---

## File Formats

### Q23. Why Parquet over CSV?

```
Parquet advantages:
   ✓ COLUMNAR (read only needed columns) → 10× faster for analytical queries
   ✓ COMPRESSED (5-10× smaller files)
   ✓ SCHEMA EMBEDDED (no inferring on every read)
   ✓ SUPPORTS complex types (arrays, structs, maps)
   ✓ Native partition pruning
   ✓ Standard across Spark, Snowflake, Athena, BigQuery, DuckDB

CSV disadvantages:
   ✗ Row-based (must scan everything)
   ✗ No schema (must infer or guess)
   ✗ Verbose, no compression
   ✗ Slow

Use Parquet for production. CSV only for input/output edges of pipeline.
```

### Q24. What is partition pruning?

```
For partitioned Parquet:
   output/
      year=2024/month=01/...
      year=2024/month=02/...
      year=2023/month=12/...

Query: SELECT * FROM data WHERE year = 2024 AND month = 02

Spark reads ONLY the year=2024/month=02/ directory.
Other partitions are SKIPPED entirely.

Massive speedup for time-series or geographically partitioned data.
```

---

## UDFs

### Q25. When should you use a UDF? When NOT?

```
USE UDF when:
   ✓ Custom business logic (e.g., complex classification)
   ✓ Integration with Python libraries (NLP, geocoding)
   ✓ Logic not expressible as built-in functions

DON'T USE UDF when:
   ✗ Built-in function exists (upper, lower, regexp_*, when, ...)
   ✗ Simple arithmetic (use column operators)
   ✗ Date manipulation (use to_date, date_format, ...)

Why avoid:
   Python UDFs serialise data JVM ↔ Python row-by-row.
   2-10× slower than built-in functions.
   Pandas UDFs (vectorised) are faster but still slower than built-ins.
```

---

## Streaming

### Q26. Batch vs streaming in Spark?

```
Batch (Spark SQL / DataFrames):
   Process a FIXED dataset.
   Read → transform → write → done.

Streaming (Structured Streaming):
   Continuously process arriving data.
   Same DataFrame API.
   Common sources: Kafka, files appearing in directory.
   Common sinks: dashboards, databases, alerting.

Both share the same code patterns — just different "trigger" semantics.
```

---

## Integration

### Q27. How does PySpark integrate with cloud platforms?

```
Storage:
   AWS S3       →  spark.read.parquet("s3://bucket/path/")
   Azure ADLS    →  spark.read.parquet("abfss://...")
   GCP GCS       →  spark.read.parquet("gs://bucket/path/")

Compute managed services:
   AWS EMR       →  Hadoop/Spark clusters
   AWS Glue      →  Serverless Spark (PySpark)
   Databricks    →  Managed Spark + lakehouse (multi-cloud)
   Azure Synapse →  Spark integrated with Azure data services
   GCP Dataproc  →  Managed Hadoop/Spark
   Snowflake     →  Loaded data via Snowpark or external tables

You don't manage clusters — they're provisioned and billed per hour/usage.
```

### Q28. How do you load data from PySpark to a data warehouse?

```
Via JDBC connector:
   df.write \
     .format("jdbc") \
     .option("url", "jdbc:postgresql://...") \
     .option("dbtable", "target_table") \
     .option("user", "...") \
     .option("password", "...") \
     .mode("append") \
     .save()

For Snowflake / Redshift:
   - Native connectors exist
   - Often more efficient: write to S3 first, then COPY INTO warehouse
```

---

## Practical / Code Questions

### Q29. Write code to find the top 10 customers by total spending.

```python
df.groupBy("customer_id") \
  .agg(F.sum("amount").alias("total_spent")) \
  .orderBy(F.col("total_spent").desc()) \
  .limit(10) \
  .show()
```

### Q30. Write code to clean a column with mixed-case strings and replace "N/A" with null.

```python
from pyspark.sql.functions import col, lower, trim, when

df_clean = df.withColumn(
    "category",
    when(
        lower(trim(col("category"))).isin("n/a", "unknown", ""),
        None
    ).otherwise(
        lower(trim(col("category")))
    )
)
```

### Q31. Compare two DataFrames and find rows only in one.

```python
# Rows in df1 NOT in df2
df1.subtract(df2)               # set difference

# Rows in df1 AND df2
df1.intersect(df2)

# Rows in df1 or df2 (no duplicates)
df1.union(df2).distinct()
```

### Q32. Window function example — running total per group.

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import sum

w = Window.partitionBy("customer_id").orderBy("date")

df.withColumn("running_total", sum("amount").over(w)).show()
```

---

## Mental Model Questions

### Q33. Walk me through what happens when I call df.show()

```
1. df.show() is an ACTION → triggers execution
2. Driver compiles the DAG (sequence of transformations)
3. Catalyst optimises the logical plan
4. DAG split into stages at shuffle boundaries
5. Each stage broken into tasks (one per partition)
6. Cluster manager allocates executors
7. Driver sends tasks to executors
8. Executors process partitions in parallel
9. Results collected back to driver
10. Driver formats and prints the first 20 rows
```

### Q34. Why is in-memory computing faster than disk-based?

```
Disk I/O is 100-1000× SLOWER than RAM.

Hadoop MapReduce: writes intermediate results to disk between every step.
   → multi-step jobs read/write disk many times.

Spark: keeps intermediate results in MEMORY between operations.
   → only writes final results.
   → 10-100× faster for multi-step pipelines.

Trade-off: needs enough RAM in cluster.
```

### Q35. Common reasons Spark jobs run slow?

```
1. SHUFFLES — too many groupBy/join causing data movement
2. DATA SKEW — one partition way bigger than others
3. SMALL FILES — many tiny files cause task overhead
4. LARGE BROADCAST — broadcasting a too-big table OOMs
5. UDFs — Python UDFs serialise row-by-row
6. UNUSED CACHING — caching big data that's not reused
7. COLLECT TO DRIVER — bringing too much data home
8. WRONG PARTITION COUNT — too few = underutilised, too many = overhead
9. NO PROJECTION — reading all columns when only few needed
10. CSV/JSON — using slow formats instead of Parquet
```

---

## Quick-Fire Round

```
Q: What is the entry point of a PySpark application?
A: SparkSession.builder.appName(...).getOrCreate()

Q: What does sc.parallelize() do?
A: Creates an RDD from a Python collection, distributed across cluster.

Q: What does df.cache() do?
A: Stores the DataFrame in memory to avoid recomputation.

Q: What is a partition?
A: Unit of parallelism — one task processes one partition.

Q: What does .collect() do?
A: Brings ALL data to the driver — risk of OOM on big data.

Q: How do you read a JSON file in PySpark?
A: spark.read.json("path") — expects one JSON record per line.

Q: How do you save a DataFrame as Parquet?
A: df.write.parquet("path", mode="overwrite")

Q: How to check if Spark is running?
A: spark.sparkContext (returns the SparkContext object)

Q: What's the default storage level for cache()?
A: MEMORY_ONLY (deserialised in memory)

Q: When does Spark execute a transformation?
A: NEVER — only actions trigger execution. Transformations are lazy.
```

---

## Topics That Always Come Up

```
✓ ETL pipeline design (Extract → Transform → Load)
✓ Pandas vs PySpark tradeoffs
✓ Full vs incremental extraction
✓ Batch vs streaming
✓ RDD vs DataFrame
✓ Transformations vs actions
✓ Lazy evaluation and DAG
✓ Lineage and fault tolerance
✓ Shuffle and stage boundaries
✓ Driver / Executor / Cluster manager
✓ Broadcast joins
✓ Caching strategies
✓ Partition tuning
✓ Data skew handling
✓ File format choice (Parquet wins)
✓ UDF performance trap
✓ Catalyst optimiser
```

Master these and you'll handle 90% of PySpark interview questions.

---

## Summary

```
ETL/PySpark interviews test:
   1. ETL concepts (stages, batch vs streaming)
   2. Why PySpark (vs Pandas, vs Hadoop)
   3. RDD foundations (lineage, lazy, transformations vs actions)
   4. DataFrames + SQL
   5. Architecture (driver/executor/DAG/stages)
   6. Optimisation (broadcast, caching, partitioning)
   7. File formats (Parquet for the win)
   8. Practical code (joins, aggregations, window functions)

The pattern: WHAT, WHY, HOW.
```

> Internalise the concepts and the questions become easy. Memorising answers gets you partway — understanding why Spark does what it does gets you the job.
