import matplotlib.pyplot as plt
import numpy as np

from physics import M, E, b_lensing, b_critical, b_capture, integrate, check_null_invariant

fig, ax = plt.subplots(subplot_kw={"projection": "polar"}, figsize=(7, 7))

cases = [
    (b_lensing, "C0", f"Lensing  ($b = {b_lensing / M:.1f}M$)"),
    (b_critical, "C1", "Critical ($b \\approx b_c$)"),
    (b_capture, "C2", f"Capture  ($b = {b_capture / M:.1f}M$)"),
]

print("--- Running Figure 2 Trajectories ---")
for b, color, label in cases:
    sol = integrate(b)
    check_null_invariant(sol, b * E, E, M)  # sanity check
    r = sol.y[0]
    phi = sol.y[2]
    ax.plot(phi, r / M, color=color, lw=1.0, label=label)

# event horizon and photon sphere for reference
theta_ring = np.linspace(0, 2 * np.pi, 300)
ax.plot(theta_ring, np.full_like(theta_ring, 2.0), "k-", lw=1.5, label="Horizon $r=2M$")
ax.plot(theta_ring, np.full_like(theta_ring, 3.0), "k--", lw=0.8, label="Photon sphere $r=3M$")

ax.set_rlim(0, 30)
ax.set_title("Photon trajectories in Schwarzschild spacetime", pad=15)
ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=8)
fig.tight_layout()

fig.savefig("polar_trajectories.svg", format="svg", bbox_inches="tight")
print("Saved polar_trajectories.svg")
plt.show()
