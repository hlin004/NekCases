#!/usr/bin/env python3
"""Regenerate the mid-plane temperature profile figures for case Ra1e3.

Compares the Nek5000 centreline data extracted with ParaView against the
profiles digitized from Fig. 4 of Patel et al., Comput. Fluids 95 (2014) 197.

Run from anywhere; paths are resolved relative to this file.
"""
import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, os.pardir, "Ra1e3", "postproc")
OUT = os.path.join(HERE, "figures")

BLUE = "#2a78d6"    # Nek5000
ORANGE = "#eb6834"  # reference
INK = "#333333"
MUTED = "#8a8a85"

plt.rcParams.update({
    "font.size": 10,
    "font.family": "serif",
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "axes.linewidth": 0.8,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.labelcolor": INK, "ytick.labelcolor": INK,
    "grid.color": "#e6e6e2", "grid.linewidth": 0.6,
    "legend.frameon": False,
    "figure.facecolor": "white", "axes.facecolor": "white",
})


def read_xy(path):
    """Two-column digitized data, no header."""
    xs, ys = [], []
    with open(path) as f:
        for row in csv.reader(f):
            if len(row) >= 2:
                try:
                    xs.append(float(row[0]))
                    ys.append(float(row[1]))
                except ValueError:
                    pass
    return xs, ys


def read_paraview(path, xcol, ycol):
    """ParaView Plot-Over-Line export, named columns."""
    xs, ys = [], []
    with open(path) as f:
        for row in csv.DictReader(f):
            xs.append(float(row[xcol]))
            ys.append(float(row[ycol]))
    return xs, ys


os.makedirs(OUT, exist_ok=True)

# Vertical mid-plane x = 0.5: T vs y
ref_T, ref_y = read_xy(os.path.join(DATA, "fig4a.csv"))
y_nek, T_nek = read_paraview(os.path.join(DATA, "x=0.5.csv"),
                             "Points_1", "temperature")

fig, ax = plt.subplots(figsize=(4.6, 3.6))
ax.plot(T_nek, y_nek, color=BLUE, lw=1.6, label="Nek5000", zorder=3)
ax.plot(ref_T, ref_y, "o", mfc="none", mec=ORANGE, mew=1.2, ms=5,
        linestyle="none", label="SEDG-LBM, ref. [1]", zorder=2)
ax.set_xlabel("Temperature $T$")
ax.set_ylabel("$y$")
ax.set_ylim(-0.02, 1.02)
ax.grid(True, zorder=0)
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "ra3_profile_x05.pdf"))

# Horizontal mid-plane y = 0.5: T vs x
ref_x, ref_T2 = read_xy(os.path.join(DATA, "fig4b.csv"))
x_nek, T_nek2 = read_paraview(os.path.join(DATA, "y=0.5.csv"),
                              "Points_0", "temperature")

fig, ax = plt.subplots(figsize=(4.6, 3.6))
ax.plot(x_nek, T_nek2, color=BLUE, lw=1.6, label="Nek5000", zorder=3)
ax.plot(ref_x, ref_T2, "o", mfc="none", mec=ORANGE, mew=1.2, ms=5,
        linestyle="none", label="SEDG-LBM, ref. [1]", zorder=2)
ax.set_xlabel("$x$")
ax.set_ylabel("Temperature $T$")
ax.set_xlim(-0.02, 1.02)
ax.grid(True, zorder=0)
ax.legend(loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "ra3_profile_y05.pdf"))

print("wrote figures to", OUT)
