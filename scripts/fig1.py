"""Figure 1 (main text), modelling panels.

A  Generations for carriers to fall from 100% to 50% without mating (mu = 1e-4).
B  Long-term carrier fraction vs growth cost c and re-introduction rate rho, mu = 1e-6.
C  As B, mu = 1e-4.

Outputs (figures/): Fig1_A_generations_to_50pct, Fig1_BC_carrier_heatmaps, Fig1_combined (.pdf, .png).
Panel letters appear only in the combined preview; re-letter as needed for the final layout.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from twomu import generations_to_fraction, equilibrium_fraction, rho_for_fraction
from twomu.style import setup, save, INK, ORANGE, GREY_BG, MUTED

COSTS_A = np.array([0, 0.001, 0.01, 0.02, 0.03])   # costs marked in panel A
RHO_RANGE = (1e-5, 1e-3)                           # reported range of rho (Ruderfer 2006; Lee 2022)
CMAP = ListedColormap(plt.get_cmap("Blues")(np.linspace(0, 1, 256)))


def panel_A(ax, mu=1e-4):
    cc = np.linspace(0, 0.0305, 300)
    ax.plot(100 * cc, generations_to_fraction(cc, mu), color=INK, lw=1, zorder=1)
    g = generations_to_fraction(COSTS_A, mu)
    ax.scatter(100 * COSTS_A, g, s=18, color=INK, zorder=2, clip_on=False)
    for c, v in zip(100 * COSTS_A, g):
        ax.annotate(f"{v:,.0f}", (c, v), xytext=(5, 2), textcoords="offset points",
                    fontsize=8, color=INK, ha="left", va="bottom")
    ax.set_yscale("log")
    ax.set_ylim(150, 3e4)
    ax.set_xlim(-0.15, 3.4)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xlabel("Growth cost, $\\mathbfit{c}$ (%)")
    ax.set_ylabel("Generations to 50% carriers")
    ax.set_title("No mating, $\\mathit{\\mu} = 10^{-4}$", pad=6)


def heatmap(ax, mu, title, show_ylabel, label_bar, n=500):
    c = np.logspace(-6, -2, n)
    C, R = np.meshgrid(c, c)
    ax.set_facecolor(GREY_BG)                       # grey = 2μ cannot persist
    m = ax.pcolormesh(C, R, equilibrium_fraction(C, mu, R), cmap=CMAP, vmin=0, vmax=1,
                      shading="auto", rasterized=True)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(1e-6, 1e-2); ax.set_ylim(1e-6, 1e-2)
    cl = np.logspace(-6, -2, 400)
    ax.plot(cl, rho_for_fraction(cl, mu, 0.0), color=INK, lw=1.0)                        # threshold
    ax.plot(cl, rho_for_fraction(cl, mu, 0.5), color="white", lw=0.9, ls=(0, (1, 1.3)))  # 50 %
    ax.plot(cl, rho_for_fraction(cl, mu, 0.9), color="white", lw=0.9, ls=(0, (4, 2)))    # 90 %
    ax.fill_between([1e-6, 1.35e-6], *RHO_RANGE, color=ORANGE, lw=0, zorder=3)
    if label_bar:
        ax.text(1.7e-6, 1.6e-4, "reported\n$\\mathit{\\rho}$ range", color=ORANGE,
                fontsize=8, va="center", ha="left", linespacing=1.0)
    ax.text(1.4e-3, 2.4e-6, "no\npersistence", color=MUTED, fontsize=8,
            ha="center", va="center", linespacing=1.0)
    for s in ax.spines.values():
        s.set_visible(True)
    ticks = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2]
    ax.set_xticks(ticks); ax.set_yticks(ticks)
    ax.set_xlabel("Growth cost, $\\mathbfit{c}$")
    if show_ylabel:
        ax.set_ylabel("Transmission by mating, $\\mathbfit{\\rho}$")
    else:
        ax.set_yticklabels([])
    ax.set_title(title, pad=6)
    ax.set_aspect("equal")
    return m


def heatmap_pair(fig, axB, axC, cax):
    heatmap(axB, 1e-6, "$\\mathit{\\mu} = 10^{-6}$ (lower loss)", True, True)
    m = heatmap(axC, 1e-4, "$\\mathit{\\mu} = 10^{-4}$ (haploid estimate)", False, False)
    cb = fig.colorbar(m, cax=cax)
    cb.set_label("Long-term carrier fraction")
    cb.outline.set_linewidth(0.75)
    cb.set_ticks([0, 0.25, 0.5, 0.75, 1])


def main():
    setup()
    # Panel A alone
    fig, ax = plt.subplots(figsize=(2.4, 2.25))
    panel_A(ax)
    fig.tight_layout(pad=0.3)
    save(fig, "Fig1_A_generations_to_50pct")
    # Panels B, C
    fig = plt.figure(figsize=(5.2, 2.35))
    axB = fig.add_axes([0.12, 0.19, 0.34, 0.69])
    axC = fig.add_axes([0.48, 0.19, 0.34, 0.69])
    cax = fig.add_axes([0.845, 0.19, 0.017, 0.69])
    heatmap_pair(fig, axB, axC, cax)
    save(fig, "Fig1_BC_carrier_heatmaps")
    # Combined preview A-C
    fig = plt.figure(figsize=(7.3, 2.35))
    axA = fig.add_axes([0.075, 0.19, 0.22, 0.69])
    axB = fig.add_axes([0.40, 0.19, 0.24, 0.69])
    axC = fig.add_axes([0.66, 0.19, 0.24, 0.69])
    cax = fig.add_axes([0.915, 0.19, 0.012, 0.69])
    panel_A(axA)
    heatmap_pair(fig, axB, axC, cax)
    for ax, lab, dx in [(axA, "A", -0.3), (axB, "B", -0.33), (axC, "C", -0.08)]:
        ax.text(dx, 1.12, lab, transform=ax.transAxes, fontsize=10, fontweight="bold", va="top")
    save(fig, "Fig1_combined")


if __name__ == "__main__":
    main()
