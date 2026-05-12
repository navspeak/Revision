import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Shape: a simple arrow-like polygon so rotation/reflection are obvious
shape = np.array([
    [0, 0],
    [2, 0],
    [2, 0.5],
    [3, 1],
    [2, 1.5],
    [2, 1],
    [0, 1],
    [0, 0]
]).T  # shape (2, N)

transformations = {
    "Rotation 90°":   np.array([[0, -1], [1,  0]]),
    "Dilation ×1.5":  np.array([[1.5, 0], [0, 1.5]]),
    "Shear (k=1)":    np.array([[1, 1], [0, 1]]),
    "Reflection\n(about x-axis)": np.array([[1, 0], [0, -1]]),
}

fig, axes = plt.subplots(2, 4, figsize=(16, 7))
fig.suptitle("Matrix Transformations — Ready Reckoner", fontsize=14, fontweight='bold')

colors = ["steelblue", "seagreen", "darkorange", "crimson"]

for col, (name, A) in enumerate(transformations.items()):
    transformed = A @ shape

    ax_before = axes[0, col]
    ax_after  = axes[1, col]

    # Before
    ax_before.fill(shape[0], shape[1], alpha=0.4, color=colors[col])
    ax_before.plot(shape[0], shape[1], color=colors[col], linewidth=1.5)
    ax_before.set_title(f"{name}", fontsize=10, fontweight='bold')
    ax_before.set_ylabel("Before" if col == 0 else "")

    # After
    ax_after.fill(transformed[0], transformed[1], alpha=0.4, color=colors[col])
    ax_after.plot(transformed[0], transformed[1], color=colors[col], linewidth=1.5)
    ax_after.set_ylabel("After" if col == 0 else "")

    # Matrix label
    mat_str = f"A = {A.tolist()}"
    ax_after.set_xlabel(mat_str, fontsize=8)

    for ax in [ax_before, ax_after]:
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("6TransformationVisual.png", dpi=150)
plt.show()
print("Saved: 6TransformationVisual.png")
