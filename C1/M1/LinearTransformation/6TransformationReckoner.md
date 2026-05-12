# Transformation Matrix — Ready Reckoner

## Rotation (anticlockwise by angle θ)
```
R = [[cos θ,  -sin θ],
     [sin θ,   cos θ]]
```
| θ | Matrix |
|---|--------|
| 90°  | [[0, -1], [1,  0]] |
| 180° | [[-1, 0], [0, -1]] |
| 270° | [[0,  1], [-1, 0]] |

- det = 1 — area preserved
- Origin fixed
- Shape unchanged, just rotated

---

## Dilation (Scaling)
```
D = [[sx, 0 ],
     [0,  sy]]
```
| Type | Matrix |
|------|--------|
| Uniform scale ×k | [[k, 0], [0, k]] |
| Stretch x only   | [[k, 0], [0, 1]] |
| Stretch y only   | [[1, 0], [0, k]] |
| Shrink           | [[0.5, 0], [0, 0.5]] |

- det = sx × sy
- det > 1 → stretch, 0 < det < 1 → shrink

---

## Shear
```
Horizontal:          Vertical:
Sh = [[1, k],        Sv = [[1, 0],
      [0, 1]]              [k, 1]]
```
- Horizontal: x shifts by k×y, y unchanged
- Vertical:   y shifts by k×x, x unchanged
- det = 1 always — area preserved

---

## Reflection
```
About x-axis:    About y-axis:    About y=x:
[[1,  0],        [[-1, 0],        [[0, 1],
 [0, -1]]         [ 0, 1]]         [1, 0]]
```
| About | Matrix |
|-------|--------|
| x-axis  | [[1, 0], [0, -1]] |
| y-axis  | [[-1, 0], [0, 1]] |
| y = x   | [[0, 1], [1, 0]]  |
| origin  | [[-1, 0], [0, -1]] |

- det = -1 — area preserved, orientation **flipped**

---

## Summary Table

| Transformation | det | Area | Orientation |
|----------------|-----|------|-------------|
| Rotation       | 1   | preserved | preserved |
| Dilation (k>1) | k²  | scaled    | preserved |
| Shear          | 1   | preserved | preserved |
| Reflection     | -1  | preserved | flipped   |
