import numpy as np
import matplotlib.pyplot as plt

def apply_matrix(A, points):
    return A @ points

# Grid of input points
x = np.linspace(-2, 2, 10)
y = np.linspace(-2, 2, 10)
xx, yy = np.meshgrid(x, y)
points = np.vstack([xx.ravel(), yy.ravel()])

# Matrices
singular     = np.array([[1, 2], [2, 4]])   # det = 0
non_singular = np.array([[2, 1], [1, 3]])   # det = 5

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Singular vs Non-Singular Matrix Transformation", fontsize=14)

def plot_points(ax, pts, title, color):
    ax.scatter(pts[0], pts[1], s=10, alpha=0.5, color=color)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

# Row 1 — Singular
plot_points(axes[0, 0], points, "Singular: Input (2D grid)\nA = [[1,2],[2,4]]  det=0", "steelblue")
transformed_s = apply_matrix(singular, points)
plot_points(axes[0, 1], transformed_s, "Singular: Output — collapsed onto line y=2x\nAll 2D points → single line", "crimson")

# draw the line y=2x
lx = np.linspace(-5, 5, 100)
axes[0, 1].plot(lx, 2 * lx, 'k--', linewidth=1.5, label='y = 2x')
axes[0, 1].legend()

# Row 2 — Non-Singular
plot_points(axes[1, 0], points, "Non-Singular: Input (2D grid)\nA = [[2,1],[1,3]]  det=5", "steelblue")
transformed_ns = apply_matrix(non_singular, points)
plot_points(axes[1, 1], transformed_ns, "Non-Singular: Output — stretched but still 2D\nEvery output maps back to one input", "seagreen")

plt.tight_layout()
plt.savefig("2InverseVisualization.png", dpi=150)
plt.show()
print("Saved as 2InverseVisualization.png")
