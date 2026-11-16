"""Regenerate all figures (main-text Figure 1, Supplementary Figs S1 and S2) into figures/.

Usage:  python make_figures.py
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "scripts"))

import fig1
import figS1
import figS2

if __name__ == "__main__":
    for name, mod in [("Figure 1", fig1), ("Figure S1", figS1), ("Figure S2", figS2)]:
        t0 = time.time()
        mod.main()
        print(f"{name}: done ({time.time() - t0:.0f} s)")
    print(f"Figures written to {os.path.join(HERE, 'figures')}")
