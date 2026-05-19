# Types of Computing

PySpark exists because **distributed computing** became necessary. To understand why, you need to know how computing evolved.

```
Serial       →  one task at a time
Parallel     →  many tasks at once on ONE machine
Distributed  →  many tasks across MANY machines
Grid         →  geographically dispersed distributed systems
Cloud        →  on-demand computing as a service
```

---

## Serial Computing

```
Tasks execute ONE AT A TIME, sequentially.
   Task 1 → Task 2 → Task 3 → ...
```

Simple but slow for large workloads. Limited by single CPU speed.

```
✓ Easy to reason about
✗ Doesn't scale — hits CPU ceiling
✗ Can't handle big data
```

---

## Parallel Computing

```
Split tasks into subtasks → run them SIMULTANEOUSLY on multiple cores.
   
   Task → [Subtask 1] → Core 1
        → [Subtask 2] → Core 2
        → [Subtask 3] → Core 3
        → [Subtask 4] → Core 4
```

All on **one machine** with multiple CPU cores or GPUs.

```
✓ Faster than serial
✓ Uses modern multi-core hardware
✗ Still limited by ONE machine's resources
✗ Memory shared → bottleneck
```

Example: NumPy uses parallel computing internally via BLAS/LAPACK.

---

## Distributed Computing

```
Split workload across MANY MACHINES connected over a network.

   Big task → [Subtask 1] → Machine 1
           → [Subtask 2] → Machine 2
           → [Subtask 3] → Machine 3
           → [Subtask 4] → Machine 4
   
   Each machine has its own CPU, memory, storage.
```

**This is what Spark does.** Designed for petabyte-scale data that no single machine can hold.

```
✓ Scales horizontally — add more machines
✓ Handles petabytes of data
✓ Fault-tolerant — survives machine failures
✗ Network overhead
✗ Complex programming model
```

---

## Grid Computing

```
Like distributed computing, but machines are GEOGRAPHICALLY DISPERSED.
Often shared/donated resources, not dedicated clusters.
```

Example: SETI@home, BOINC.

```
✓ Massive scale, low cost (volunteer compute)
✗ High latency, unreliable machines
```

Different from Spark — Spark assumes a dedicated cluster with fast network.

---

## Cloud Computing

```
On-demand computing resources delivered over the internet.

   You don't OWN the machines.
   You RENT them by the hour/minute/second.
```

Providers: **AWS, Azure, GCP, IBM Cloud**.

```
✓ Pay only for what you use
✓ Scale up/down on demand
✓ No hardware management
✓ Global reach (multiple regions)
✗ Vendor lock-in concerns
✗ Network costs can add up
```

Modern Spark runs on cloud platforms (Databricks, EMR, Dataproc, Synapse).

---

## How They Connect

```
Serial   →  ONE core, ONE task at a time
Parallel →  MANY cores, ONE machine
Distributed → MANY machines, coordinated work
Cloud    →  RENT the distributed infrastructure
```

PySpark + Cloud = the modern data engineering stack.

---

## Historical Evolution

```
1950s-60s:  Batch processing
            Punch cards, sequential execution

1960s-70s:  Time-sharing
            Multiple users on one mainframe in real-time

1970s-80s:  Mini-computers, workstations
            Distributed across departments

1980s-90s:  Networking + parallel computing
            Beowulf clusters, grid computing

2000s:      Big data era
            Hadoop, MapReduce, distributed storage

2010s:      Spark + Cloud
            In-memory distributed computing, managed services

2020s:      Serverless + lakehouses
            Even more abstracted infrastructure
```

Each era built on the previous.

---

## Processor Types

Different processors for different workloads:

| Processor | Strength | Used for |
|-----------|----------|----------|
| **CPU** | General-purpose | Most computing tasks |
| **GPU** | Massive parallelism | ML, graphics, scientific computing |
| **TPU** | Optimised for tensor ops | Deep learning (Google) |
| **FPGA** | Customisable hardware | Specialised pipelines, low-latency |
| **ASIC** | Application-specific | Bitcoin mining, dedicated tasks |

CPU components:
```
Control Unit (CU)         →  fetches and decodes instructions
Arithmetic Logic Unit (ALU) →  performs computations
Registers                  →  ultra-fast tiny memory inside CPU
Cache                      →  fast memory near CPU
```

---

## Memory & Storage Hierarchy

From **fastest + smallest** to **slowest + largest**:

```
Registers       (ns)        few bytes        ← inside CPU
Cache L1/L2/L3  (ns to µs)  KB to MB         ← on CPU die
RAM             (µs)        GB                ← main memory
SSD             (ms)        TB                ← persistent storage
HDD             (10s of ms) TB                ← cheaper persistent
Network/Cloud   (10s-100s of ms)  any size    ← remote storage
```

**Key insight:** speed decreases and capacity increases as you move down. Big data doesn't fit in RAM, so we need:
- Distributed storage (HDFS, S3)
- Smart caching (Spark's in-memory layer)
- Lazy evaluation to avoid reading what we don't need

---

## Why This Matters for PySpark

```
Spark sits on TOP of:
   ✓ Distributed computing model (multiple machines)
   ✓ Distributed storage (HDFS, S3, etc.)
   ✓ Cluster manager (YARN, Mesos, Kubernetes)

Spark gives you:
   ✓ A Python/Scala API that hides distribution complexity
   ✓ Fault tolerance via RDD lineage
   ✓ In-memory computation (faster than Hadoop MapReduce)
   ✓ Optimisations via Catalyst optimizer & DAG scheduling
```

Without distributed computing, you couldn't process big data. Without Spark's API, distributed computing would be much harder to use.

---

## Common Interview Questions

```
Q: Why is distributed computing needed?
A: Single machines hit memory and compute limits.
   Distributed = scale horizontally with more machines.

Q: Difference between parallel and distributed?
A: Parallel = many cores ONE machine.
   Distributed = many cores across MANY machines.

Q: Why is memory hierarchy important for big data?
A: Big data doesn't fit in RAM → must read from disk/network.
   Smart caching (Spark) and partitioning minimise expensive reads.

Q: When would you choose grid over cluster?
A: Grid for opportunistic compute across organisations.
   Cluster for dedicated, low-latency workloads (like Spark).
```

---

## Summary

```
Serial      →  one core, sequential
Parallel    →  many cores, one machine
Distributed →  many machines, one task   ← Spark lives here
Grid        →  many dispersed machines
Cloud       →  rent distributed infrastructure on demand

Memory hierarchy matters because data is too big for RAM.
Spark uses distributed storage + smart caching to handle TB-scale data.
```

> Distributed computing is the bedrock of modern data engineering. Spark and PySpark let you tap into it without manually managing 100 machines.
