# EDMLDS — M2 — Database Design Recap

---

## Gotchas

### Entity Constraints — what they do and don't do

Constraints (`PRIMARY KEY`, `UNIQUE`, `NOT NULL`, `DEFAULT`, `CHECK`) are for **data quality and integrity only**.

| Constraint | Does | Does NOT |
|---|---|---|
| `NOT NULL` | Ensures a value is always provided | Control who can access the data |
| `UNIQUE` | Ensures no duplicate values in a column | Prevent updates to the column |
| `PRIMARY KEY` | Uniquely identifies each row | Manage user permissions |
| `CHECK` | Validates value against a condition | Replace application-level validation |

**Common wrong assumptions:**

```
Constraints = access control?   NO — access control is handled by roles, permissions, views
Constraints = prevent updates?  NO — preventing updates is handled by permissions or triggers
Constraints = no duplicates?    YES — but only UNIQUE/PK, not NOT NULL or CHECK
```

---

### mappedBy — value is the Java field name, not the DB column name

```java
@JoinColumn(name = "d_id")       // "d_id"       = DB column name
private Department department;   // "department"  = Java field name

@OneToMany(mappedBy = "department")   // must match Java field name, NOT "d_id"
```

---

### FK alone does not tell you if it is 1:1 or 1:M

```sql
FOREIGN KEY (e_id) REFERENCES employee(e_id)   -- could be either

-- Only UNIQUE on the FK column confirms 1:1:
e_id VARCHAR(10) UNIQUE,
FOREIGN KEY (e_id) REFERENCES employee(e_id)   -- definitively 1:1
```

---

### The entity with the FK is the child AND the owner

```
Has FK  =  child  =  owner  =  @JoinColumn side
No FK   =  parent =  non-owner = mappedBy side
```

"Child" means dependent on, not derived from. You cannot insert a child row referencing a parent that doesn't exist.

---

### In M:M, @JoinTable placement is a business decision

Both sides are equal. DB schema is identical regardless of which side you put `@JoinTable` on. Pick the side you query from most often.

---

### Cardinality direction — reading FROM one entity TO another

The direction of the question changes the answer even for the same relationship.

**Example:** Team and Project
```
One Team    → one Project     (a team belongs to one project)
One Project → many Teams      (a project has many teams)
```

**Tables:**
```
PROJECT
+------------+--------------+
| project_id | project_name |
+------------+--------------+
| P1         | Banking App  |
| P2         | Trading Sys  |
+------------+--------------+

TEAM
+---------+---------------+------------+
| team_id | team_name     | project_id |  ← FK lives here (child/many side)
+---------+---------------+------------+
| T1      | Backend Team  | P1         |
| T2      | QA Team       | P1         |
| T3      | UI Team       | P1         |
| T4      | Analytics Team| P2         |
+---------+---------------+------------+

P1 has 3 teams. Each team points to exactly one project.
```

| Question direction | Answer |
|---|---|
| FROM Team TO Project | Many-to-One (M:1) — many teams share one project |
| FROM Project TO Team | One-to-Many (1:M) — one project has many teams |

Same relationship. Opposite direction. Different label.

**Rule:** Read the question direction as *"how many [source] rows point to one [target] row?"*
```
FROM Team TO Project:  how many Teams point to one Project?  → Many  → M:1
FROM Project TO Team:  how many Projects point to one Team?  → One   → 1:M
```

ERD: `TEAM >O——|| PROJECT`  — FK (project_id) lives on TEAM (the many/child side).

---

### USING in chained JOINs — works or errors depending on schema

```sql
SELECT id, col_1, col_2
FROM table_1 a
INNER JOIN table_2 b USING(id)
INNER JOIN table_3 c USING(id_2);
```

**Whether this errors depends on where `id_2` lives:**

```
id_2 in table_1 only  →  ✅ works — one unambiguous id_2 on left side
id_2 in table_2 only  →  ✅ works — one unambiguous id_2 on left side
id_2 in BOTH tables   →  ✗  error — two id_2 columns in intermediate result
```

After `USING(id)`, only `id` is merged. `id_2` is NOT part of that USING — so if both table_1 and table_2 have `id_2`, both survive into the intermediate result → `USING(id_2)` can't resolve which one.

**Quiz answer (happy path):** assumes `id_2` exists in only one of the first two tables → no ambiguity → works fine, performs inner join on `id_2` with table_3.

**Fix for ambiguous case — use ON:**
```sql
SELECT id, col_1, col_2
FROM table_1 a
INNER JOIN table_2 b ON a.id   = b.id
INNER JOIN table_3 c ON a.id_2 = c.id_2;   -- explicit, no ambiguity
```

**Rule:** `USING(col)` is safe only when `col` appears unambiguously once on each side.
When chaining 3+ tables, prefer `ON` to stay explicit.

---

### Self-join on salary table to compare student vs roommate salary

To compare a value from two different rows in the same table, join that table **twice with two aliases**.

```sql
SELECT st.student_name
FROM student st
JOIN roommate rm    ON st.student_id  = rm.student_id
JOIN salary   st_sa ON st.student_id  = st_sa.student_id   -- student's salary
JOIN salary   rm_sa ON rm.roommate_id = rm_sa.student_id   -- roommate's salary
WHERE st_sa.salary = rm_sa.salary
ORDER BY st.student_id;
```

```
salary joined twice:
  st_sa  →  alias for student's salary row
  rm_sa  →  alias for roommate's salary row
WHERE st_sa.salary = rm_sa.salary  →  only keep pairs where salaries match
```

**Pattern:** any time you need to compare two rows from the same table — self-join with two aliases.

**Common mistakes to avoid:**
- Wrong column name: table has `student_name` not `name`
- Missing `ORDER BY` when question asks for ordered output
- Typos in table/column names (`roomate` vs `roommate`)

---

### Facts are not always numeric

The rule of thumb is numeric = fact, but the real test is **aggregatability**:

> *Can I meaningfully SUM, AVG, or COUNT this column to answer a business question?*

```
SUM(revenue)       ✓ makes sense  → fact
AVG(quantity)      ✓ makes sense  → fact
SUM(customer_name) ✗ nonsense     → dimension
AVG(city)          ✗ nonsense     → dimension
```

| | Fact | Dimension |
|---|---|---|
| Typical type | Numeric — measurable, aggregatable | Text/categorical — descriptive |
| Examples | revenue, qty, discount, duration | name, city, segment, category |

**Edge cases:**

| Column | Type | Why |
|---|---|---|
| `Order_Date` | Fact | Records when the event occurred — timestamp |
| `Transaction_ID` | Degenerate dimension | Lives in fact table but is an identifier, not a measure |
| `Status` | Debatable | "Shipped", "Returned" — descriptive, often treated as dimension |

In interviews/exams: if it's numeric and in a transaction table → treat it as a fact.
A table named after an entity (customers, products) → almost always a dimension table with 0 facts.

---

## Practice Questions

### Q2 — Entity Constraints (2/7)

**Entity constraints such as PRIMARY KEY, UNIQUE and NOT NULL are used to:**

| Option | Correct? | Reason |
|---|---|---|
| Validate the quality of data entered for a specific property | ✅ | Constraints such as `NOT NULL` help validate input and ensure data quality |
| Control who is allowed access to the data | ❌ | Access control = roles, permissions, views — not constraints |
| Ensure that duplicate records are not entered | ✅ | `UNIQUE` and `PRIMARY KEY` prevent duplicate values |
| Prevent users from changing values stored in the table | ❌ | Preventing updates = database permissions or triggers, not constraints |

---

### Q — Fact variables in Customers table

**How many fact variables are present in the customers table?**

```
customers: Customer_Name, City, State, Customer_Segment, Cust_id
```

**Answer: 0**

Every column is a dimension (descriptive) — not a fact (quantitative measure).

| Column | Type | Why |
|---|---|---|
| `Customer_Name` | Dimension | Describes who — text |
| `City` | Dimension | Describes where — text |
| `State` | Dimension | Describes where — text |
| `Customer_Segment` | Dimension | Describes category — text |
| `Cust_id` | Dimension | Identifier — not a measure |

The customers table IS a dimension table. Fact variables (revenue, qty, discount) live in a fact table.

```
FACT_SALES                        DIM_CUSTOMER
+----------+--------+----------+  +---------+---------------+-------+
| sale_id  | amount | cust_id  |  | cust_id | customer_name | city  |
+----------+--------+----------+  +---------+---------------+-------+
             ↑                                ↑
           FACT                            DIMENSION
        (quantitative)                   (descriptive)
```
