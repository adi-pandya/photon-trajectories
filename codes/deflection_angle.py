import matplotlib.pyplot as plt
import numpy as np

from physics import M, bc, integrate, check_null_invariant

b_vals = np.linspace(bc * 1.01, 20 * M, 60)
delta_phi_numerical = []

print("--- Computing Deflection Angles for Figure 3 ---")
for b in b_vals:
    # start far out so the flat-space initial/final angle assumption holds
    sol = integrate(b, r_start=1000.0 * M, r_out=1000.0 * M)
    check_null_invariant(sol, b, 1.0, M)
    phi_final = sol.y[2][-1]
    delta_phi_numerical.append(phi_final - np.pi)

delta_phi_numerical = np.array(delta_phi_numerical)
delta_phi_analytic = 4.0 * M / b_vals  # weak-field GR result

# residual table for select impact parameters
specific_bs = [20.0, 12.0, 8.0, 6.5, 5.5, 5.25]
r_start_fig3 = 1000.0 * M

print(f"\n{'b/M':<8} | {'Num (deg)':<12} | {'Ana (deg)':<12} | {'Residual (deg)':<15}")
print("-" * 55)
for b in specific_bs:
    sol = integrate(b, r_start=r_start_fig3, r_out=r_start_fig3)
    phi_final = sol.y[2][-1]
    flat_sweep = np.pi - 2.0 * np.arcsin(b / r_start_fig3)  # flat-space baseline
    num_deg = np.degrees(phi_final - flat_sweep)
    ana_deg = np.degrees(4.0 * M / b)
    res_deg = num_deg - ana_deg
    print(f"{b / M:<8.1f} | {num_deg:<12.2f} | {ana_deg:<12.2f} | {res_deg:<15.2f}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(b_vals / M, np.degrees(delta_phi_numerical), "o", ms=3, label="Numerical")
ax.plot(b_vals / M, np.degrees(delta_phi_analytic), "-", label=r"Weak-field: $4M/b$")
ax.set_xlabel(r"$b / M$")
ax.set_ylabel(r"$\Delta\phi$ (degrees)")
ax.set_title("Deflection angle: numerical vs weak-field approximation")
ax.legend()
ax.set_ylim(bottom=0)
fig.tight_layout()

fig.savefig("deflection_angles.svg", format="svg", bbox_inches="tight")
print("\nSaved deflection_angles.svg")
plt.show()
