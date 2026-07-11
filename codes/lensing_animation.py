"""
NOTE:

Set SAVE_GIF = True to render the full animation (slow). Default saves a single
representative still frame as SVG, matching what's needed for the report/README.
"""

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

from physics import M, b_lensing, b_critical, b_capture, integrate

SAVE_GIF = False  # flip to True to render lensing_animation.gif (takes a while)

# Three scenarios, offset by 120 degrees so they approach from different sides.
anim_cases = [
    {"b": b_capture, "color": "tomato", "phi_offset": 0.0, "label": "Capture"},
    {"b": b_critical, "color": "gold", "phi_offset": 2 * np.pi / 3, "label": "Critical"},
    {"b": b_lensing, "color": "cyan", "phi_offset": 4 * np.pi / 3, "label": "Lensing"},
]

t_max_anim = 120.0 * M
frames_count = 600
t_uniform = np.linspace(0, t_max_anim, frames_count)

anim_data = []

print("--- Preparing Animation Data ---")
for case in anim_cases:
    sol = integrate(case["b"])
    r_raw = sol.y[0]
    phi_raw = sol.y[2] + case["phi_offset"]
    t_raw = sol.y[3]

    if np.min(r_raw) < 2.1 * M:
        cutoff = int(len(t_raw) * 0.98)
        r_raw, phi_raw, t_raw = r_raw[:cutoff], phi_raw[:cutoff], t_raw[:cutoff]

    r_anim = interp1d(t_raw, r_raw, kind="linear", bounds_error=False,
                       fill_value=(r_raw[0], r_raw[-1]))(t_uniform)
    phi_anim = interp1d(t_raw, phi_raw, kind="linear", bounds_error=False,
                         fill_value=(phi_raw[0], phi_raw[-1]))(t_uniform)

    x_anim = (r_anim / M) * np.cos(phi_anim)
    y_anim = (r_anim / M) * np.sin(phi_anim)

    anim_data.append({"x": x_anim, "y": y_anim, "color": case["color"], "label": case["label"]})

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect("equal")
ax.set_xlim(-35, 35)
ax.set_ylim(-35, 35)
ax.set_facecolor("white")

horizon = plt.Circle((0, 0), 2.0, color="white", zorder=5)
horizon_ring = plt.Circle((0, 0), 2.0, color="black", fill=False, lw=1.2, zorder=6)
photon_sph = plt.Circle((0, 0), 3.0, color="gray", fill=False, lw=0.8, ls="--", zorder=6)
ax.add_patch(horizon)
ax.add_patch(horizon_ring)
ax.add_patch(photon_sph)
ax.text(0, 2.3, r"$r=2M$", color="black", ha="center", fontsize=8, zorder=7)
ax.text(0, 3.3, r"$r=3M$", color="gray", ha="center", fontsize=8, zorder=7)

trails, photons = [], []
for data in anim_data:
    (trail,) = ax.plot([], [], color=data["color"], lw=1.0, alpha=0.6)
    (photon,) = ax.plot([], [], marker="o", color=data["color"], ms=5, zorder=10, label=data["label"])
    trails.append(trail)
    photons.append(photon)

time_text = ax.text(0.05, 0.95, "", transform=ax.transAxes, color="black", fontsize=10, va="top")
ax.legend(loc="upper right", facecolor="white", edgecolor="black", labelcolor="black")
ax.set_title("Multi-Photon Trajectories in Coordinate Time", color="black", pad=15)

trail_length = 80  # frames kept in the comet tail


def init():
    for trail in trails:
        trail.set_data([], [])
    for photon in photons:
        photon.set_data([], [])
    time_text.set_text("")
    return (*trails, *photons, time_text)


def update(frame):
    start = max(0, frame - trail_length)
    for i, data in enumerate(anim_data):
        trails[i].set_data(data["x"][start:frame], data["y"][start:frame])
        photons[i].set_data([data["x"][frame]], [data["y"][frame]])
    time_text.set_text(f"t = {t_uniform[frame]:.1f} M")
    return (*trails, *photons, time_text)


ani = animation.FuncAnimation(fig, update, frames=len(t_uniform), init_func=init, interval=15, blit=True)

if SAVE_GIF:
    print("Saving animation to GIF... (this might take a minute)")
    ani.save("lensing_animation.gif", writer="pillow", fps=60)
    print("Saved lensing_animation.gif")
else:
    update(200)  # representative frame near closest approach
    fig.savefig("animation_frame.svg", format="svg", bbox_inches="tight")
    print("Saved animation_frame.svg")

plt.show()
