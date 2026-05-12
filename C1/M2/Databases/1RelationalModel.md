# Relational Database Model

## Data Structure

Data is stored in **tables** (also called relations). Each table has:

```
Relation Heading  →  column names + datatypes
Relation Body     →  actual records (rows)
```

Example:
```
| ID (INTEGER) | NAME (STRING) | DEPARTMENT (STRING) |
|--------------|---------------|---------------------|
| 101          | Alice         | Engineering         |
| 102          | Bob           | Marketing           |
```

---

## Keys

### Primary Key
- Uniquely identifies each row in a table
- **Uniqueness:** no two rows can have the same value
- **Non-nullability:** cannot be NULL

```
EMPLOYEE table:  E_ID is primary key
DEPARTMENT table: D_ID is primary key
```

### Composite Primary Key
When a single column is not enough — combine two or more columns:
```
ORDER_ITEMS table: (ORDER_ID + PRODUCT_ID) together = primary key
```

### Candidate Key
Any column (or combination) that **could** serve as a primary key.
The one chosen = primary key. The rest = **alternate keys**.

### Foreign Key
An attribute in one table that **links to the primary key of another table**.

```
EMPLOYEE.D_ID  →  references  →  DEPARTMENT.D_ID
     ↑                                  ↑
  foreign key                       primary key
```

**Properties:**
- **Referential integrity** — value must exist in the referenced table or be NULL
- **Data consistency** — prevents orphan records (employee in non-existent dept)
- **Relational navigation** — enables JOINs between tables
- **Optional** — foreign keys can allow NULLs

---

## Constraints

| Constraint | Meaning | Example |
|---|---|---|
| PRIMARY KEY | Unique + not null identifier | E_ID |
| FOREIGN KEY | Links to another table's PK | D_ID references DEPARTMENT |
| UNIQUE | No duplicates allowed | Email column |
| NOT NULL | Column cannot be empty | Name column |
| CHECK | Custom condition | CHECK (age >= 18) |
| Data Type | Values must match type | INTEGER, STRING, DATE |

---

## Data Integrity — Three Components

| Type | Ensures | Enforced by |
|---|---|---|
| **Attribute integrity** | Each column has correct name and datatype | Schema definition |
| **Entity integrity** | No two rows are identical, each uniquely identifiable | Primary key |
| **Referential integrity** | Relationships between tables are consistent | Foreign key |

---

## Entity-Relationship Diagrams (ERDs)

A visual representation of all tables and how they relate to each other.

### Why use ERDs?
When you have many tables (employees, customers, orders, departments, roles...) — an ERD lets you see the whole database on one diagram.

### Example — Company Database
```
[EMPLOYEE] ----< [EMPLOYEE_ROLES] >---- [ROLES]
    |
    |
[DEPARTMENT]
    |
    |
[ACCOUNT_DETAILS]
```

---

## Cardinality

Defines **how many instances** of one entity relate to another.

### One-to-One (1:1)
```
EMPLOYEE ——— SALARY_ACCOUNT

One employee → exactly one salary account
One salary account → exactly one employee
```

### Many-to-One (M:1) / Many-to-Zero-or-One
```
EMPLOYEE >——— DEPARTMENT

Many employees → one department
One department → many employees
```

### Many-to-Many (M:M)
```
EMPLOYEE >———< ROLES

One employee → many roles
One role → many employees
(requires a junction/bridge table: EMPLOYEE_ROLES)
```

---

## Summary

| Concept | Purpose |
|---|---|
| Primary key | Uniquely identify each row |
| Composite key | When one column isn't enough |
| Foreign key | Link tables together |
| Constraints | Enforce data rules |
| ERD | Visualise all tables and relationships |
| Cardinality | Define how many entities relate (1:1, M:1, M:M) |
