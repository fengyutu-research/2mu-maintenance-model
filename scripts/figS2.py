"""Figure S2: experimental vs simulated loss of 2μ.

A  2μ copy number in evolving populations, reproduced from Fig. 9B of Johnson et al. (2021),
   eLife 10:e63910, https://doi.org/10.7554/eLife.63910, (c) 2021 Johnson et al., CC BY 4.0
   (data/johnson2021_fig9B.png; panel B of their Fig. 9, cropped).
B  Serial-transfer simulation of their YPD 30 C protocol: 10 doublings per daily transfer
   (1:2^10 dilution), 8,000 cells transferred, no mating. 12 of 2,000 simulated populations
   per scenario, at the generations sampled by Johnson et al.

Output (figures/): FigS2_comparison (.pdf, .png). Table S4 values: scripts/tables.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt

from twomu import serial_transfer
from twomu.style import setup, save, INK, DATADIR

# Protocol of Johnson et al. (2021), YPD 30 C
DOUBLINGS = 10
BOTTLENECK = 8000
TIMEPOINTS = [70, 1410, 2640, 5170, 7550, 10190]
N_REP = 2000
N_SHOW = 12
SEED = 20261009
SCENARIOS = [  # (cost c, loss probability mu, label)
    (0.0, 1e-4, "No cost"),
    (0.001, 1e-4, "0.1% cost"),
    (0.01, 1e-4, "1% cost"),
    (0.001, 1e-6, "0.1% cost, lower loss"),
]
MU_LAB = {1e-4: "$\\mathit{\\mu} = 10^{-4}$", 1e-6: "$\\mathit{\\mu} = 10^{-6}$"}


def simulate():
    """Carrier fraction at TIMEPOINTS for each scenario: list of arrays (len(TIMEPOINTS), N_REP)."""
    n_cycles = TIMEPOINTS[-1] // DOUBLINGS
    idx = [t // DOUBLINGS for t in TIMEPOINTS]
    rng = np.random.default_rng(SEED)
    return [serial_transfer(c, mu, BOTTLENECK, n_cycles, N_REP, rng, DOUBLINGS)[idx]
            for c, mu, _ in SCENARIOS]


def main():
    setup()
    results = simulate()

    W, H = 6.5, 6.9
    fig = plt.figure(figsize=(W, H))
    # A: experiment
    img = plt.imread(os.path.join(DATADIR, "johnson2021_fig9B.png"))
    ih, iw = img.shape[:2]
    a_w = 3.7 / W
    a_h = (3.7 * ih / iw) / H
    axA = fig.add_axes([0.5 - a_w / 2 + 0.03, 1 - a_h - 0.015, a_w, a_h])
    axA.imshow(img)
    axA.axis("off")
    fig.text(0.02, 0.985, "A", fontsize=10, fontweight="bold", va="top")
    fig.text(0.02, 0.43, "B", fontsize=10, fontweight="bold", va="top")

    # B: simulation
    left, w, gap, bottom, h = 0.095, 0.178, 0.024, 0.105, 0.255
    axes = [fig.add_axes([left + i * (w + gap), bottom, w, h]) for i in range(4)]
    cax = fig.add_axes([left + 4 * (w + gap) - gap + 0.012, bottom, 0.012, h])
    for ax, res, (c, mu, lab) in zip(axes, results, SCENARIOS):
        im = ax.imshow(res[:, :N_SHOW].T, cmap="Blues", vmin=0, vmax=1, aspect="auto",
                       interpolation="nearest")
        ax.set_xticks(range(len(TIMEPOINTS)))
        ax.set_xticklabels([f"{t:,}" for t in TIMEPOINTS], rotation=90)
        ax.set_yticks([])
        ax.set_xticks(np.arange(-0.5, len(TIMEPOINTS)), minor=True)
        ax.set_yticks(np.arange(-0.5, N_SHOW), minor=True)
        ax.grid(which="minor", color="white", linewidth=0.8)
        ax.tick_params(which="minor", length=0)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.set_title(f"{lab}\n{MU_LAB[mu]}", color=INK, pad=4, linespacing=1.3)
        ax.set_xlabel("Generation")
    axes[0].set_ylabel(f"{N_SHOW} simulated populations")
    cb = fig.colorbar(im, cax=cax)
    cb.set_label("Carrier fraction")
    cb.set_ticks([0, 0.5, 1])
    cb.outline.set_linewidth(0.75)
    save(fig, "FigS2_comparison")


if __name__ == "__main__":
    main()
