"""Figure S1: plasmid loss constrains the tolerable cost even when mating re-introduces 2μ.

A  Largest tolerable cost c_crit = (rho - mu)/(1 - mu) vs loss probability mu, for three rho.
   Grey band: haploid loss estimates of Futcher & Cox (1983), 7.6e-5 to 3.1e-4.
B  Long-term carrier fraction vs growth cost at rho = 1e-3, for mu = 1e-6 and 1e-4;
   dashed lines mark c_crit.

Output (figures/): FigS1_tolerable_cost (.pdf, .png).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt

from twomu import critical_cost, equilibrium_fraction
from twomu.style import setup, save, INK, MUTED, GREY_BG, BLUES3

RHO_COL = {1e-5: BLUES3[0], 1e-4: BLUES3[1], 1e-3: BLUES3[2]}
RHO_LAB = {1e-5: "10^{-5}", 1e-4: "10^{-4}", 1e-3: "10^{-3}"}
HAPLOID_MU = (7.6e-5, 3.1e-4)


def main():
    setup()
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(6.2, 2.2), gridspec_kw={"width_ratios": [1.15, 1]})

    # A: c_crit vs mu
    axA.axvspan(*HAPLOID_MU, color=GREY_BG, lw=0, zorder=0)
    axA.text(np.sqrt(HAPLOID_MU[0] * HAPLOID_MU[1]), 2.2e-2, "haploid\nestimate", ha="center",
             va="top", color=MUTED, fontsize=8, linespacing=1.0)
    for rho in [1e-5, 1e-4, 1e-3]:
        mu = np.logspace(-7, np.log10(rho), 2000)[:-1]
        cc = critical_cost(rho, mu)
        axA.plot(mu, cc, color=RHO_COL[rho], lw=1.4)
        axA.plot([mu[-1], mu[-1]], [cc[-1], 1e-9], color=RHO_COL[rho], lw=1.4)   # drop to zero at mu = rho
        axA.text(1.3e-7, rho * 1.35, f"$\\mathit{{\\rho}} = {RHO_LAB[rho]}$", color=RHO_COL[rho],
                 fontsize=8, va="bottom")
    axA.set_xscale("log"); axA.set_yscale("log")
    axA.set_xlim(1e-7, 1e-2); axA.set_ylim(1e-8, 3e-2)
    axA.set_xticks([1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2])
    axA.set_yticks([1e-8, 1e-6, 1e-4, 1e-2])
    axA.set_xlabel("Loss probability per division, $\\mathbfit{\\mu}$")
    axA.set_ylabel("Largest tolerable cost, $\\mathbfit{c}_{\\mathbf{crit}}$")

    # B: carrier fraction vs cost at rho = 1e-3
    rho = 1e-3
    c = np.linspace(0, 1.0e-3, 4001)
    for mu, col, lab, xpos, ypos in [(1e-6, BLUES3[2], "$\\mathit{\\mu} = 10^{-6}$", 0.040, 0.935),
                                     (1e-4, BLUES3[0], "$\\mathit{\\mu} = 10^{-4}$", 0.030, 0.72)]:
        x = np.nan_to_num(equilibrium_fraction(c, mu, rho), nan=0.0)
        axB.plot(100 * c, 100 * x, color=col, lw=1.4)
        axB.axvline(100 * critical_cost(rho, mu), color=col, lw=0.8, ls=(0, (3, 2)))
        axB.text(xpos, 100 * ypos, lab, color=col, fontsize=8, va="center")
    axB.set_xlim(0, 0.1); axB.set_ylim(0, 103)
    axB.set_xticks([0, 0.02, 0.04, 0.06, 0.08, 0.1])
    axB.set_xlabel("Growth cost, $\\mathbfit{c}$ (%)")
    axB.set_ylabel("Long-term carriers (%)")
    axB.set_title("$\\mathit{\\rho} = 10^{-3}$", color=INK, pad=4)

    for ax, lab in [(axA, "A"), (axB, "B")]:
        ax.text(-0.24, 1.04, lab, transform=ax.transAxes, fontsize=10, fontweight="bold", va="bottom")
    fig.tight_layout(pad=0.4, w_pad=2.6)
    save(fig, "FigS1_tolerable_cost")


if __name__ == "__main__":
    main()
