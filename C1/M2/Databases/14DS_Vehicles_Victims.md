# DS — Vehicles & Victims Analysis

## Problem
**Which vehicles have affected the most victims (killed + injured)?**

Tables: `parties`, `collisions`

---

## Step 1 — Create a Cleaned View

```sql
CREATE OR REPLACE VIEW parties_vehicles_num_victims_cleaned AS (
    SELECT
        t1.case_id,
        party_number,
        statewide_vehicle_type,
        vehicle_make,
        killed_victims + injured_victims AS num_affected_victims
    FROM parties t1
    LEFT JOIN collisions t2 ON t1.case_id = t2.case_id
    WHERE at_fault = 1
      AND vehicle_year > 0
      AND vehicle_make != ''
      AND statewide_vehicle_type != ''
);
```

**Why each filter:**
```
at_fault = 1          →  only the party responsible for the collision
vehicle_year > 0      →  remove invalid/missing year entries
vehicle_make != ''    →  remove blank make entries
statewide_vehicle_type != '' →  remove blank type entries
```

**Why LEFT JOIN:**
- `parties` is the base — we want all at-fault parties
- `collisions` provides `killed_victims` and `injured_victims`
- LEFT JOIN ensures no party row is lost if join fails

---

## Q1 — Rank each vehicle make by risk score

```sql
SELECT
    vehicle_make,
    SUM(num_affected_victims)                              AS total_num_affected_victims,
    RANK() OVER (ORDER BY SUM(num_affected_victims) DESC) AS risk_score_rank
FROM parties_vehicles_num_victims_cleaned
GROUP BY vehicle_make
ORDER BY risk_score_rank;
```

**Why this works:**
```
GROUP BY vehicle_make           →  one row per make
SUM(num_affected_victims)       →  total victims across all incidents for that make
RANK() OVER (ORDER BY SUM DESC) →  rank makes from most to least harmful

Window function applied AFTER GROUP BY — each row in the grouped result
gets a rank based on its aggregated total
```

---

## Q2 — Rank each vehicle type + make combination within type

```sql
SELECT
    statewide_vehicle_type,
    vehicle_make,
    SUM(num_affected_victims)  AS total_num_affected_victims,
    RANK() OVER (
        PARTITION BY statewide_vehicle_type
        ORDER BY SUM(num_affected_victims) DESC
    )                          AS risk_score_rank
FROM parties_vehicles_num_victims_cleaned
GROUP BY statewide_vehicle_type, vehicle_make
ORDER BY statewide_vehicle_type, risk_score_rank;
```

**Why PARTITION BY statewide_vehicle_type:**
```
Without PARTITION BY  →  one global rank across all types
                          (a Sedan make vs a Motorcycle make — unfair comparison)

With PARTITION BY     →  rank resets within each vehicle type
                          rank 1 in Sedan = most dangerous Sedan make
                          rank 1 in Motorcycle = most dangerous Motorcycle make
```

**Example output:**
```
statewide_vehicle_type  vehicle_make  total_victims  risk_score_rank
Passenger Car           Toyota        5200           1
Passenger Car           Honda         4800           2
Passenger Car           Ford          4500           3
Motorcycle              Harley        320            1   ← resets for Motorcycle
Motorcycle              Yamaha        280            2
```

---

## Key Concepts Used

| Concept | Where used | Why |
|---|---|---|
| `CREATE OR REPLACE VIEW` | Step 1 | Reusable cleaned subset — avoids rewriting complex JOIN+WHERE every time |
| `LEFT JOIN` | View | Keep all party rows even if collision join fails |
| `killed + injured AS num_affected_victims` | View | Derived column combining two measures |
| `GROUP BY` | Q1, Q2 | Aggregate per make / per type+make |
| `SUM` inside `RANK() OVER` | Q1, Q2 | Rank on aggregated value — window applied after grouping |
| `PARTITION BY` | Q2 only | Independent ranking within each vehicle type |

---

## Gotcha — Window function on aggregated column

```sql
-- You cannot use the alias in RANK() OVER:
RANK() OVER (ORDER BY total_num_affected_victims DESC)   -- ✗ alias not yet defined

-- Must repeat the expression:
RANK() OVER (ORDER BY SUM(num_affected_victims) DESC)    -- ✓
```

This follows from execution order — SELECT (where alias is defined) runs after window functions.
