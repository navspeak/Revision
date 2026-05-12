import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Standard Basis — What [1,0] and [0,1] Mean", fontsize=13)

# --- Plot 1: Just the basis vectors ---
ax = axes[0]
ax.set_title("î and ĵ — Standard Basis")
ax.annotate("", xy=(1,0), xytext=(0,0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2.5))
ax.annotate("", xy=(0,1), xytext=(0,0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2.5))
ax.text(1.05, 0.05, "î = [1,0]", color="steelblue", fontsize=11)
ax.text(0.05, 1.05, "ĵ = [0,1]", color="crimson", fontsize=11)

# --- Plot 2: Any vector as combination ---
ax = axes[1]
ax.set_title("v = [3,5] = 3î + 5ĵ")
# 3 steps along x
ax.annotate("", xy=(3,0), xytext=(0,0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2, linestyle="dashed"))
# 5 steps along y from (3,0)
ax.annotate("", xy=(3,5), xytext=(3,0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2, linestyle="dashed"))
# final vector
ax.annotate("", xy=(3,5), xytext=(0,0), arrowprops=dict(arrowstyle="->", color="green", lw=2.5))
ax.text(1.5, -0.3, "3 × î", color="steelblue", fontsize=10)
ax.text(3.1, 2.5,  "5 × ĵ", color="crimson",   fontsize=10)
ax.text(1.2, 3.0,  "v=[3,5]", color="green",    fontsize=11)

# --- Plot 3: What happens without standard basis ---
ax = axes[2]
ax.set_title("Non-standard basis\nv₁=[2,1], v₂=[-1,2]")
v1 = np.array([2, 1])
v2 = np.array([-1, 2])
ax.annotate("", xy=v1, xytext=(0,0), arrowprops=dict(arrowstyle="->", color="steelblue", lw=2.5))
ax.annotate("", xy=v2, xytext=(0,0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2.5))
ax.text(v1[0]+0.1, v1[1]+0.1, "v₁=[2,1]", color="steelblue", fontsize=10)
ax.text(v2[0]-0.5, v2[1]+0.1, "v₂=[-1,2]", color="crimson", fontsize=10)

# show same point [3,5] in this basis: 3v1 + 5v2 ... wait let me use 1v1 + 1v2
combo = v1 + v2
ax.annotate("", xy=combo, xytext=(0,0), arrowprops=dict(arrowstyle="->", color="green", lw=2.5))
ax.text(combo[0]+0.1, combo[1], "v₁+v₂=[1,3]", color="green", fontsize=10)

for ax in axes:
    ax.set_xlim(-2, 5)
    ax.set_ylim(-2, 6)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.set_xlabel("x")
    ax.set_ylabel("y")

plt.tight_layout()
plt.savefig("0StandardBasis.png", dpi=150)
plt.show()
print("Saved: 0StandardBasis.png")
