# SQL — ALTER TABLE

---

## Four Operations

```
ADD     — add something new (column or constraint)
MODIFY  — change an existing column's definition
RENAME  — rename a column or table
DROP    — remove a column or constraint
```

---

## ADD

```sql
-- Add a new column
ALTER TABLE employee ADD COLUMN salary DECIMAL(10,2);
ALTER TABLE employee ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Add a constraint
ALTER TABLE employee ADD CONSTRAINT chk_age    CHECK (age >= 18);
ALTER TABLE employee ADD CONSTRAINT uq_email   UNIQUE (email);
ALTER TABLE employee ADD CONSTRAINT pk_emp     PRIMARY KEY (emp_id);
ALTER TABLE employee ADD CONSTRAINT fk_dept
    FOREIGN KEY (dept_id) REFERENCES department(dept_id) ON DELETE CASCADE;
```

---

## MODIFY / ALTER COLUMN

Change data type, size, or nullability of an existing column.

```sql
-- MySQL
ALTER TABLE employee MODIFY salary    DECIMAL(12,2) NOT NULL;
ALTER TABLE employee MODIFY name      VARCHAR(100);

-- PostgreSQL
ALTER TABLE employee ALTER COLUMN salary  TYPE DECIMAL(12,2);
ALTER TABLE employee ALTER COLUMN name    SET NOT NULL;
ALTER TABLE employee ALTER COLUMN dept_id DROP NOT NULL;

-- SQL Server
ALTER TABLE employee ALTER COLUMN salary  DECIMAL(12,2) NOT NULL;
```

---

## RENAME

```sql
-- RENAME — dedicated command, table level only (MySQL)
RENAME TABLE employee TO staff;
RENAME TABLE employee TO staff, department TO dept;   -- rename multiple in one go

-- ALTER + RENAME — rename column or table
ALTER TABLE employee RENAME COLUMN emp_id TO employee_id;   -- column (PostgreSQL / MySQL 8+)
ALTER TABLE employee RENAME TO staff;                        -- table (PostgreSQL / MySQL)
EXEC sp_rename 'employee', 'staff';                          -- table (SQL Server)
EXEC sp_rename 'employee.emp_id', 'employee_id', 'COLUMN';  -- column (SQL Server)
```

**RENAME vs ALTER RENAME:**

| | `RENAME TABLE` | `ALTER ... RENAME` |
|---|---|---|
| Rename table | ✅ | ✅ |
| Rename column | ❌ | ✅ |
| Multiple tables at once | ✅ (MySQL) | ❌ |
| Other operations (ADD/DROP) | ❌ | ✅ |

```
RENAME TABLE  →  shorthand for table renaming only (MySQL)
ALTER TABLE   →  full toolkit — rename columns, tables, plus ADD/DROP/MODIFY

PostgreSQL has no standalone RENAME TABLE — must use ALTER TABLE ... RENAME TO
```

---

## DROP

```sql
-- Drop a column
ALTER TABLE employee DROP COLUMN salary;

-- Drop constraints
ALTER TABLE employee DROP CONSTRAINT chk_age;
ALTER TABLE employee DROP CONSTRAINT uq_email;
ALTER TABLE employee DROP PRIMARY KEY;
ALTER TABLE employee DROP FOREIGN KEY fk_dept;    -- MySQL
ALTER TABLE employee DROP CONSTRAINT fk_dept;     -- PostgreSQL / SQL Server

-- Drop index (MySQL way to drop UNIQUE)
ALTER TABLE employee DROP INDEX uq_email;         -- MySQL
```

---

## Quick Reference

| Operation | Keyword | What it targets |
|---|---|---|
| `ADD` | New column or constraint | Didn't exist before |
| `MODIFY` / `ALTER COLUMN` | Existing column definition | Type, size, nullability |
| `RENAME` | Column or table name | Name only, data untouched |
| `DROP` | Column or constraint | Removes it entirely |

---

## Syntax Differences by Database

| Action | MySQL | PostgreSQL | SQL Server |
|---|---|---|---|
| Change type | `MODIFY col INT` | `ALTER COLUMN col TYPE INT` | `ALTER COLUMN col INT` |
| Set NOT NULL | `MODIFY col INT NOT NULL` | `ALTER COLUMN col SET NOT NULL` | `ALTER COLUMN col INT NOT NULL` |
| Drop NOT NULL | `MODIFY col INT NULL` | `ALTER COLUMN col DROP NOT NULL` | `ALTER COLUMN col INT NULL` |
| Rename column | `RENAME COLUMN old TO new` | `RENAME COLUMN old TO new` | `EXEC sp_rename 'tbl.old','new','COLUMN'` |
| Drop FK | `DROP FOREIGN KEY name` | `DROP CONSTRAINT name` | `DROP CONSTRAINT name` |

---

## Gotcha — ADD vs MODIFY

```
ADD     = the column or constraint does not exist yet  → creates it
MODIFY  = the column already exists                    → changes its definition

Using ADD on an existing column → error
Using MODIFY on a non-existent column → error
```

---

## DROP vs TRUNCATE vs DELETE

```sql
DROP TABLE employee;              -- removes everything
TRUNCATE TABLE employee;          -- removes all rows, keeps the table
DELETE FROM employee;             -- removes all rows one by one, keeps the table
DELETE FROM employee WHERE ...;   -- removes specific rows
```

| | DROP | TRUNCATE | DELETE |
|---|---|---|---|
| **Type** | DDL | DDL | DML |
| **Removes rows** | ✅ | ✅ | ✅ |
| **Removes schema** | ✅ | ❌ | ❌ |
| **Removes constraints** | ✅ | ❌ | ❌ |
| **Can filter rows** | ❌ | ❌ | ✅ (`WHERE`) |
| **Speed** | Fast | Fast (drops & recreates table) | Slow (row by row) |
| **Rollback possible** | ❌ | ❌ (mostly) | ✅ |
| **Resets AUTO_INCREMENT** | ✅ | ✅ | ❌ |

**In plain English:**
```
DROP     = demolish the building entirely — structure and data both gone
TRUNCATE = gut the building — keep the structure, remove everything inside, fast
DELETE   = remove items one by one — slow, but surgical, can undo
```

**Gotcha:**
```
TRUNCATE is DDL not DML — it cannot be rolled back in most databases
DELETE is DML — wrapped in a transaction it can be rolled back

TRUNCATE is much faster on large tables because it drops and recreates
the table internally rather than logging each row deletion.
```
