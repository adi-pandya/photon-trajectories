import matplotlib.pyplot as plt
import numpy as np

from physics import M, E, bc, V_eff

fig, ax = plt.subplots(figsize=(8, 5))

r_plot = np.linspace(2.1 * M, 20 * M, 1000)
for L_val, label in [
    (5 * M, r"$L = 5M$"),
    (bc * M, r"$L = b_c$"),
    (8 * M, r"$L = 8M$"),
]:
    ax.plot(r_plot / M, V_eff(r_plot, L_val) / E**2, label=label)

# newtonian potential for comparison: L^2/r^2 only, no (1-2M/r) factor
L_ref = 6.0 * M
ax.plot(
    r_plot / M,
    L_ref**2 / r_plot**2 / E**2,
    "k--",
    alpha=0.5,
    label=r"Newtonian ($L=6M$)",
)

ax.axvline(3.0, color="gray", lw=0.8, ls=":")
ax.text(3.1, 0.02, r"$r = 3M$", fontsize=9, color="gray")
ax.set_xlabel(r"$r / M$")
ax.set_ylabel(r"$V_\mathrm{eff} / E^2$")
ax.set_title("Effective potential for null geodesics")
ax.legend()
ax.set_xlim(2.0, 20.0)
fig.tight_layout()

fig.savefig("effective_potential.svg", format="svg", bbox_inches="tight")
print("Saved effective_potential.svg")
plt.show()
