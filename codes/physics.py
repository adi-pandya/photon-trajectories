"""
Core physics for photon geodesics in Schwarzschild spacetime.
State vector: y = [r, r_dot, phi, t]  (affine parameter lambda as independent variable)
Units: geometrised, G = c = 1. Black hole mass M sets the scale.

Imported by all scripts — nothing in this file produces output on its own.
"""

import numpy as np
from scipy.integrate import solve_ivp

# Parameters

M = 0.5  # BH mass (everything else is in units of M)
E = 1.0  # photon energy
r0 = 30.0 * M  # initial radius
bc = 3.0 * np.sqrt(3.0) * M  # critical impact parameter ~ 5.196 M

# Three representative impact parameters
b_lensing = 8.0 * M  # b > bc: deflected, escapes
b_critical = bc * 1.001  # b just above bc: winds around photon sphere many times
b_capture = 4.0 * M  # b < bc: falls in

# Integration range in affine parameter
lam_span = (0.0, 2000.0)
lam_eval = np.linspace(*lam_span, 200_000)


# Core physics

def V_eff(r, L):
    # Effective potential for null geodesics: L^2/r^2 * (1 - 2M/r)
    return (L**2 / r**2) * (1.0 - 2.0 * M / r)


def geodesic_rhs(lam, y, L):
    r, r_dot, phi, t = y

    r_ddot = L**2 / r**3 - 3.0 * M * L**2 / r**4

    phi_dot = L / r**2  # from conservation of L = r^2 * phi_dot
    t_dot = E / (1.0 - 2.0 * M / r)  # from conservation of E; diverges at horizon

    return [r_dot, r_ddot, phi_dot, t_dot]


def make_events(r_inner=2.05 * M, r_outer=500.0 * M):

    def hit_horizon(lam, y, L):
        return y[0] - r_inner

    hit_horizon.terminal = True
    hit_horizon.direction = -1

    def escaped(lam, y, L):
        return y[0] - r_outer

    escaped.terminal = True
    escaped.direction = +1

    return [hit_horizon, escaped]


def integrate(b, r_start=r0, r_out=500.0 * M):
    L = b * E

    # initial r_dot from null condition
    # negative sign: photon starts far out and moves inward
    r_dot0 = -np.sqrt(max(E**2 - V_eff(r_start, L), 0.0))

    y0 = [r_start, r_dot0, 0.0, 0.0]  # [r, r_dot, phi, t]

    sol = solve_ivp(
        geodesic_rhs,
        lam_span,
        y0,
        args=(L,),
        method="RK45",
        t_eval=lam_eval,
        events=make_events(r_outer=r_out),
        rtol=1e-10,
        atol=1e-12,  # tight tolerances non-negotiable near b ~ bc
        dense_output=False,
    )
    return sol


def check_null_invariant(sol, L, E, M_val=1.0):
    r, r_dot, phi, t = sol.y
    phi_dot = L / r**2
    t_dot = E / (1.0 - 2.0 * M_val / r)

    term_t = -(1.0 - 2.0 * M_val / r) * t_dot**2
    term_r = (1.0 / (1.0 - 2.0 * M_val / r)) * r_dot**2
    term_phi = (r**2) * phi_dot**2

    ds2 = term_t + term_r + term_phi
    max_drift = np.max(np.abs(ds2))
    print(f"Max null invariant drift for b={L / E:.3f}M: {max_drift:.2e}")
    return max_drift
