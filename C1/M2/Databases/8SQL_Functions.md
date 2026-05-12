# SQL — Scalar Functions

A **scalar function** returns one value per row (operates on each row individually).

Three categories:
```
String functions    — manipulate text
Date-time functions — manipulate dates and times
REGEX               — pattern matching
```

---

## String Functions

### UPPER / LOWER

```sql
SELECT UPPER('hello');          -- HELLO
SELECT LOWER('HELLO');          -- hello

SELECT UPPER(name) FROM employee;
-- Alice → ALICE
-- bob   → BOB
```

---

### LENGTH

```sql
SELECT LENGTH('hello');         -- 5
SELECT LENGTH('');              -- 0

SELECT name, LENGTH(name) AS name_length FROM employee;
-- Alice → 5
-- Bob   → 3
```

---

### CONCAT

```sql
SELECT CONCAT('Hello', ' ', 'World');          -- Hello World
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM employee;

-- MySQL also supports || in some modes, but CONCAT is safer
SELECT CONCAT('Emp: ', emp_id, ' - ', name) FROM employee;
-- Emp: E01 - Alice
```

**Gotcha:** If any argument is NULL, CONCAT returns NULL.
```sql
SELECT CONCAT('Hello', NULL, 'World');   -- NULL

-- Use CONCAT_WS (with separator) to handle NULLs safely:
SELECT CONCAT_WS(' ', first_name, middle_name, last_name);
-- skips NULL values automatically
```

---

### REVERSE

```sql
SELECT REVERSE('hello');        -- olleh
SELECT REVERSE('12345');        -- 54321

SELECT name, REVERSE(name) FROM employee;
-- Alice → ecilA
```

---

### SUBSTRING

Returns part of a string.

```sql
-- SUBSTRING(string, start, length)
-- start position is 1-based (not 0)

SELECT SUBSTRING('Hello World', 1, 5);    -- Hello
SELECT SUBSTRING('Hello World', 7, 5);    -- World
SELECT SUBSTRING('Hello World', 7);       -- World  (no length = till end)

SELECT SUBSTRING(email, 1, 3) FROM employee;
-- alice@gmail.com → ali
```

**Negative start (from end):**
```sql
SELECT SUBSTRING('Hello World', -5);      -- World  (last 5 chars)
```

---

### SUBSTRING_INDEX

Splits a string by a delimiter and returns part of it.

```sql
-- SUBSTRING_INDEX(string, delimiter, count)
-- count > 0 → read from LEFT,  return left side  (before Nth delimiter)
-- count < 0 → read from RIGHT, return right side (after Nth delimiter from right)

SELECT SUBSTRING_INDEX('alice@gmail.com', '@', 1);   -- alice
SELECT SUBSTRING_INDEX('alice@gmail.com', '@', -1);  -- gmail.com
```

**Count direction visualised:**
```
'a.b.c.d'
 ↑ ↑ ↑
 1 2 3      from left  →  SUBSTRING_INDEX('a.b.c.d', '.',  2) = a.b
     ↑ ↑ ↑
     3 2 1  from right →  SUBSTRING_INDEX('a.b.c.d', '.', -2) = c.d

Positive → return LEFT  side up to Nth delimiter
Negative → return RIGHT side after Nth delimiter from right
```

```sql
SELECT SUBSTRING_INDEX('a.b.c.d', '.', 1);    -- a
SELECT SUBSTRING_INDEX('a.b.c.d', '.', 2);    -- a.b
SELECT SUBSTRING_INDEX('a.b.c.d', '.', 3);    -- a.b.c
SELECT SUBSTRING_INDEX('a.b.c.d', '.', -1);   -- d
SELECT SUBSTRING_INDEX('a.b.c.d', '.', -2);   -- c.d
SELECT SUBSTRING_INDEX('a.b.c.d', '.', -3);   -- b.c.d
```

**Gotcha — count beyond available delimiters returns full string:**
```sql
-- 'alice@gmail.com' has only ONE @
SUBSTRING_INDEX('alice@gmail.com', '@', 2)    -- alice@gmail.com (no 2nd @ → full string)
```

**Practical use — extract domain from email:**
```sql
SELECT
    email,
    SUBSTRING_INDEX(email, '@', 1)  AS username,
    SUBSTRING_INDEX(email, '@', -1) AS domain
FROM employee;
-- alice@gmail.com  →  alice  |  gmail.com
```

---

## Quick Reference

| Function | Syntax | Example | Result |
|---|---|---|---|
| `UPPER` | `UPPER(str)` | `UPPER('hello')` | `HELLO` |
| `LOWER` | `LOWER(str)` | `LOWER('HELLO')` | `hello` |
| `LENGTH` | `LENGTH(str)` | `LENGTH('hello')` | `5` |
| `CONCAT` | `CONCAT(s1, s2, ...)` | `CONCAT('Hi', ' ', 'Bob')` | `Hi Bob` |
| `REVERSE` | `REVERSE(str)` | `REVERSE('abc')` | `cba` |
| `SUBSTRING` | `SUBSTRING(str, start, len)` | `SUBSTRING('Hello', 1, 3)` | `Hel` |
| `SUBSTRING_INDEX` | `SUBSTRING_INDEX(str, delim, n)` | `SUBSTRING_INDEX('a@b.com','@',1)` | `a` |

---

## COALESCE

Returns the **first non-NULL value** from a list of arguments.

```sql
-- COALESCE(val1, val2, val3, ...)
SELECT COALESCE(NULL, NULL, 'hello', 'world');   -- hello  (first non-NULL)
SELECT COALESCE(NULL, NULL, NULL);               -- NULL   (all NULL → returns NULL)
SELECT COALESCE('first', 'second');              -- first  (already non-NULL)
```

**Practical use — fallback values:**
```sql
-- Use middle_name if exists, else 'N/A'
SELECT COALESCE(middle_name, 'N/A') FROM employee;

-- Use mobile, else landline, else 'No contact'
SELECT COALESCE(mobile, landline, 'No contact') AS contact FROM employee;

-- Replace NULL salary with 0
SELECT name, COALESCE(salary, 0) AS salary FROM employee;
```

**COALESCE vs IFNULL:**
```sql
-- IFNULL — two arguments only, MySQL specific
SELECT IFNULL(NULL, 'fallback');              -- fallback

-- COALESCE — multiple arguments, standard SQL (MySQL, PostgreSQL, SQL Server)
SELECT COALESCE(NULL, NULL, 'fallback');      -- fallback

IFNULL(a, b)  =  COALESCE(a, b)   when two args — same result
```

Prefer `COALESCE` — standard SQL, works across all databases.

---

## Combining String Functions

```sql
-- Capitalise first letter only
SELECT CONCAT(UPPER(SUBSTRING(name, 1, 1)), LOWER(SUBSTRING(name, 2))) FROM employee;
-- ALICE → Alice,  bOB → Bob

-- Extract username from email
SELECT SUBSTRING_INDEX(email, '@', 1) AS username FROM employee;

-- Name length > 4
SELECT * FROM employee WHERE LENGTH(name) > 4;
```

---

## Date-Time Functions

### Getting Current Date / Time

```sql
SELECT NOW();               -- 2026-05-12 14:30:00  (date + time)
SELECT CURDATE();           -- 2026-05-12           (date only)
SELECT CURTIME();           -- 14:30:00             (time only)
SELECT CURRENT_TIMESTAMP;   -- same as NOW()
```

---

### YEAR / MONTH / DAY

```sql
SELECT YEAR('2026-05-12');      -- 2026
SELECT MONTH('2026-05-12');     -- 5
SELECT DAY('2026-05-12');       -- 12

-- From a column
SELECT YEAR(order_date), MONTH(order_date) FROM orders;

-- Orders placed in May
SELECT * FROM orders WHERE MONTH(order_date) = 5;
```

---

### DATE_FORMAT

Formats a date into a custom string.

```sql
-- DATE_FORMAT(date, format)
SELECT DATE_FORMAT('2026-05-12', '%d-%m-%Y');     -- 12-05-2026
SELECT DATE_FORMAT('2026-05-12', '%M %d, %Y');    -- May 12, 2026
SELECT DATE_FORMAT(NOW(), '%H:%i:%s');            -- 14:30:00

-- Common format codes:
-- %Y  four-digit year      2026
-- %y  two-digit year       26
-- %M  full month name      May
-- %m  month number         05
-- %d  day number           12
-- %H  hour (24h)           14
-- %h  hour (12h)           02
-- %i  minutes              30
-- %s  seconds              00
```

---

### DATEDIFF / TIMESTAMPDIFF

```sql
-- DATEDIFF — difference in days
SELECT DATEDIFF('2026-05-12', '2026-01-01');      -- 131 days

SELECT DATEDIFF(NOW(), hire_date) AS days_employed FROM employee;

-- TIMESTAMPDIFF — difference in any unit
SELECT TIMESTAMPDIFF(YEAR,  '2000-05-12', NOW());   -- age in years
SELECT TIMESTAMPDIFF(MONTH, '2026-01-01', NOW());   -- months difference
SELECT TIMESTAMPDIFF(DAY,   '2026-01-01', NOW());   -- days difference
```

---

### DATE_ADD / DATE_SUB

```sql
-- DATE_ADD(date, INTERVAL n unit)
SELECT DATE_ADD('2026-05-12', INTERVAL 7 DAY);     -- 2026-05-19
SELECT DATE_ADD('2026-05-12', INTERVAL 1 MONTH);   -- 2026-06-12
SELECT DATE_ADD('2026-05-12', INTERVAL 1 YEAR);    -- 2027-05-12

-- DATE_SUB
SELECT DATE_SUB('2026-05-12', INTERVAL 30 DAY);    -- 2026-04-12

-- Orders from last 30 days
SELECT * FROM orders WHERE order_date >= DATE_SUB(NOW(), INTERVAL 30 DAY);
```

---

### Date-Time Quick Reference

| Function | Returns | Example | Result |
|---|---|---|---|
| `NOW()` | Date + time | `NOW()` | `2026-05-12 14:30:00` |
| `CURDATE()` | Date only | `CURDATE()` | `2026-05-12` |
| `CURTIME()` | Time only | `CURTIME()` | `14:30:00` |
| `YEAR(d)` | Year number | `YEAR('2026-05-12')` | `2026` |
| `MONTH(d)` | Month number | `MONTH('2026-05-12')` | `5` |
| `DAY(d)` | Day number | `DAY('2026-05-12')` | `12` |
| `DATE_FORMAT(d,f)` | Formatted string | `DATE_FORMAT(d,'%M %Y')` | `May 2026` |
| `DATEDIFF(d1,d2)` | Days between | `DATEDIFF(d1,d2)` | `131` |
| `TIMESTAMPDIFF(u,d1,d2)` | Diff in unit | `TIMESTAMPDIFF(YEAR,...)` | `2` |
| `DATE_ADD(d,INTERVAL n u)` | New date | `DATE_ADD(d, INTERVAL 7 DAY)` | `+7 days` |
| `DATE_SUB(d,INTERVAL n u)` | New date | `DATE_SUB(d, INTERVAL 1 MONTH)` | `-1 month` |

---

## REGEX

Pattern matching in `WHERE` clauses using `REGEXP` (MySQL) or `~` (PostgreSQL).

### Basic Syntax

```sql
SELECT * FROM employee WHERE name REGEXP 'pattern';
-- MySQL:      REGEXP or RLIKE
-- PostgreSQL: ~ (case sensitive)  or  ~* (case insensitive)
```

---

### Common Patterns

```sql
-- Starts with 'A'
SELECT * FROM employee WHERE name REGEXP '^A';

-- Ends with 'n'
SELECT * FROM employee WHERE name REGEXP 'n$';

-- Contains 'ali' anywhere
SELECT * FROM employee WHERE name REGEXP 'ali';

-- Exactly 5 characters
SELECT * FROM employee WHERE name REGEXP '^.{5}$';

-- Only letters (no numbers or symbols)
SELECT * FROM employee WHERE name REGEXP '^[A-Za-z]+$';

-- Starts with A, B or C
SELECT * FROM employee WHERE name REGEXP '^[ABC]';

-- Valid email pattern
SELECT * FROM employee WHERE email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';

-- Phone: digits only, exactly 10
SELECT * FROM employee WHERE phone REGEXP '^[0-9]{10}$';
```

---

### REGEX Pattern Reference

| Pattern | Meaning | Example | Matches |
|---|---|---|---|
| `^` | Start of string | `^A` | Alice, Arpit |
| `$` | End of string | `n$` | John, Ben |
| `.` | Any single character | `a.c` | abc, aXc |
| `*` | 0 or more of preceding | `ab*` | a, ab, abbb |
| `+` | 1 or more of preceding | `ab+` | ab, abbb (not a) |
| `?` | 0 or 1 of preceding | `ab?` | a, ab |
| `{n}` | Exactly n times | `a{3}` | aaa |
| `{n,m}` | Between n and m times | `a{2,4}` | aa, aaa, aaaa |
| `[abc]` | Any one of a, b, c | `[ABC]` | A, B, or C |
| `[^abc]` | Not a, b, or c | `[^0-9]` | any non-digit |
| `[A-Z]` | Range | `[A-Za-z]` | any letter |
| `\d` | Digit (PostgreSQL) | `\d+` | 123 |
| `\|` | OR | `cat\|dog` | cat or dog |

---

### REGEXP vs LIKE

```sql
-- LIKE — simple pattern, only two wildcards
SELECT * FROM employee WHERE name LIKE 'A%';      -- starts with A
SELECT * FROM employee WHERE name LIKE '_ob';     -- any char + ob (Bob, Rob)

-- REGEXP — full pattern matching, much more powerful
SELECT * FROM employee WHERE name REGEXP '^A';    -- starts with A
SELECT * FROM employee WHERE name REGEXP '^[A-C]'; -- starts with A, B or C
```

| | `LIKE` | `REGEXP` |
|---|---|---|
| Wildcards | `%` (any), `_` (one char) | Full regex patterns |
| Power | Simple | Full pattern matching |
| Performance | Faster | Slower on large tables |
| Use when | Simple prefix/suffix match | Complex pattern needed |

---

## BETWEEN vs < >

**`BETWEEN` is always inclusive on both ends.**

```sql
-- These are identical:
SELECT * FROM employee WHERE salary BETWEEN 3000 AND 7000;
SELECT * FROM employee WHERE salary >= 3000 AND salary <= 7000;
-- both include 3000 and 7000
```

**Exclusive bounds — must use < >:**
```sql
-- BETWEEN cannot do this:
SELECT * FROM employee WHERE salary > 3000 AND salary < 7000;
-- excludes 3000 and 7000 exactly
```

**NOT BETWEEN:**
```sql
SELECT * FROM employee WHERE salary NOT BETWEEN 3000 AND 7000;
-- same as: salary < 3000 OR salary > 7000
```

**Date trap — BETWEEN misses times on the end date:**
```sql
-- Looks right but misses orders at 14:30 on 2026-05-12
-- '2026-05-12' is treated as '2026-05-12 00:00:00'
SELECT * FROM orders WHERE order_date BETWEEN '2026-01-01' AND '2026-05-12';

-- Safe version — use < next day instead:
SELECT * FROM orders WHERE order_date >= '2026-01-01' AND order_date < '2026-05-13';
```

**Summary:**

| | `BETWEEN a AND b` | `>= a AND <= b` | `> a AND < b` |
|---|---|---|---|
| Includes a | ✅ | ✅ | ❌ |
| Includes b | ✅ | ✅ | ❌ |
| Readable | ✅ cleaner | ✅ | ✅ |
| Exclusive bounds | ❌ | ❌ | ✅ |

```
BETWEEN  →  always inclusive, cleaner syntax  →  simple range checks
< >      →  full control over boundaries      →  when excluding endpoints or using datetimes
```
