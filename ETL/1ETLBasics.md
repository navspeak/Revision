# ETL Basics

**ETL = Extract, Transform, Load** — the foundational process in data engineering for preparing raw data for analysis.

```
Raw data sources  →  EXTRACT  →  TRANSFORM  →  LOAD  →  Data warehouse / lake
   (messy)                       (clean)                  (ready for analytics)
```

---

## The Three Stages

### 1. Extract — Gather Data from Sources

Pull raw data from where it lives:

```
Structured     →  databases (PostgreSQL, MySQL), data warehouses
Semi-structured →  JSON, XML, log files, APIs
Unstructured    →  text documents, images, audio, video
Streaming       →  Kafka, Kinesis, sensor feeds
```

### 2. Transform — Clean and Reshape

Make raw data usable:

```
Cleaning              →  remove duplicates, fix errors, fill missing
Standardisation        →  uniform formats (dates, currency, casing)
Filtering              →  remove irrelevant rows
Deriving fields         →  Total = Quantity × UnitPrice
Aggregation             →  sum, mean, count per group
Joining                 →  combine multiple sources
```

### 3. Load — Write to Destination

Store the cleaned data:

```
Relational databases  →  PostgreSQL, MySQL
Data warehouses        →  Amazon Redshift, Snowflake, BigQuery
Data lakes             →  AWS S3, Azure Data Lake, GCS
NoSQL                   →  MongoDB, Cassandra
```

---

## Why ETL Matters

```
✓ Consistent, reliable data for decision-making
✓ Single source of truth across the organisation
✓ Supports BI, ML, dashboards, analytics
✓ Critical in regulated industries (healthcare, finance)
```

Without ETL: data is scattered, inconsistent, and unusable.

---

## Types of Extraction

### Full Extraction

```
Pull EVERYTHING from the source, every time.

✓ Simple, ensures completeness
✗ Resource-intensive, slow for large data
```

Use case: small datasets, initial loads, reference tables that rarely change.

### Incremental Extraction

```
Pull only NEW or UPDATED records since last run.

✓ Efficient, scales to large systems
✗ More complex (need to track change timestamps / CDC)
```

Use case: large transactional systems (e-commerce orders, banking transactions).

**Tracking changes:**
- Timestamp column (`updated_at`)
- Change Data Capture (CDC) from database logs
- Sequence IDs

---

## Data Transformation Tasks

| Task | Example |
|------|---------|
| **Cleaning** | Remove duplicates, fix typos, fill missing values |
| **Standardisation** | "USA" / "U.S.A" / "United States" → all to "USA" |
| **Filtering** | Drop rows with invalid status, keep only adult users |
| **Deriving** | `Total = Quantity × UnitPrice` |
| **Aggregation** | Daily sales total per region |
| **Joining** | Combine orders with customer details |

Real-world transformations are usually **many small steps chained together**.

---

## Data Loading Methods

### Batch Loading

```
Load data in PERIODIC chunks (hourly, daily, weekly).

✓ Simple, predictable, efficient for large volumes
✗ Data is stale between loads
```

Use case: nightly reporting, monthly analytics, historical data backfills.

### Streaming Loading

```
Load data in REAL TIME as it arrives.

✓ Fresh data, low latency
✗ More complex infrastructure, harder to debug
```

Use case: fraud detection, live dashboards, IoT sensors, trading systems.

### Append vs Overwrite

```
Append    →  add new records to existing data (history preserved)
Overwrite →  replace entire dataset (only latest snapshot)
```

Choose based on whether history matters.

---

## ETL at Different Scales

| | Pandas | PySpark |
|-|--------|---------|
| **Data size** | Up to a few GB | TB to PB |
| **Compute** | Single machine | Cluster |
| **Use case** | Local analysis, prototyping | Production ETL pipelines |
| **Cloud integration** | Manual | Native (Databricks, EMR) |

You start with Pandas, graduate to PySpark when data grows.

---

## Common Storage Targets

```
Relational DBs (OLTP):
   PostgreSQL, MySQL, Oracle
   → transactional workloads, ACID guarantees

Data Warehouses (OLAP):
   Amazon Redshift, Snowflake, BigQuery
   → analytical queries, columnar storage

Data Lakes:
   AWS S3, Azure Data Lake, Google Cloud Storage
   → raw, semi-structured data at any scale, cheap storage

Lakehouses:
   Databricks Delta, Apache Iceberg, Hudi
   → combines lake flexibility + warehouse performance
```

Modern stack: ingest into a lake, transform with Spark, load curated data into a warehouse.

---

## Modern ETL vs ELT

```
ETL: Extract → Transform → Load
   Transform happens BEFORE loading (in the ETL tool)
   Traditional approach

ELT: Extract → Load → Transform
   Transform happens AFTER loading (in the warehouse)
   Modern approach (with powerful warehouses like Snowflake)
```

The line blurs in modern stacks. Both terms describe the same goal — turning raw data into analytics-ready data.

---

## ETL Tool Landscape

```
Open source:
   Apache Spark (PySpark)
   Apache Airflow (orchestration)
   dbt (in-warehouse transformations)
   Apache NiFi
   Apache Beam

Commercial:
   Informatica
   Talend
   Fivetran (extraction)
   Matillion
   AWS Glue
```

PySpark is one piece of a broader data engineering stack.

---

## Summary

```
ETL = Extract → Transform → Load
   foundation of all data engineering

Extraction:
   Full          → everything every time
   Incremental   → only new / changed records

Transformation:
   Clean, standardise, filter, derive, join, aggregate

Loading:
   Batch    → periodic (daily, hourly)
   Streaming → real-time
   Append vs Overwrite

Scales:
   Pandas     → small/medium data
   PySpark    → large, distributed data
```

> Master ETL and you can move data anywhere, in any shape, at any scale. Every analytics product, dashboard, and ML model starts with an ETL pipeline.
