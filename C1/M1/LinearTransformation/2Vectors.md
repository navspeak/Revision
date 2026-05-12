# Vectors — Recap

## Data Representation
- Vectors represent real-life data sets
- Plotting vectors helps visualise and study data

## Vector Properties
- **Magnitude** — length/size of a vector
- **Angle** — direction in space

## Operations on Vectors
- **Addition** — tip-to-tail combination of two vectors
- **Scalar multiplication** — stretches or shrinks a vector; flips direction if negative
- **Dot product** — measures how much two vectors point in the same direction
  - a · b = |a| |b| cos(θ)
  - If dot product = 0 → vectors are perpendicular (orthogonal)
- **Norm** — length of a vector; ||v|| = √(v · v)
- **Cross product** — a × b gives a vector perpendicular to both a and b (3D only)
  - a × b = [a2b3-a3b2, a3b1-a1b3, a1b2-a2b1]
  - |a × b| = |a| |b| sin(θ) — equals area of parallelogram formed by a and b
  - If cross product = 0 → vectors are parallel
  - Dot product tells how parallel; cross product tells how perpendicular
  - The cross product a × b gives a vector that points perpendicular (90°) to the plane containing both a and b.
  - Right-hand rule: Point fingers along a, curl them toward b — your thumb points in the direction of a × b.
```
          a × b (up)
            ↑
            |
            |
      b ----+---→
           /
          /
         ↙
        a

  Its magnitude = |a| |b| sin(θ) — the area of the parallelogram formed by a and b.

  - θ = 0° → sin(0) = 0 → vectors are parallel → cross product = zero vector
  - θ = 90° → sin(90°) = 1 → maximum cross product
  ┌──────────┬───────────────────────────┬───────────────────────┐
  │          │        Dot Product        │     Cross Product     │
  ├──────────┼───────────────────────────┼───────────────────────┤
  │ Result   │ Scalar (number)           │ Vector                │
  ├──────────┼───────────────────────────┼───────────────────────┤
  │ Meaning  │ How aligned               │ Perpendicular to both │
  ├──────────┼───────────────────────────┼───────────────────────┤
  │ If 0     │ Vectors are perpendicular │ Vectors are parallel  │
  ├──────────┼───────────────────────────┼───────────────────────┤
  │ Works in │ Any dimension             │ 3D only               │
  └──────────┴───────────────────────────┴───────────────────────┘
```
  - Real uses:
    - Graphics/physics — finding the normal to a surface (which way a face is pointing)
    - Robotics — computing torque and rotation axes
    - ML — rarely used directly, but underpins 3D geometry and some computer vision

  - Think of it this way: dot product tells you how parallel two vectors are; cross product tells you how perpendicular they are.

## Basis Vectors
- Standard basis in 3D space: **î, ĵ, k̂** (unit vectors along x, y, z axes)
- Basis vectors are not unique — there is a choice
- Any vector in the space can be written as a linear combination of basis vectors

## Linear Combinations & Span
- **Linear combination**: c₁v₁ + c₂v₂ + ... for scalars c₁, c₂, ...
- **Span**: the set of all vectors reachable via linear combinations of a given set
- Basis vectors span the entire space they define
