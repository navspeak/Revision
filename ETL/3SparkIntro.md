# PySpark Introduction

**Apache Spark** = unified analytics engine for large-scale data processing.
**PySpark** = the Python API for Spark.

```
Apache Spark           →  the engine (written in Scala, runs on JVM)
PySpark                →  Python wrapper that lets you use Spark from Python

Same engine. Different language. Same distributed power.
```

---

## Why Spark Exists

Traditional tools fail at big data:

```
Pandas:        OOM when data > RAM
Single SQL DB: doesn't scale across machines
Hadoop MapReduce: slow (writes to disk between every step)

Spark solves all three:
   ✓ Distributes data across machines (no single-machine limit)
   ✓ Keeps data IN MEMORY between operations (much faster than Hadoop)
   ✓ Provides high-level APIs (DataFrame, SQL, MLlib)
```

Spark is **10-100× faster than Hadoop MapReduce** for many workloads.

---

## Key Features of PySpark

```
✓ DISTRIBUTED DataFrames     →  data spread across cluster, looks like Pandas
✓ HIGH-LEVEL APIs             →  ETL, SQL, streaming, ML
✓ LAZY EVALUATION              →  builds DAG, optimises before executing
✓ FAULT TOLERANCE              →  rebuild lost data via lineage
✓ IN-MEMORY computation        →  cache datasets across operations
✓ INTEGRATION with Hadoop ecosystem (HDFS, Hive, Kafka, etc.)
✓ INTEGRATION with cloud platforms (S3, ADLS, GCS)
```

---

## PySpark vs Pandas

| | Pandas | PySpark |
|-|--------|---------|
| **Data size** | Small to medium (fits in RAM) | Big data (TB+, distributed) |
| **Execution location** | Single machine | Cluster (many machines) |
| **Speed (small data)** | Fast | Slower (cluster overhead) |
| **Speed (big data)** | OOM crash | Scales horizontally |
| **API** | DataFrames | DataFrames + SQL |
| **Lazy evaluation** | No | Yes |
| **Fault tolerance** | No | Yes |
| **Use case** | Local analysis, prototyping | Production ETL, large-scale ML |

**Rule of thumb:** if data fits comfortably in RAM → use Pandas. Otherwise → PySpark.

---

## When to Use PySpark

```
✓ Data volume > single machine's RAM (typically > 100 GB)
✓ Need to process streaming data (Kafka, Kinesis)
✓ Need cluster-level parallelism
✓ Running on Hadoop/cloud infrastructure
✓ ETL pipelines for production
✓ Distributed ML training (MLlib, distributed PyTorch)

✗ Small data (< 10 GB)            → Pandas is faster
✗ Single-machine development      → Pandas is simpler
✗ Highly interactive workflows     → Pandas iterates faster
```

---

## Common Use Cases

```
Log and event analysis
   → terabytes of web/server logs
   → real-time anomaly detection

Transaction analysis
   → bank transactions, e-commerce orders
   → fraud detection, lifetime value

Real-time streaming analytics
   → live dashboards
   → IoT sensor data

Preprocessing for ML pipelines
   → clean, transform, feature engineer at scale
   → feed into distributed ML training

Data warehouse loading
   → daily/hourly ETL from source systems
   → load to Snowflake, Redshift, BigQuery

Data lake processing
   → read raw data from S3
   → transform and write curated layers
```

---

## SparkSession — The Entry Point

Every PySpark program starts by creating a **SparkSession**:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyApp") \
    .getOrCreate()
```

This is the **gateway** to all Spark functionality:
- Create DataFrames
- Run SQL queries
- Access SparkContext (for RDDs)
- Configure cluster settings

```python
sc = spark.sparkContext   # for RDDs (lower-level API)
```

---

## A Minimal PySpark Example

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Demo").getOrCreate()

# Create a DataFrame
data = [("Alice", 29), ("Bob", 35), ("Charlie", 30)]
df = spark.createDataFrame(data, ["Name", "Age"])

# Show it
df.show()
# +-------+---+
# |   Name|Age|
# +-------+---+
# |  Alice| 29|
# |    Bob| 35|
# |Charlie| 30|
# +-------+---+

# Transform and aggregate
df.filter(df.Age > 28) \
  .groupBy() \
  .avg("Age") \
  .show()
```

---

## Spark Architecture in One Picture

```
            ┌──────────────────────────────────────┐
            │      DRIVER PROGRAM (your code)       │
            │      Creates SparkSession             │
            │      Defines transformations           │
            └──────────────┬────────────────────────┘
                           │
                  ┌────────▼────────┐
                  │   SparkContext    │
                  │ (Cluster Manager) │
                  └────────┬─────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
         ┌────▼───┐   ┌────▼───┐   ┌────▼───┐
         │EXECUTOR│   │EXECUTOR│   │EXECUTOR│
         │ Task 1 │   │ Task 2 │   │ Task 3 │
         │ Task 4 │   │ Task 5 │   │ Task 6 │
         └────────┘   └────────┘   └────────┘
            
            Each executor: own JVM, own memory, runs multiple tasks
```

- **Driver** → your program; coordinates the work
- **Cluster Manager** → assigns resources (YARN, Mesos, Kubernetes, or Spark standalone)
- **Executors** → workers that run the actual tasks on data partitions

Covered in detail in `9SparkArchitecture.md`.

---

## Spark APIs

PySpark exposes several APIs:

```
RDD API           →  low-level, original API
                     full control, more verbose
                     covered in 4RDD.md

DataFrame API     →  high-level, like Pandas
                     most common in modern Spark
                     covered in 5DataFrames.md

SQL API           →  write SQL queries against DataFrames
                     spark.sql("SELECT ... FROM ...")

MLlib             →  distributed machine learning
                     classification, regression, clustering

Structured Streaming →  real-time data pipelines
                        same DataFrame API for batch and stream

GraphX            →  graph processing (less commonly used)
```

For ETL work, you'll mostly use **DataFrame API + SQL**.

---

## The Spark Ecosystem

```
Storage:
   HDFS                →  Hadoop Distributed File System
   S3 / ADLS / GCS    →  cloud object stores
   Cassandra           →  NoSQL database
   HBase                →  wide-column store

Compute:
   Apache Spark        →  unified analytics engine
   YARN / Mesos / K8s → cluster managers
   
Streaming:
   Kafka               →  distributed message broker
   Kinesis             →  AWS managed Kafka

Warehouses (load destinations):
   Snowflake, Redshift, BigQuery, Databricks SQL

Orchestration:
   Apache Airflow
   Dagster, Prefect
```

PySpark is **one piece** of this ecosystem — usually the compute layer that reads from storage and writes to warehouses.

---

## Common Pitfalls

```
✗ Using PySpark for small data
   → Pandas would be 10× faster
   → Spark overhead not worth it

✗ Calling .toPandas() on huge DataFrames
   → pulls all data to driver → OOM

✗ Collecting too much to driver
   → .collect() brings everything to one machine
   → use .show() or .take(n) for inspection

✗ Forgetting Spark is lazy
   → "nothing happened" until you call an action

✗ Not understanding partitioning
   → wrong partition count → slow or skewed jobs
```

---

## Summary

```
PySpark = Python API for Apache Spark
        = distributed data processing at scale
        = the de facto choice for big data ETL

Advantages over Pandas:
   ✓ Handles data that doesn't fit in memory
   ✓ Distributes work across many machines
   ✓ Fault-tolerant via RDD lineage
   ✓ Lazy evaluation enables optimisation

When to use:
   ✓ Big data (TB+)
   ✓ Cluster environments
   ✓ Production pipelines
   ✓ Cloud platforms

Entry point: SparkSession.builder.appName(...).getOrCreate()
```

> Spark is the engine. PySpark is your steering wheel. Together they let you process data at scales that single machines couldn't dream of.
