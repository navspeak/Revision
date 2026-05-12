# SQL — Subqueries, CTEs and Views

---

## Subqueries (Inner Queries)

A subquery is a query nested inside another query. Can appear in three places:

```
WHERE clause  — filter rows based on another query's result
FROM clause   — use inner query result as a temporary table
SELECT clause — compute a value per row
```

---

### Subquery in FROM clause

Inner query runs first, result acts as a temporary table. **Must be aliased.**

```sql
-- English movies with duration > 80
SELECT movie_title
FROM (
    SELECT movie_title, duration
    FROM movie_main
    WHERE language = 'English'
) AS iq                          -- alias is mandatory
WHERE duration > 80;
```

```sql
-- Average of max gross per language
SELECT AVG(max_gross) AS average_max_gross
FROM (
    SELECT language, MAX(gross) AS max_gross
    FROM movie_main
    GROUP BY language
) AS max_gross_by_language;
```

---

### Subquery in WHERE clause (with IN)

```sql
-- Movies with IMDB > 8
SELECT movie_title
FROM movie_main
WHERE movie_title IN (
    SELECT movie_title
    FROM movie_info
    WHERE imdb > 8
);
```

**Gotcha — LIMIT inside IN does not work:**
```sql
-- WRONG:
WHERE movie_title IN (SELECT movie_title FROM movie_info LIMIT 10)  -- ✗ error

-- IN does not support LIMIT inside the subquery in MySQL
-- Use a JOIN or CTE instead
```

---

### When subqueries get painful

```
Hard to read when deeply nested
Result needed multiple times → must rewrite the subquery each time
```

Solution → **CTE** (once) or **View** (many times across sessions).

---

## CTE — Common Table Expression

A named temporary result set that exists **only for the duration of the query**.

```sql
WITH <cte_name> AS (
    -- subquery / definition
)
SELECT ...
FROM <cte_name>
WHERE ...;
```

**Example — high IMDB movies:**
```sql
WITH high_imdb AS (
    SELECT movie_title, imdb
    FROM movie_info
    WHERE imdb > 8
)
SELECT movie_title FROM high_imdb;

-- Reuse the same CTE in the same query:
WITH high_imdb AS (
    SELECT movie_title, imdb
    FROM movie_info
    WHERE imdb > 8
)
SELECT COUNT(*) AS total_high_imdb FROM high_imdb;
```

**Multiple CTEs:**
```sql
WITH
  english_movies AS (
      SELECT movie_title, duration FROM movie_main WHERE language = 'English'
  ),
  long_movies AS (
      SELECT movie_title FROM english_movies WHERE duration > 80
  )
SELECT * FROM long_movies;
```

**Properties:**
```
Lives in memory only while the query runs
Can be referenced multiple times in the SAME query
Cannot be used across different queries (use View for that)
Improves readability over deeply nested subqueries
```

---

## Views

A **virtual table** stored as a saved query definition in the database.

```sql
CREATE VIEW <view_name> AS
SELECT column(s)
FROM table
WHERE condition;
```

**Example:**
```sql
CREATE VIEW high_imdb_movies AS
SELECT movie_title, imdb
FROM movie_info
WHERE imdb > 8;

-- Use like any table:
SELECT * FROM high_imdb_movies;
SELECT COUNT(*) FROM high_imdb_movies;
SELECT movie_title FROM high_imdb_movies WHERE imdb > 9;
```

**Key notes:**
```
Virtual table — no separate storage of rows
MySQL saves only the query definition, not the data
Every time you query the view, MySQL reruns the definition
Can be queried like a regular table (SELECT, JOIN, WHERE etc.)
Can be updated or dropped:  DROP VIEW high_imdb_movies;
```

**Data security use case:**
```
Confidential table has columns: salary, SSN, name, dept
Create a view with only name and dept → share view with user
User sees only name + dept, never sees salary or SSN
Main table stays hidden
```

---

## CTE vs View vs Subquery

| | Subquery | CTE | View |
|---|---|---|---|
| Syntax | Nested inside query | `WITH name AS (...)` | `CREATE VIEW name AS` |
| Lifespan | Single query | Single query | Persists in DB until dropped |
| Reuse in same query | ❌ rewrite each time | ✅ reference by name | ✅ reference by name |
| Reuse across queries | ❌ | ❌ | ✅ |
| Stored in DB | ❌ | ❌ | ✅ (definition only) |
| Readability | Poor (deeply nested) | Good | Good |
| Security | ❌ | ❌ | ✅ hide columns/rows |

```
Use subquery  →  simple one-off filter, short and readable
Use CTE       →  complex logic needed once, want readable code
Use View      →  same subset needed repeatedly across multiple queries/sessions
```

---

## ERD — Collisions Dataset

```
COLLISIONS                          PARTIES
+------------------+---------+      +------------------+---------+
| case_id       PK | VARCHAR |      | case_id       FK | VARCHAR |
| county_location  | VARCHAR |      | cellphone_in_use | BOOLEAN |
| ...              |         |      | cellphone_use_type| VARCHAR|
+------------------+---------+      | at_fault         | BOOLEAN |
                                    | party_age         | INT     |
                                    | ...               |         |
                                    +------------------+---------+

COLLISIONS ||——O< PARTIES

One collision → many parties (1:M)
FK: parties.case_id → collisions.case_id
```

---

## Real Queries — Collisions Dataset

**Q1 — Average age of at-fault parties in Los Angeles:**
```sql
SELECT AVG(party_age) AS avg_party_age
FROM parties
JOIN collisions USING (case_id)     -- USING when column name is same in both tables
WHERE at_fault = 1
  AND county_location = 'Los Angeles';
```

**Q2 — Frequency and average age per cellphone use type (at-fault, Los Angeles):**
```sql
SELECT
    cellphone_use_type,
    COUNT(*)         AS num_fault_parties,
    AVG(party_age)   AS avg_party_age
FROM parties
JOIN collisions USING (case_id)
WHERE at_fault = 1
  AND county_location = 'Los Angeles'
GROUP BY cellphone_use_type
ORDER BY cellphone_use_type;
```

**Same Q2 using subquery in WHERE:**
```sql
SELECT cellphone_use_type, AVG(party_age), COUNT(P.case_id)
FROM parties P
WHERE at_fault = 1
  AND P.case_id IN (
      SELECT case_id
      FROM collisions
      WHERE county_location = 'Los Angeles'
  )
GROUP BY cellphone_use_type;
```

**Rule:** Every non-aggregated column in SELECT must appear in GROUP BY.
```
cellphone_use_type  →  in GROUP BY  ✓
COUNT(*)            →  aggregate    ✓
AVG(party_age)      →  aggregate    ✓
```
