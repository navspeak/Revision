# Spark Architecture

Understanding **how Spark runs** is essential for interviews and for writing efficient code.

```
Driver Program  →  coordinates everything
Cluster Manager  →  allocates resources
Executors        →  run the tasks on data
```

Plus: **lazy evaluation**, **DAG**, **stages**, **shuffle**, **lineage**, **fault tolerance**.

---

## The Three Main Components

```
                ┌──────────────────────────────────┐
                │   DRIVER PROGRAM (your code)      │
                │   - SparkSession                  │
                │   - DAG scheduler                 │
                │   - Tracks running stages         │
                └──────────────┬───────────────────┘
                               │
                      ┌────────▼────────┐
                      │ CLUSTER MANAGER │  ← YARN / Mesos / Kubernetes / Standalone
                      │  allocates      │
                      │  resources      │
                      └────────┬────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
         ┌────▼────┐       ┌───▼────┐      ┌───▼────┐
         │EXECUTOR │       │EXECUTOR│      │EXECUTOR│
         │ JVM      │       │ JVM    │      │ JVM    │
         │ tasks    │       │ tasks  │      │ tasks  │
         │ memory   │       │ memory │      │ memory │
         └─────────┘        └────────┘      └────────┘
```

### Driver

```
Your application's main program.
Runs the user code, creates SparkContext, defines transformations,
schedules and tracks the work.

ONE driver per Spark application.
```

### Cluster Manager

```
Allocates resources (CPU, memory) to executors.

Options:
   - Standalone   →  Spark's built-in
   - YARN         →  Hadoop's resource manager
   - Mesos         →  general-purpose cluster manager
   - Kubernetes   →  container orchestration (modern choice)
```

### Executors

```
Worker processes running on cluster nodes.
Each executor has its own JVM and memory.
Runs multiple TASKS in parallel.

MANY executors per application.
```

---

## Tasks, Stages, Jobs

The execution hierarchy:

```
JOB    →  triggered by an action (.count(), .write(), etc.)
   │
   ├── STAGE 1  →  sequence of operations WITHOUT a shuffle
   │   │
   │   ├── TASK 1  →  process one PARTITION of data
   │   ├── TASK 2
   │   └── TASK 3
   │
   ├── STAGE 2  →  starts AFTER a shuffle
   │   │
   │   ├── TASK 1
   │   └── TASK 2
   │
   └── STAGE N  →  more stages...
```

### Definitions

```
Job   = Spark execution triggered by an action
Stage = group of tasks that can run without shuffling data
Task  = unit of work on ONE partition (single thread per task)
```

```
1 action → 1 job → multiple stages → many tasks
```

---

## What Triggers a Stage Boundary?

A **shuffle** — when data needs to move between partitions.

```
NO shuffle (pipelined together in ONE stage):
   map, filter, withColumn, select, cast

YES shuffle (cause stage boundary):
   groupBy, join, distinct, orderBy, repartition, reduceByKey
```

```
df.filter(...).map(...).filter(...).count()
   STAGE 1: filter → map → filter (all pipelined)
   STAGE 2: count
   
df.filter(...).groupBy("key").agg(...).count()
   STAGE 1: filter (pipelined)
   SHUFFLE BOUNDARY (data redistributed by key)
   STAGE 2: groupBy + agg
   STAGE 3: count
```

Each shuffle is **expensive** — moving data across the network.

---

## Lazy Evaluation

Spark **doesn't execute transformations immediately**:

```python
df1 = df.filter(...)        # nothing happens
df2 = df1.select(...)        # nothing happens
df3 = df2.groupBy(...).agg(...)  # nothing happens

df3.show()                   # NOW everything runs
```

### Why Lazy?

```
1. SEE the whole plan before executing
   → optimise it (Catalyst can reorder, combine, prune)

2. PIPELINE multiple operations into one pass
   → avoid intermediate writes

3. PUSH DOWN filters
   → execute filter as early as possible

4. SKIP unnecessary work
   → if a later filter eliminates rows, don't compute earlier transformations on them
```

Without lazy evaluation, Spark couldn't optimise. With it, Spark can make a slow query 10× faster.

---

## DAG (Directed Acyclic Graph)

When you call an action, Spark builds a **DAG** of operations:

```
       parallelize
            │
            ▼
          map
            │
            ▼
         filter
            │
            ▼
       groupByKey
            │
            ▼
          count
```

Then it:
1. **Optimises** the DAG (Catalyst optimiser, code generation)
2. **Splits** into stages (at shuffle boundaries)
3. **Schedules** stages to run in order
4. **Distributes** tasks to executors

This is the **DAG Scheduler** — one of Spark's key components.

---

## Lineage — How Spark Achieves Fault Tolerance

Each DataFrame/RDD remembers how it was produced:

```
final_df = raw_df.filter(...).map(...).groupBy(...).agg(...)

Lineage:
   final_df ← agg ← groupBy ← map ← filter ← raw_df ← spark.read.parquet(...)
```

**If a partition is lost:**

```
1. Spark looks at the lineage
2. Identifies the missing partition's recipe
3. RECOMPUTES only that partition from the source

→ no need for checkpointing or replicas
→ no need for backups
→ Spark "self-heals"
```

This is the **R** in **R**DD — Resilient.

---

## Catalyst Optimizer

The optimiser behind DataFrames:

```
Your query
   ↓
Logical plan (unoptimised)
   ↓
Logical plan (optimised — predicate pushdown, projection pruning, etc.)
   ↓
Physical plan (specific operators chosen)
   ↓
Compiled bytecode (whole-stage code generation)
   ↓
Execution on executors
```

### Common Optimisations

```
✓ Predicate pushdown
   df.join(other).filter(condition)
   → moves filter to BEFORE the join (reduces shuffle)

✓ Projection pruning
   df.select("name", "age").filter(...)
   → reads ONLY name and age columns from Parquet, not all

✓ Constant folding
   df.filter(col("price") > 5 + 3)
   → simplifies to "price > 8"

✓ Join reorder
   chooses optimal join order in multi-table queries
```

You don't see these directly, but they happen automatically. They're why DataFrames are faster than equivalent RDD code.

---

## Inspecting Execution Plans

```python
df.explain()                # physical plan
df.explain(True)             # full: parsed, analyzed, optimised, physical
df.explain("formatted")      # readable formatted version
```

Useful for debugging slow queries — see what Spark actually plans to do.

---

## Spark Memory Model

Each executor has memory divided into:

```
Spark Executor Memory:
   ├── Storage Memory       →  cached RDDs/DataFrames
   ├── Execution Memory     →  shuffles, joins, aggregations
   ├── User Memory          →  UDFs, custom data structures
   └── Reserved Memory       →  Spark internals
```

Storage and Execution share a pool — Spark balances dynamically.

Common config:

```python
spark = SparkSession.builder \
    .config("spark.executor.memory", "8g") \
    .config("spark.executor.cores", "4") \
    .config("spark.executor.instances", "10") \
    .getOrCreate()
```

```
spark.executor.memory     →  memory per executor
spark.executor.cores      →  CPUs per executor
spark.executor.instances  →  number of executors
```

---

## Shuffle — The Expensive Operation

Shuffle = redistributing data across the network.

```
Before shuffle:                  After shuffle:
Partition 1: [A1, B1, C1]         Partition 1: [A1, A2, A3, A4]
Partition 2: [A2, B2, C2]         Partition 2: [B1, B2, B3, B4]
Partition 3: [A3, B3, C3]         Partition 3: [C1, C2, C3, C4]
Partition 4: [A4, B4, C4]
```

Operations that cause shuffle:
- `groupBy` / `reduceByKey`
- `join` (without broadcast)
- `distinct`
- `orderBy`
- `repartition`

Shuffles write data to disk, then read across the network. **Minimise them for performance.**

---

## How Spark Runs Your Code (Full Flow)

```
1. You write Python code → driver creates a DataFrame plan
2. Lazy: nothing happens
3. You call an action (.show, .count, .write)
4. Driver compiles the DAG
5. Catalyst optimises
6. DAG split into stages (at shuffle boundaries)
7. Stages broken into tasks (one per partition)
8. Cluster manager allocates executors
9. Tasks distributed to executors
10. Executors run tasks in parallel
11. Results collected back to driver (or written to storage)
```

This is what `df.show()` triggers behind the scenes.

---

## Fault Tolerance in Action

```
Scenario: executor crashes mid-job

1. Cluster manager notices executor lost
2. Driver receives notification
3. Driver checks LINEAGE of lost partitions
4. Driver tells another executor to recompute the lost partitions
5. Job continues without failure
```

No data corruption, no checkpoint reload, just recomputation from lineage.

---

## Common Interview Questions

```
Q: Walk me through what happens when I call df.show().
A: Triggers an action → builds DAG → optimises via Catalyst →
   splits into stages at shuffles → distributes tasks to executors →
   collects results back to driver.

Q: What is lazy evaluation? Why?
A: Transformations don't execute immediately — they build a plan.
   Allows global optimisation, pipelining, predicate pushdown.

Q: Driver vs executor?
A: Driver = your program, coordinates. Executor = worker, runs tasks.

Q: What is a stage?
A: Group of tasks that can run without shuffling.
   Boundaries occur at shuffles (groupBy, join, etc.).

Q: How does Spark handle node failure?
A: Lineage = recipe of transformations.
   On failure, recompute lost partitions from lineage.
   No need for data replication or checkpoints.

Q: Spark vs Hadoop MapReduce?
A: Hadoop writes to disk between every step → slow.
   Spark keeps data in memory between steps → 10-100× faster.
   Spark also has a richer API and better optimiser.
```

---

## Summary

```
Architecture:
   Driver           →  your program, coordinates
   Cluster Manager  →  allocates resources
   Executors        →  run tasks on partitioned data

Execution hierarchy:
   Job → Stages → Tasks (one per partition)

Stage boundaries: SHUFFLES (groupBy, join, etc.)

Lazy evaluation + DAG + Catalyst:
   - transformations build a plan
   - action triggers execution
   - optimisation happens automatically

Fault tolerance: lineage = recipe to recompute lost partitions.

Spark is fast because of:
   ✓ In-memory computation (vs Hadoop's disk-based MapReduce)
   ✓ Catalyst optimiser
   ✓ Whole-stage code generation
   ✓ DAG scheduling and pipelining
```

> Understanding Spark architecture is the difference between writing code that works and code that scales. Every interview will probe these concepts.
