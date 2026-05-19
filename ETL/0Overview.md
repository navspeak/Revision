# ETL with PySpark — Revision

Quick-reference notes summarising **ETL concepts, PySpark/RDD essentials, and common interview topics** — built from `EDA/ETL/M1` lecture notes and hands-on notebooks.

---

## What This Module Covers

```
ETL (Extract, Transform, Load) →  data engineering's core process
PySpark                         →  Python API for Apache Spark
Distributed computing            →  why Spark exists
```

The goal: handle data at **scale** — millions of rows, distributed across clusters, beyond what Pandas can do.

---

## Files

| # | File | Topic |
|---|------|-------|
| 1 | `1ETLBasics.md` | What ETL is, the 3 stages, batch vs streaming |
| 2 | `2Computing.md` | Serial / parallel / distributed / cloud computing |
| 3 | `3SparkIntro.md` | What Spark/PySpark is, why over Pandas, use cases |
| 4 | `4RDD.md` | Resilient Distributed Datasets — Spark's foundation |
| 5 | `5DataFrames.md` | PySpark DataFrames — modern API, operations |
| 6 | `6FileFormats.md` | CSV vs JSON vs Parquet — when to use which |
| 7 | `7DataCleaning.md` | Cleaning operations in PySpark |
| 8 | `8UDF.md` | User Defined Functions — extending PySpark |
| 9 | `9SparkArchitecture.md` | Driver, executors, DAG, lineage, lazy evaluation |
| 10 | `10Optimization.md` | Partitions, caching, broadcast joins, tuning |
| 11 | `11InterviewQuestions.md` | Common ETL / PySpark interview questions with answers |

---

## Key Concepts to Remember

```
ETL              → Extract, Transform, Load
RDD              → Resilient Distributed Dataset (low-level Spark API)
DataFrame        → high-level API on top of RDD
Lazy evaluation  → transformations build a DAG; actions trigger execution
DAG              → Directed Acyclic Graph of operations
Lineage          → recipe to rebuild lost partitions (fault tolerance)
Transformation   → returns a new RDD/DataFrame (lazy)
Action           → triggers execution, returns a value (eager)
Partition        → unit of parallelism in Spark
Executor         → worker process running tasks on cluster nodes
Driver           → program that coordinates the Spark application
```

---

## Quick Comparison

| | Pandas | PySpark |
|-|--------|---------|
| **Data size** | Small to medium (in memory) | Large (distributed) |
| **Execution** | Single machine | Cluster (many nodes) |
| **Lazy evaluation** | No | Yes (builds DAG) |
| **Fault tolerance** | No | Yes (RDD lineage) |
| **Speed (small data)** | Fast | Slower (overhead) |
| **Speed (big data)** | Crashes / OOM | Scales horizontally |
| **API style** | DataFrames | DataFrames (PySpark API) |

---

## Learning Objectives

By the end of this module you should be able to:

- Define ETL and explain its three stages
- Compare full vs incremental extraction, batch vs streaming loading
- Explain why distributed computing is needed and where Spark fits
- Use RDD and DataFrame APIs in PySpark
- Apply cleaning, transformations, joins, aggregations in PySpark
- Understand lazy evaluation, DAG, and lineage
- Optimise PySpark jobs with partitions, caching, broadcast joins
- Answer common ETL/PySpark interview questions
