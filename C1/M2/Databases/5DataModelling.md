# Data Modelling

## What is Data Modelling?

The world produces huge amounts of unorganised, unstructured data. Data modelling is the process of deciding **how to collect, organise and structure that data** so it can be analysed and acted on.

> ERD = the floor plan for a schema.
> Just as you finalise a building's floor plan before construction, you finalise the data model before building the database. Once relationships are defined it is hard to alter them — like adding a foundation after the building is up.

---

## Real-World Use Cases

| Industry | Data Captured |
|---|---|
| **Social Media** (Facebook, Instagram, Twitter) | User profile, pages visited, interactions, likes vs friends' likes |
| **Streaming** (Netflix, Prime, YouTube) | Categories watched, drop-off points in videos, ad-skipping behaviour |
| **Airlines** (IndiGo, Air India) | Ticket bookings, origin/destination, peak booking periods, high-demand routes |
| **Mobile Apps** (Swiggy, Ola, Amazon) | Navigation paths, time on pages, saved addresses |
| **Banking** (SBI, HDFC, ICICI) | Transaction history, user profile, preferred channel (netbanking/branch/phone) |

Banking example: transaction data helps target customers for loans/credit cards and detect fraudulent activity from irregularities.

---

## Data Warehouse

A **data warehouse** is a specialised system for storing large volumes of structured historical data collected from multiple sources across an organisation.

| | Operational Database (OLTP) | Data Warehouse (OLAP) |
|---|---|---|
| Purpose | Day-to-day transactions | Analytics, reporting, decisions |
| Data | Current, live | Historical, aggregated |
| Queries | Simple, fast writes | Complex, read-heavy |
| Design | Normalised (3NF) | Often denormalised (star/snowflake) |

The accuracy and performance of a data warehouse depends heavily on how well the **data model** has been designed upfront.

---

## Why ERDs Come First

1. ERDs identify entities, relationships and constraints before any table is created
2. Once the model is built and populated, restructuring is expensive
3. Poor design → anomalies, redundancy, slow queries → hard to fix later

```
ERD (design)  →  Schema (structure)  →  Data Warehouse (storage)  →  Analysis
```

---

## Practice Questions

### Q1 — Why is data modelling necessary at the logical level?

| Option | Correct? | Reason |
|---|---|---|
| To design different data elements in a particular structure | ✅ | Data models provide a structure to the data |
| To design the physical structure in which data can be stored on devices | ❌ | Logical level does not deal with physical storage — that is the physical layer |
| To give a specific structure to the data in accordance with business requirements | ✅ | Data models are built in accordance with business requirements |
| To design applications that can be used to access data | ❌ | Application design is the view/presentation layer, not the logical level |

**The three levels of a database:**
```
View level     (external)  — applications, user interfaces
Logical level  (conceptual) — structure of data, relationships, constraints  ← data modelling
Physical level (internal)  — how data is stored on disk, indexes, files
```

---

### Q5 — Data quality assurance in a relational model (Graded)

**How does a table in a relational model provide data quality assurance?**

| Option | Correct? | Reason |
|---|---|---|
| By ensuring that non-null fields contain values | ✅ | `NOT NULL` constraint prevents incomplete data entry — essential fields must always have a value |
| By ensuring that every field contains only permitted values | ✅ | `CHECK` or `FOREIGN KEY` constraints restrict values to a valid domain or reference set |
| By ensuring that the data in a field is of the specified data type | ✅ | Every column is defined with a data type — type mismatches are rejected at insert/update time |
| By ensuring that the rows are in a particular order | ❌ | Row order is NOT guaranteed in the relational model — use `ORDER BY` in queries to impose order |

**Gotcha:** Rows in a relational table are **unordered by definition**. Any order you see is coincidental — never rely on it without an explicit `ORDER BY`.
