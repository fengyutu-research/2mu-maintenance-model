"""Shared figure style: Helvetica-metric font, text >= 8 pt, bold axis titles,
transparent background, editable text in PDFs.

The bundled fonts (fonts/HerosTT-*.ttf) are TeX Gyre Heros, a metric clone of Helvetica,
converted to TrueType so that PDFs embed them as editable text. If they are missing,
system Helvetica, then Arial, then DejaVu Sans is used.
"""
import glob
import os

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(REPO, "figures")
DATADIR = os.path.join(REPO, "data")

INK = "#1f2d3d"        # titles and labels
MUTED = "#6B7480"      # secondary annotations
ORANGE = "#E07B39"     # reported range of rho in Fig. 1B, C
GREY_BG = "#E4E6E9"    # "no persistence" region and band fills
BLUES3 = ["#4E9ACD", "#2171B5", "#08306B"]  # light -> dark; lightest meets 3:1 text contrast


def setup():
    """Register the bundled fonts and apply the shared rcParams. Returns the font family used."""
    for f in glob.glob(os.path.join(REPO, "fonts", "HerosTT-*.ttf")):
        fm.fontManager.addfont(f)
    available = {f.name for f in fm.fontManager.ttflist}
    font = next(f for f in ["HerosTT", "Helvetica", "Arial", "DejaVu Sans"] if f in available)
    matplotlib.rcParams.update({
        "font.family": font, "font.size": 8,
        "mathtext.fontset": "custom", "mathtext.rm": font, "mathtext.it": f"{font}:italic",
        "mathtext.bf": f"{font}:bold", "mathtext.bfit": f"{font}:italic:bold",
        "mathtext.default": "regular",
        "axes.labelsize": 9, "axes.titlesize": 9, "axes.labelweight": "bold",
        "xtick.labelsize": 8, "ytick.labelsize": 8,
        "axes.linewidth": 0.75, "xtick.major.width": 0.75, "ytick.major.width": 0.75,
        "xtick.minor.width": 0.5, "ytick.minor.width": 0.5,
        "xtick.major.size": 3, "ytick.major.size": 3, "xtick.minor.size": 1.8, "ytick.minor.size": 1.8,
        "axes.spines.top": False, "axes.spines.right": False,
        "pdf.fonttype": 42, "ps.fonttype": 42,          # editable text in Illustrator
        "savefig.dpi": 600, "figure.dpi": 150,
        "figure.facecolor": "none", "axes.facecolor": "none",
        "savefig.facecolor": "none", "savefig.edgecolor": "none",
    })
    os.makedirs(FIGDIR, exist_ok=True)
    return font


def save(fig, name):
    """Save a figure as PDF (vector) and PNG (300 dpi preview) in figures/."""
    fig.savefig(os.path.join(FIGDIR, f"{name}.pdf"))
    fig.savefig(os.path.join(FIGDIR, f"{name}.png"), dpi=300)
    plt.close(fig)
