# Multivariable Functions

## What is a Multivariable Function?

A function that takes **more than one variable as input** and returns a single output.

```
Univariate:     f(x)       → one input,   one output
Multivariable:  f(x, y)    → two inputs,  one output
                f(x, y, z) → three inputs, one output
```

---

## Examples

### Two variables
```
f(x, y) = x² + y²

For x=1, y=2:
f(1, 2) = 1² + 2² = 1 + 4 = 5
```

### Three variables
```
g(x, y, z) = x² + 2y + 3z

For x=1, y=2, z=3:
g(1, 2, 3) = 1 + 4 + 9 = 14
```

---

## Why Multivariable in ML?

In ML, model parameters are always multiple — a neural network can have millions.

```
Loss = f(w₁, w₂, w₃, ... , wₙ)
```

Training = minimising this multivariable function over all weights simultaneously.

Every real-world system depends on more than one factor:
- House price = f(size, location, bedrooms, age, ...)
- Disease risk = f(age, weight, diet, exercise, ...)

---

## Visualising f(x, y)

For a single variable f(x) → 2D curve.
For two variables f(x, y) → 3D surface.

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)

Z = X**2 + Y**2    # f(x,y) = x² + y²

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x,y)')
ax.set_title('f(x,y) = x² + y²')
plt.show()
```

f(x,y) = x² + y² is a **bowl shape** — minimum at origin (0,0). This is the classic shape of a loss function in ML.

---

## Domain and Range

For f(x, y) = x² + y²:

- **Domain** = set of all valid inputs = R² (all real (x,y) pairs)
- **Range** = set of all possible outputs = R (all real numbers ≥ 0 here)

The graph is the set of all points **(x, y, f(x,y))** — a surface in 3D space.

---

## What the Surface Tells You

```
f(x,y) = x² + y²

         z
         |    *
         |   ***
         |  *****   ← high values far from origin
         | *******
         |******* *
         +----------> y
        /
       x
```

- **Peaks** — local maxima (high points)
- **Valleys** — local minima (low points)
- **Saddle points** — looks like a min from one direction, max from another

```
Saddle point example: f(x,y) = x² - y²

Along x-axis: x² → minimum at origin
Along y-axis: -y² → maximum at origin
→ origin is a saddle point — neither max nor min
```

---

## Higher Dimensions

Beyond f(x,y) — 3 or more inputs — we can't visualise directly.

Instead we use:
- **Contour plots** — 2D slices of the 3D surface (like a map with elevation lines)
- **Heatmaps** — colour represents function value

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2

plt.contourf(X, Y, Z, levels=20, cmap='viridis')
plt.colorbar(label='f(x,y)')
plt.title('Contour plot of f(x,y) = x² + y²')
plt.xlabel('x'); plt.ylabel('y')
plt.show()
```

Contour lines = points of equal output value. Closer lines = steeper surface.

---

## Key Difference from Univariate

| | Univariate f(x) | Multivariable f(x,y) |
|---|---|---|
| Input | Single number | Ordered pair (x, y) |
| Graph | 2D curve | 3D surface |
| Derivative | f'(x) | Partial derivatives ∂f/∂x, ∂f/∂y |
| Minimum | Single point x | Point (x, y) in 2D space |
