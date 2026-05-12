# Schema — Star and Snowflake

## What is a Schema?

A **logical view of a database** — shows how data points are organised and related.

Defines:
- Tables and their columns
- Data types
- Relationships between tables

---

## Facts vs Dimensions

| | Facts | Dimensions |
|---|---|---|
| Type | Quantitative / numerical | Descriptive / metadata |
| Examples | Sales amount, quantity sold, revenue | Customer name, order ID, address, date |
| Changes | Frequently (transactional) | Slowly (reference data) |
| Purpose | What happened (the measure) | Who, what, when, where (the context) |

```
FACT:      Alice bought 3 units of Product X for £50 on 12-May
DIMENSION: Alice (customer), Product X (product), 12-May (time), £50 (fact)
```

---

## Star Schema

The **simplest and most widely used** dimensional model.

```
                [TIME]
                  |
[CUSTOMER] — [FACT: SALES] — [PRODUCT]
                  |
               [STORE]
```

- **Central fact table** — contains measurable data (sales amount, qty)
- **Dimension tables** — directly connected to fact table, provide context
- Shape looks like a star ⭐

### Example — Sales Star Schema
```
FACT_SALES
+------------+-----------+-----------+----------+----------+--------+
| Sale_ID PK | Time_ID FK| Cust_ID FK| Prod_ID FK| Store_ID FK| Amount|
+------------+-----------+-----------+----------+----------+--------+

Surrounded by:
DIM_TIME     → year, quarter, month, day
DIM_CUSTOMER → name, address, age
DIM_PRODUCT  → category, brand, price
DIM_STORE    → location, manager
```

### Pros and Cons
| ✅ Pros | ❌ Cons |
|---|---|
| Fast queries (fewer joins) | Some data redundancy in dimensions |
| Simple and intuitive | Not fully normalised |
| Easy for analysts | |

---

## Snowflake Schema

A **normalised version** of the star schema — dimension tables are broken into sub-dimensions.

```
[REGION]
   |
[ADDRESS]
   |
[CUSTOMER] — [FACT: SALES] — [PRODUCT] — [CATEGORY]
                  |
               [STORE]
                  |
              [LOCATION]
```

### Example — Customer dimension split into sub-tables
```
Star Schema (one table):
DIM_CUSTOMER: customer_id, name, address, city, region

Snowflake Schema (split into):
DIM_CUSTOMER:  customer_id, name, address_id (FK)
DIM_ADDRESS:   address_id, city, region_id (FK)
DIM_REGION:    region_id, region_name
```

### Pros and Cons
| ✅ Pros | ❌ Cons |
|---|---|
| Less redundancy | More complex queries (more joins) |
| Better storage efficiency | Slower query performance |
| Better data integrity | Harder to understand |

---

## Star vs Snowflake

| | Star Schema | Snowflake Schema |
|---|---|---|
| Structure | Fact + flat dimensions | Fact + normalised dimensions |
| Joins needed | Fewer | More |
| Query speed | Faster | Slower |
| Storage | More (redundancy) | Less (normalised) |
| Complexity | Simple | Complex |
| Use case | Analytics, BI dashboards | Large warehouses, storage-sensitive |

---

## Normalisation

The process of **structuring data to minimise redundancy** by splitting larger tables into smaller related ones.

```
Before normalisation (flat):
CUSTOMER: id, name, city, country, continent

After normalisation (snowflake):
CUSTOMER:  id, name, city_id
CITY:      city_id, city_name, country_id
COUNTRY:   country_id, country_name, continent
```

- Reduces duplicate data
- Ensures consistency (change country name in one place, not everywhere)
- Used in snowflake schema
- Trade-off: more joins needed for queries

### Why Normalise — Anomalies

**Data redundancy** = same data stored in multiple places → prone to inconsistency.

**Root cause:** Multiple entities (employee, city, project) crammed into one table with duplicated rows.

**Denormalised table — all three anomalies live here:**
```
EMP_PROJECTS
+--------+--------+-------+------------+
| emp_id | name   | city  | project_id |
+--------+--------+-------+------------+
| 101    | Rohan  | Delhi | D01        |
| 101    | Rohan  | Delhi | D02        |  ← Rohan duplicated
| 103    | Arpit  | Delhi | D01        |
| 166    | Geetika| Pune  | D90        |
| 166    | Geetika| Pune  | D92        |  ← Geetika duplicated
+--------+--------+-------+------------+
```

**1. Insertion Anomaly**
```
Want to add new employee Vishwa (not yet assigned to a project):
+--------+--------+------+------------+
| 102    | Vishwa | Pune | NULL       |  ← forced to insert NULL for project_id

Problem: employee data and project data are coupled.
Cannot store an employee independently of a project.
```

**2. Update Anomaly**
```
Delhi changes to New Delhi — must update EVERY row for that employee:
| 101 | Rohan | Delhi | D01 |   ← updated
| 101 | Rohan | Delhi | D02 |   ← forgot this one → now inconsistent

One row says Delhi, another says New Delhi. Same employee, conflicting data.
```

**3. Deletion Anomaly**
```
Project D90 is removed → delete that row:
| 166 | Geetika | Pune | D90 |  ← deleted

If D90 was the only row containing Geetika's city info,
deleting the project accidentally deletes employee/city data too.
```

| Anomaly | Trigger | Effect |
|---|---|---|
| Insertion | Adding entity A requires entity B to exist | Incomplete or blocked inserts |
| Update | Same data duplicated across rows | Inconsistency when one copy is missed |
| Deletion | Unrelated data shares a row | Losing data you didn't intend to delete |

---

### First Normal Form (1NF)

**Rules:**
1. Every cell must hold a single (atomic) value — no comma-separated lists
2. Every row must be uniquely identifiable (has a primary key)

**Before 1NF (violates rule 1):**
```
ORDERS
+----------+---------+-----------+------------------+---------+--------+
| order_id | cust_id | cust_name | products         | price   | city   |
+----------+---------+-----------+------------------+---------+--------+
| 1        | C01     | Alice     | Pen, Notebook    | 1, 5    | London |
| 2        | C01     | Alice     | Pen              | 1       | London |
| 3        | C02     | Bob       | Notebook         | 5       | Paris  |
```

**After 1NF — one row per product:**
```
ORDERS (1NF)
+----------+---------+-----------+----------+-------+--------+
| order_id | cust_id | cust_name | product  | price | city   |
+----------+---------+-----------+----------+-------+--------+
| 1        | C01     | Alice     | Pen      | 1     | London |
| 1        | C01     | Alice     | Notebook | 5     | London |
| 2        | C01     | Alice     | Pen      | 1     | London |
| 3        | C02     | Bob       | Notebook | 5     | Paris  |
+----------+---------+-----------+----------+-------+--------+
PK = (order_id + product)  ← composite key
```

---

### Second Normal Form (2NF)

**Rules:**
1. Must already be in 1NF
2. No **partial dependency** — every non-key column must depend on the **whole** primary key, not just part of it

> Only possible to violate when PK is composite (two or more columns).
> Test: *"If I only knew part of the PK, could I already determine this column's value?"* → yes = partial dependency.

**Problem in 1NF above** — PK is `(order_id, product)` but:
```
cust_name → depends only on order_id   ✗ partial (cust_name has nothing to do with product)
city      → depends only on order_id   ✗ partial
price     → depends only on product    ✗ partial (price has nothing to do with which order)
qty       → needs both order_id + product  ✓ full dependency
```

**More partial dependency examples:**

```
EXAM_RESULTS  PK = (student_id, course_id)
+------------+-----------+--------------+-------+
| student_id | course_id | student_name | grade |
+------------+-----------+--------------+-------+
student_name → only student_id   ✗ partial  (Alice is Alice in every course)
grade        → both              ✓ full     (grade changes per student per course)

STOCK  PK = (warehouse_id, product_id)
+--------------+------------+----------------+----------+-----+
| warehouse_id | product_id | warehouse_city | p_name   | qty |
+--------------+------------+----------------+----------+-----+
warehouse_city → only warehouse_id  ✗ partial
p_name         → only product_id    ✗ partial
qty            → both               ✓ full
```

**After 2NF — split into separate tables:**
```
ORDER_ITEMS                    ORDERS               
+----------+----------+-----+  +----------+---------+
| order_id | product  | qty |  | order_id | cust_id |
+----------+----------+-----+  +----------+---------+
| 1        | Pen      | 2   |  | 1        | C01     |
| 1        | Notebook | 1   |  | 2        | C01     |
| 2        | Pen      | 1   |  | 3        | C02     |
| 3        | Notebook | 3   |  
                               CUSTOMERS
PRODUCTS                       +---------+-----------+--------+
+----------+-------+           | cust_id | cust_name | city   |
| product  | price |           +---------+-----------+--------+
+----------+-------+           | C01     | Alice     | London |
| Pen      | 1     |           | C02     | Bob       | Paris  |
| Notebook | 5     |           
```

---

### Third Normal Form (3NF)

**Rules:**
1. Must already be in 2NF
2. No **transitive dependency** — a non-key column must not depend on another non-key column

```
Transitive chain:   PK → non-key col A → non-key col B
                                               ↑
                              B depends on A, not directly on PK
```

**Example 1 — Employee:**
```
EMPLOYEE  PK = emp_id
+--------+-------+---------+-----------+
| emp_id | name  | dept_id | dept_name |
+--------+-------+---------+-----------+
| E01    | Alice | D01     | Engg      |
| E02    | Bob   | D01     | Engg      |
| E03    | Carol | D02     | Mktg      |

Chain: emp_id → dept_id → dept_name
dept_name doesn't care about emp_id — it only depends on dept_id (a non-key column) ✗
```

Fix:
```
EMPLOYEE                        DEPARTMENT
+--------+-------+---------+    +---------+-----------+
| emp_id | name  | dept_id |    | dept_id | dept_name |
+--------+-------+---------+    +---------+-----------+
| E01    | Alice | D01     |    | D01     | Engg      |
| E02    | Bob   | D01     |    | D02     | Mktg      |
| E03    | Carol | D02     |    +---------+-----------+
```

**Example 2 — Orders with zip code:**
```
ORDERS  PK = order_id
+----------+---------+----------+--------+
| order_id | cust_id | zip_code | city   |
+----------+---------+----------+--------+
| O01      | C01     | SW1A     | London |
| O02      | C02     | 75001    | Paris  |

Chain: order_id → zip_code → city
city depends on zip_code, not on order_id ✗
```

Fix → move `zip_code + city` into a `LOCATION` table.

---

### 2NF vs 3NF — the difference

```
2NF: non-key column depends on PART of the composite PK

     (order_id, product) → cust_name
           ↑
      only this part

3NF: non-key column depends on ANOTHER non-key column

     emp_id → dept_id → dept_name
                             ↑
                  depends on dept_id (non-key), not emp_id
```

| Form | Dependency to remove | Requires composite PK? |
|---|---|---|
| 2NF | Partial — column needs only **part** of PK | Yes |
| 3NF | Transitive — column depends on a **non-key** column | No |

---

### Fourth Normal Form (4NF)

**Rules:**
1. Must already be in 3NF
2. No **multi-valued dependency** — one column must not independently determine multiple values across two unrelated columns

> Notation: `A →→ B` means A multi-determines B (A determines a set of B values)

**What goes wrong:** A single column determines two independent sets of values → every combination must be stored → rows multiply.

**Example 1 — Person Contacts:**
```
PERSON_CONTACT  (violates 4NF)
+-------+----------+--------------------+
| name  | phone    | email              |
+-------+----------+--------------------+
| Alice | 07700    | alice@gmail.com    |
| Alice | 07700    | alice@work.com     |   ← same phone, different email
| Alice | 07800    | alice@gmail.com    |   ← different phone, same email
| Alice | 07800    | alice@work.com     |
+-------+----------+--------------------+

name →→ phone    (phones are independent of emails)
name →→ email    (emails are independent of phones)

2 phones × 2 emails = 4 rows. Add a 3rd email → must add 2 rows (one per phone). ✗
```

Fix:
```
PERSON_PHONE              PERSON_EMAIL
+-------+----------+      +-------+--------------------+
| name  | phone    |      | name  | email              |
+-------+----------+      +-------+--------------------+
| Alice | 07700    |      | Alice | alice@gmail.com    |
| Alice | 07800    |      | Alice | alice@work.com     |
+-------+----------+      +-------+--------------------+
```

**Example 2 — Course Teachers and Textbooks:**
```
COURSE_INFO  (violates 4NF)
+--------+---------+-----------+
| course | teacher | textbook  |
+--------+---------+-----------+
| Maths  | Alice   | Calculus  |
| Maths  | Alice   | Algebra   |   ← same teacher, different book
| Maths  | Bob     | Calculus  |   ← different teacher, same book
| Maths  | Bob     | Algebra   |
+--------+---------+-----------+

course →→ teacher    (who teaches it, unrelated to which books)
course →→ textbook   (which books, unrelated to who teaches)
```

Fix:
```
COURSE_TEACHER            COURSE_TEXTBOOK
+--------+---------+      +--------+-----------+
| course | teacher |      | course | textbook  |
+--------+---------+      +--------+-----------+
| Maths  | Alice   |      | Maths  | Calculus  |
| Maths  | Bob     |      | Maths  | Algebra   |
+--------+---------+      +--------+-----------+
```

---

### 3NF vs 4NF — the difference

```
3NF: non-key column depends on ANOTHER non-key column (chain)
     emp_id → dept_id → dept_name

4NF: one column drives TWO INDEPENDENT sets of values (fan-out)
     name →→ phone
     name →→ email   (phone and email have nothing to do with each other)
```

| Form | Dependency to remove |
|---|---|
| 3NF | Transitive — non-key → non-key chain |
| 4NF | Multi-valued — one key fans out to two independent sets |

---

### Normal Forms Summary

```
Unnorm → 1NF           → 2NF                   → 3NF                      → 4NF
         ───────────     ─────────────────────    ──────────────────────     ──────────────────────────
         Atomic cells    Remove partial deps       Remove transitive deps     Remove multi-valued deps
         One value/cell  Full PK dependency        Direct PK dependency       No independent fan-outs
```

| Form | Key Question |
|---|---|
| 1NF | Does every cell hold exactly one value? |
| 2NF | Does every non-key column need the **whole** PK, or just part of it? |
| 3NF | Does every non-key column depend **directly** on the PK, or via another non-key? |
| 4NF | Does one column independently drive **two separate sets** of values in other columns? |

---

## Summary

```
Flat file → Star Schema → Snowflake Schema
           (some structure)  (fully normalised)

Facts    = what happened (numbers)
Dimensions = context (who, what, when, where)
```
