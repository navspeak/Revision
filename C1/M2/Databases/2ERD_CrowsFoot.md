# ERD — Crow's Foot Notation & Foreign Keys

## Crow's Foot Notation

The most common way to draw ERDs. Uses symbols at the ends of lines to show cardinality.

### Symbols — Drawn

Each symbol sits at the **end of the line**, right next to the entity it describes.

```
                    CARDINALITY MARKS (at line end)
                    ────────────────────────────────

  One (mandatory)        ───|
  Zero (optional)        ───O
  Many (crow's foot)     ───<

  ════════════════════════════════════════════════════

  COMBINED — the two marks closest to the entity tell the full story:

  One and only one       ───||──        (exactly 1, mandatory)
                              ↑↑
                           min  max

  Zero or one            ───O|──        (0 or 1, optional)

  One or many            ───|<──        (at least 1, mandatory)

  Zero or many           ───O<──        (0 or more, optional)

  ════════════════════════════════════════════════════

  HOW TO READ the two symbols:
    Outer mark (far from entity) = MINIMUM  →  O = zero,  | = one
    Inner mark (close to entity) = MAXIMUM  →  | = one,   < = many
```

### Quick Reference Card

```
  Symbol    Reads as           Min   Max
  ──────    ──────────────     ───   ───
  ──||──    One and only one    1     1
  ──O|──    Zero or one         0     1
  ──|<──    One or many         1     ∞
  ──O<──    Zero or many        0     ∞
```

### Reading a relationship — always read BOTH directions

```
EMPLOYEE ||——O< DEPARTMENT

Left to right:  One employee belongs to zero or one department
Right to left:  One department has zero or many employees
```

---

## Common Cardinality Patterns

### One-to-One (1:1)
```
EMPLOYEE ||——|| SALARY_ACCOUNT

One employee has exactly one salary account
One salary account belongs to exactly one employee
```

**Table rows:**
```
EMPLOYEE                       SALARY_ACCOUNT
+------+-------+               +----------+------+--------+
| e_id | name  |               | acct_id  | e_id | salary |
+------+-------+               +----------+------+--------+
| E01  | Alice |               | A01      | E01  | 50000  |
| E02  | Bob   |               | A02      | E02  | 60000  |
+------+-------+               +----------+------+--------+
                               e_id is FK + UNIQUE → enforces 1:1
```

**SQL:**
```sql
CREATE TABLE employee (
    e_id   VARCHAR(10) PRIMARY KEY,
    name   VARCHAR(50)
);

CREATE TABLE salary_account (
    acct_id VARCHAR(10) PRIMARY KEY,
    salary  DECIMAL(10,2),
    e_id    VARCHAR(10) UNIQUE,                      -- UNIQUE enforces 1:1
    FOREIGN KEY (e_id) REFERENCES employee(e_id)     -- FK lives here
);
```

**Who owns?**
```
SALARY_ACCOUNT owns — it holds the FK column (e_id).
EMPLOYEE has no FK — it is the "parent" / referenced side.

Owner    = the table/entity that holds the FK column
Non-owner = the other side (just has a reference back, no FK column)

Should both own? NO.
Only one side holds the FK. The other side just navigates back via mappedBy.
If both held a FK you'd have a circular dependency and two columns to keep in sync.
```

**Java Entity:**
```java
@Entity
public class Employee { // One that has PK is Parent 
    @Id
    private String eId;
    private String name;

    @OneToOne(mappedBy = "employee")   // non-owner: no FK here, points back to owner field
    //  mappedBy says: "I know about this relationship but I don't own it. The FK is defined over there, in the field called employee or whatever its called"
    private SalaryAccount salaryAccount;
}

@Entity
public class SalaryAccount { // One that has FK is child and owner of relationship
    @Id
    private String acctId;
    private double salary;

    @OneToOne
    @JoinColumn(name = "e_id")         // OWNER: FK column lives in this table
    private Employee employee;
}
```

---

### One-to-Many (1:M)
```
DEPARTMENT ||——O< EMPLOYEE

One department has zero or many employees
One employee belongs to exactly one department
```

**Table rows:**
```
DEPARTMENT                     EMPLOYEE
+------+-------+               +------+-------+------+
| d_id | name  |               | e_id | name  | d_id |
+------+-------+               +------+-------+------+
| D01  | Engg  |               | E01  | Alice | D01  |
| D02  | Mktg  |               | E02  | Bob   | D01  |
+------+-------+               | E03  | Carol | D02  |
                               +------+-------+------+
                               d_id is FK → many employees, one dept
```

**SQL:**
```sql
CREATE TABLE department (
    d_id  VARCHAR(10) PRIMARY KEY,
    name  VARCHAR(50)
);

CREATE TABLE employee (
    e_id  VARCHAR(10) PRIMARY KEY,
    name  VARCHAR(50),
    d_id  VARCHAR(10),                               -- FK lives on the MANY side
    FOREIGN KEY (d_id) REFERENCES department(d_id)
);
```

**Who owns?**
```
EMPLOYEE owns — the FK (d_id) lives in the employee table, not department.

Rule: in 1:M the FK ALWAYS lives on the "many" side.
      It would be impossible on the "one" side — a single department row
      cannot hold a list of employee IDs in one column (violates 1NF).

Should both own? NO. Only the many side holds the FK.
```

**Java Entity:**
```java
@Entity
public class Department {
    @Id
    private String dId;
    private String name;

    @OneToMany(mappedBy = "department")   // non-owner: no FK here
    private List<Employee> employees;
}

@Entity
public class Employee {
    @Id
    private String eId;
    private String name;

    @ManyToOne
    @JoinColumn(name = "d_id")            // name = actual DB column name (not Java field name)
    private Department department;        // Java field can be named anything — "department", "dept", "d"
}
```

---

### Many-to-Many (M:M)
```
EMPLOYEE ||——O< EMPLOYEE_ROLES >O——|| ROLES

Requires a junction table (EMPLOYEE_ROLES) in between
One employee has many roles
One role is assigned to many employees
```

**Table rows:**
```
EMPLOYEE           EMPLOYEE_ROLES          ROLES
+------+-------+   +------+------+         +------+---------+
| e_id | name  |   | e_id | r_id |         | r_id | name    |
+------+-------+   +------+------+         +------+---------+
| E01  | Alice |   | E01  | R01  |         | R01  | Manager |
| E02  | Bob   |   | E01  | R02  |         | R02  | Dev     |
+------+-------+   | E02  | R01  |         +------+---------+
                   +------+------+
                   PK = (e_id + r_id) composite
```

**SQL:**
```sql
CREATE TABLE employee (
    e_id  VARCHAR(10) PRIMARY KEY,
    name  VARCHAR(50)
);

CREATE TABLE roles (
    r_id  VARCHAR(10) PRIMARY KEY,
    name  VARCHAR(50)
);

CREATE TABLE employee_roles (
    e_id  VARCHAR(10),
    r_id  VARCHAR(10),
    PRIMARY KEY (e_id, r_id),                          -- composite PK
    FOREIGN KEY (e_id) REFERENCES employee(e_id),
    FOREIGN KEY (r_id) REFERENCES roles(r_id)
);
```

**Who owns?**
```
Neither EMPLOYEE nor ROLES owns — the JUNCTION TABLE (employee_roles) owns both FKs.
In Java, one entity is designated owner just to avoid duplicate SQL being generated.
Pick the more "natural" starting point (usually the one you query from most).

Should both Java entities own? NO — causes Hibernate to insert into the junction
table twice. Use @JoinTable on one side, mappedBy on the other.
```

**Java Entity:**
```java
@Entity
public class Employee {
    @Id
    private String eId;
    private String name;

    @ManyToMany                                        // OWNER side
    @JoinTable(
        name = "employee_roles",
        joinColumns = @JoinColumn(name = "e_id"),
        inverseJoinColumns = @JoinColumn(name = "r_id")
    )
    private List<Role> roles;
}

@Entity
public class Role {
    @Id
    private String rId;
    private String name;

    @ManyToMany(mappedBy = "roles")
    private List<Employee> employees;
}
```

---

## Ownership — Parent, Child, FK

### Owner = Child = holds the FK

> **The table/entity that has the FK is the child AND the owner of the relationship.**

```
Parent table  =  the table whose PK is referenced   →  DEPARTMENT
Child table   =  the table that holds the FK         →  EMPLOYEE

DEPARTMENT (parent)          EMPLOYEE (child)
+------+-------+             +------+-------+------+
| d_id | name  |             | e_id | name  | d_id |  ← FK here
+------+-------+             +------+-------+------+
```

"Child" does not mean derived from — it means DEPENDENT ON.
Employee cannot reference a department that doesn't exist.

Delete rule makes it obvious:
  Delete Employee → fine, no impact on Department       (child removed freely)
  Delete Department → BLOCKED if employees reference it  (parent is protected)
```

Navigation direction at DB level:
  Child → Parent:  easy, FK gives you it directly
  Parent → Child:  must search — no FK on parent, scan by FK value
```

In domain terms Department feels "bigger" (contains employees).
In DB terms Employee is the child (holds the FK, depends on dept existing).
Both are correct — just different angles.

---

### @JoinColumn vs mappedBy — which side, what SQL is generated

| Annotation | Goes on | Meaning | SQL generated |
|---|---|---|---|
| `@JoinColumn` | **Owner (child)** | "I hold the FK column in my table" | Creates the FK column + FOREIGN KEY constraint |
| `mappedBy` | **Non-owner (parent)** | "Use the FK defined over there, don't create anything here" | Nothing — no column, no constraint |

```
Rule: mappedBy side NEVER generates a column.
      @JoinColumn side ALWAYS generates a FK column.
      Only one side should own — if both use @JoinColumn, JPA creates two FK columns (bug).
```

**1:M example — what JPA generates:**

```java
// DEPARTMENT — non-owner (parent)
@OneToMany(mappedBy = "department")    // ← mappedBy: generates NO SQL
private List<Employee> employees;

// EMPLOYEE — owner (child)
@ManyToOne
@JoinColumn(name = "d_id")             // ← generates this:
private Department department;
```

SQL generated by JPA:
```sql
-- From @JoinColumn(name = "d_id") on Employee:
ALTER TABLE employee ADD COLUMN d_id VARCHAR(10);
ALTER TABLE employee ADD CONSTRAINT fk_emp_dept FOREIGN KEY (d_id) REFERENCES department(d_id);

-- From mappedBy on Department:
-- (nothing)
```

**1:1 example — what JPA generates:**

```java
// EMPLOYEE — non-owner
@OneToOne(mappedBy = "employee")       // ← generates NO SQL
private SalaryAccount salaryAccount;

// SALARY_ACCOUNT — owner (child, dependent entity)
@OneToOne
@JoinColumn(name = "e_id")             // ← generates FK + UNIQUE constraint
private Employee employee;
```

SQL generated by JPA:
```sql
ALTER TABLE salary_account ADD COLUMN e_id VARCHAR(10) UNIQUE;
ALTER TABLE salary_account ADD FOREIGN KEY (e_id) REFERENCES employee(e_id);
-- UNIQUE enforces the 1:1 (without it, it would be M:1)
```

**M:M example — what JPA generates:**

```java
// EMPLOYEE — owner (designated)
@ManyToMany
@JoinTable(
    name = "employee_roles",
    joinColumns = @JoinColumn(name = "e_id"),
    inverseJoinColumns = @JoinColumn(name = "r_id")
)                                      // ← generates the entire junction table
private List<Role> roles;

// ROLE — non-owner
@ManyToMany(mappedBy = "roles")        // ← generates NO SQL
private List<Employee> employees;
```

SQL generated by JPA:
```sql
CREATE TABLE employee_roles (
    e_id VARCHAR(10),
    r_id VARCHAR(10),
    PRIMARY KEY (e_id, r_id),
    FOREIGN KEY (e_id) REFERENCES employee(e_id),
    FOREIGN KEY (r_id) REFERENCES roles(r_id)
);
-- mappedBy on Role generates nothing
```

**Which side gets @JoinTable — a business decision:**
```
In M:M neither side is naturally the owner — both are equal.
The DB result is identical regardless of which side you choose.
Same junction table, same two FK columns either way.

Pick the side you query FROM most:
  employee.getRoles()     more common  →  put @JoinTable on Employee
  role.getEmployees()     more common  →  put @JoinTable on Role

Or pick the more "dominant" concept in your domain.
```

---

### Summary table

```
Relationship  Parent (non-owner)         Child / Owner               FK lives in
────────────  ─────────────────────────  ──────────────────────────  ───────────────────
1:1           Employee (@mappedBy)        SalaryAccount (@JoinColumn) salary_account table
1:M           Department (@mappedBy)      Employee (@JoinColumn)      employee table
M:M           Role (@mappedBy)            Employee (@JoinTable)       junction table (both FKs)
```

---

### Cannot tell 1:1 from 1:M in DDL without UNIQUE

A bare FK looks identical for both relationships:

```sql
-- Is this 1:1 or 1:M? You cannot tell from the FK alone.
CREATE TABLE salary_account (
    acct_id VARCHAR(10) PRIMARY KEY,
    e_id    VARCHAR(10),
    FOREIGN KEY (e_id) REFERENCES employee(e_id)
);
```

The **only distinguishing marker** is a `UNIQUE` constraint on the FK column:

```sql
-- 1:M — no UNIQUE → many salary_account rows can reference the same employee
e_id VARCHAR(10),
FOREIGN KEY (e_id) REFERENCES employee(e_id)

-- 1:1 — UNIQUE → enforces that only one row can reference a given employee
e_id VARCHAR(10) UNIQUE,
FOREIGN KEY (e_id) REFERENCES employee(e_id)
```

| What you see in DDL | Relationship |
|---|---|
| FK, no UNIQUE | 1:M — or a poorly written 1:1 (UNIQUE forgotten) |
| FK + UNIQUE | Definitively 1:1 |
| FK column = PK | 1:1 (PK already implies uniqueness) |

In practice `UNIQUE` on a FK is often forgotten — so DDL alone is frequently not enough.
You need application code or documentation to confirm the intended cardinality.

---

## Foreign Key Examples

### Example 1 — EMPLOYEE and DEPARTMENT

```
DEPARTMENT                    EMPLOYEE
+--------+---------+          +--------+---------+----------+
| D_ID   | D_NAME  |          | E_ID   | E_NAME  | D_ID     |
+--------+---------+          +--------+---------+----------+
| D01    | Engg    |          | E01    | Alice   | D01      |
| D02    | Mktg    |          | E02    | Bob     | D02      |
| D03    | HR      |          | E03    | Carol   | D01      |
+--------+---------+          +--------+---------+----------+
     ↑ Primary Key                               ↑ Foreign Key
```

- DEPARTMENT.D_ID = primary key
- EMPLOYEE.D_ID = foreign key → references DEPARTMENT.D_ID
- Carol and Alice both work in D01 (Engg)
- Foreign key enforces: you cannot assign an employee to D04 if D04 doesn't exist

---

### Example 2 — ORDER and CUSTOMER

```
CUSTOMER                      ORDER
+----------+----------+       +----------+----------+-------------+
| C_ID     | C_NAME   |       | O_ID     | O_DATE   | C_ID        |
+----------+----------+       +----------+----------+-------------+
| C01      | Alice    |       | O001     | 2024-01  | C01         |
| C02      | Bob      |       | O002     | 2024-02  | C01         |
| C03      | Carol    |       | O003     | 2024-03  | C02         |
+----------+----------+       +----------+----------+-------------+
     ↑ Primary Key                                  ↑ Foreign Key
```

- One customer can place many orders (1:M)
- ORDER.C_ID references CUSTOMER.C_ID
- Cannot create order for C99 if C99 doesn't exist → referential integrity

---

### Example 3 — Many-to-Many with Junction Table

```
EMPLOYEE              EMPLOYEE_ROLES           ROLES
+------+-------+      +------+--------+       +--------+----------+
| E_ID | NAME  |      | E_ID | R_ID   |       | R_ID   | R_NAME   |
+------+-------+      +------+--------+       +--------+----------+
| E01  | Alice |      | E01  | R01    |       | R01    | Manager  |
| E02  | Bob   |      | E01  | R02    |       | R02    | Dev      |
+------+-------+      | E02  | R01    |       | R03    | Analyst  |
                      +------+--------+       +--------+----------+
                        ↑FK    ↑FK
```

- EMPLOYEE_ROLES has TWO foreign keys: E_ID + R_ID
- Together they form a **composite primary key**
- Alice has both Manager and Dev roles
- Bob has Manager role

---

## ERD Crow's Foot Diagram (ASCII)

```
CUSTOMER          ORDER              ORDER_ITEM         PRODUCT
+--------+        +--------+         +----------+       +--------+
| C_ID PK|——||  O<| O_ID PK|——||  O<| OI_ID PK |>O——||  | P_ID PK|
| C_NAME |        | O_DATE |         | O_ID  FK |       | P_NAME |
| EMAIL  |        | C_ID FK|         | P_ID  FK |       | PRICE  |
+--------+        +--------+         | QTY      |       +--------+
                                     +----------+
```

- One customer → many orders
- One order → many order items
- One product → many order items

---

## Rules for Foreign Keys

| Rule | Meaning |
|---|---|
| Must reference a PK | FK value must exist in the parent table |
| Can be NULL | If relationship is optional |
| Can have multiple FKs | A table can reference many other tables |
| Prevents orphan records | Cannot delete a dept if employees reference it |
