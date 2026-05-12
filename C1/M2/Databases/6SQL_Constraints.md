# SQL — Constraints & DDL Syntax

---

## PRIMARY KEY

```sql
-- Inline (single column)
CREATE TABLE employee (
    emp_id  VARCHAR(10) PRIMARY KEY,
    name    VARCHAR(50)
);

-- Table-level (single or composite)
CREATE TABLE employee (
    emp_id  VARCHAR(10),
    name    VARCHAR(50),
    PRIMARY KEY (emp_id)
);

-- Composite primary key
CREATE TABLE order_item (
    order_id    VARCHAR(10),
    product_id  VARCHAR(10),
    qty         INT,
    PRIMARY KEY (order_id, product_id)
);

-- Named + add later
ALTER TABLE employee
ADD CONSTRAINT pk_employee PRIMARY KEY (emp_id);

-- Drop
ALTER TABLE employee
DROP PRIMARY KEY;
```

**Rules:**
- Implicitly `NOT NULL` + `UNIQUE`
- Only one per table
- Can be composite

---

## FOREIGN KEY

```sql
-- Inline
CREATE TABLE employee (
    emp_id  VARCHAR(10) PRIMARY KEY,
    dept_id VARCHAR(10) REFERENCES department(dept_id)
);

-- Table-level (recommended — supports naming and ON DELETE)
CREATE TABLE employee (
    emp_id  VARCHAR(10) PRIMARY KEY,
    dept_id VARCHAR(10),
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

-- Named with referential actions
CREATE TABLE employee (
    emp_id  VARCHAR(10) PRIMARY KEY,
    dept_id VARCHAR(10),
    CONSTRAINT fk_emp_dept
        FOREIGN KEY (dept_id)
        REFERENCES department(dept_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Add to existing table
ALTER TABLE employee
ADD CONSTRAINT fk_emp_dept
    FOREIGN KEY (dept_id) REFERENCES department(dept_id);

-- Drop
ALTER TABLE employee
DROP FOREIGN KEY fk_emp_dept;
```

**ON DELETE / ON UPDATE options:**

| Action | Behaviour |
|---|---|
| `CASCADE` | Delete/update child rows automatically |
| `SET NULL` | Set FK column to NULL in child |
| `SET DEFAULT` | Set FK column to its default value |
| `RESTRICT` | Block the delete/update if children exist |
| `NO ACTION` | Same as RESTRICT (checked at end of transaction) |

---

## UNIQUE

```sql
-- Inline
CREATE TABLE employee (
    emp_id  VARCHAR(10) PRIMARY KEY,
    email   VARCHAR(100) UNIQUE,
    phone   VARCHAR(15)  UNIQUE
);

-- Table-level (named)
CREATE TABLE employee (
    emp_id  VARCHAR(10) PRIMARY KEY,
    email   VARCHAR(100),
    CONSTRAINT uq_email UNIQUE (email)
);

-- Composite unique (combination must be unique, not each column individually)
CREATE TABLE employee (
    emp_id      VARCHAR(10) PRIMARY KEY,
    first_name  VARCHAR(50),
    last_name   VARCHAR(50),
    CONSTRAINT uq_fullname UNIQUE (first_name, last_name)
);

-- Add to existing table
ALTER TABLE employee
ADD CONSTRAINT uq_email UNIQUE (email);

-- Drop
ALTER TABLE employee
DROP INDEX uq_email;          -- MySQL
-- or
ALTER TABLE employee
DROP CONSTRAINT uq_email;     -- PostgreSQL / SQL Server
```

**UNIQUE vs PRIMARY KEY:**

| | PRIMARY KEY | UNIQUE |
|---|---|---|
| NULLs allowed | No | Yes (one NULL per column in most DBs) |
| Per table | Only one | Many |
| Enforces | Identity | No duplicates |

---

## NOT NULL

```sql
-- Inline only (no table-level syntax)
CREATE TABLE employee (
    emp_id  VARCHAR(10) PRIMARY KEY,
    name    VARCHAR(50)  NOT NULL,
    email   VARCHAR(100) NOT NULL,
    dept_id VARCHAR(10)             -- nullable (optional)
);

-- Add to existing column
ALTER TABLE employee
MODIFY name VARCHAR(50) NOT NULL;       -- MySQL

ALTER TABLE employee
ALTER COLUMN name VARCHAR(50) NOT NULL; -- SQL Server

-- Drop (make nullable)
ALTER TABLE employee
MODIFY name VARCHAR(50) NULL;           -- MySQL
```

---

## CHECK

```sql
-- Inline
CREATE TABLE employee (
    emp_id  VARCHAR(10)   PRIMARY KEY,
    age     INT           CHECK (age >= 18),
    salary  DECIMAL(10,2) CHECK (salary > 0),
    gender  CHAR(1)       CHECK (gender IN ('M', 'F', 'O'))
);

-- Named, table-level
CREATE TABLE employee (
    emp_id  VARCHAR(10)   PRIMARY KEY,
    age     INT,
    salary  DECIMAL(10,2),
    CONSTRAINT chk_age    CHECK (age >= 18),
    CONSTRAINT chk_salary CHECK (salary > 0)
);

-- Multi-column check
CREATE TABLE booking (
    booking_id VARCHAR(10) PRIMARY KEY,
    start_date DATE,
    end_date   DATE,
    CONSTRAINT chk_dates CHECK (end_date > start_date)
);

-- Range check
CREATE TABLE product (
    product_id VARCHAR(10)   PRIMARY KEY,
    price      DECIMAL(10,2) CHECK (price BETWEEN 0 AND 99999)
);

-- Add to existing table
ALTER TABLE employee
ADD CONSTRAINT chk_age CHECK (age >= 18);

-- Drop
ALTER TABLE employee
DROP CONSTRAINT chk_age;
```

**What CHECK can and cannot do:**

| | Example |
|---|---|
| ✅ Compare to fixed value | `age >= 18` |
| ✅ List of permitted values | `status IN ('Active', 'Inactive')` |
| ✅ Range | `price BETWEEN 0 AND 9999` |
| ✅ Multi-column logic | `end_date > start_date` |
| ❌ Reference another table | Use `FOREIGN KEY` instead |
| ❌ Reference another row | Use triggers instead |

---

## DEFAULT

```sql
CREATE TABLE orders (
    order_id    VARCHAR(10)  PRIMARY KEY,
    status      VARCHAR(20)  DEFAULT 'Pending',
    created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    qty         INT          DEFAULT 1
);

-- Add to existing column
ALTER TABLE orders
ALTER COLUMN status SET DEFAULT 'Pending';    -- PostgreSQL

ALTER TABLE orders
MODIFY status VARCHAR(20) DEFAULT 'Pending';  -- MySQL

-- Drop default
ALTER TABLE orders
ALTER COLUMN status DROP DEFAULT;             -- PostgreSQL
```

---

## All Constraints Together

```sql
CREATE TABLE order_item (
    order_id    VARCHAR(10)   NOT NULL,
    product_id  VARCHAR(10)   NOT NULL,
    qty         INT           NOT NULL      CHECK (qty > 0),
    discount    DECIMAL(5,2)  DEFAULT 0.00  CHECK (discount BETWEEN 0 AND 100),

    PRIMARY KEY (order_id, product_id),

    CONSTRAINT fk_order
        FOREIGN KEY (order_id)   REFERENCES orders(order_id)   ON DELETE CASCADE,
    CONSTRAINT fk_product
        FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE RESTRICT
);
```

---

## Quick Reference

| Constraint | Inline | Table-level | Multiple per table | NULLs |
|---|---|---|---|---|
| `PRIMARY KEY` | ✅ | ✅ | ❌ one only | ❌ |
| `FOREIGN KEY` | ✅ | ✅ | ✅ | ✅ |
| `UNIQUE` | ✅ | ✅ | ✅ | ✅ (one NULL) |
| `NOT NULL` | ✅ | ❌ | ✅ | N/A |
| `CHECK` | ✅ | ✅ | ✅ | ✅ |
| `DEFAULT` | ✅ | ❌ | ✅ | N/A |
