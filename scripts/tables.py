"""Print the numbers quoted in the Supplementary Note.

Fig. 1A   generations to 50% carriers without mating (mu = 1e-4)
Table S3  largest tolerable cost at reported re-introduction rates
S3 text   carrier fraction near the cost limit at rho = 1e-3
Table S4  serial-transfer simulations of the YPD 30 C protocol (same runs as Fig. S2B)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np

from twomu import generations_to_fraction, critical_cost, equilibrium_fraction, deterministic

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figS2


def pct(v):
    """Format a cost as in Table S3: 'none' if no cost is tolerable."""
    if v < 0:
        return "none"
    if v == 0:
        return "0"
    return f"{100 * v:.3f}%" if v >= 1e-4 else f"{100 * v:.4f}%"


def main():
    print("Fig. 1A: generations to 50% carriers, no mating, mu = 1e-4")
    for c in [0, 0.001, 0.01, 0.02, 0.03]:
        print(f"  c = {100 * c:g}%: {generations_to_fraction(c, 1e-4):,.0f}")

    print("\nTable S3: largest tolerable cost c_crit = (rho - mu)/(1 - mu)")
    print(f"  {'rho':>8}  {'mu=1e-4':>9}  {'mu=1e-6':>9}  carriers at c=0, mu=1e-4")
    for rho in [1e-3, 3e-4, 1e-4, 2e-5]:
        x0 = np.nan_to_num(equilibrium_fraction(0.0, 1e-4, rho), nan=0.0)
        print(f"  {rho:>8.0e}  {pct(critical_cost(rho, 1e-4)):>9}  {pct(critical_cost(rho, 1e-6)):>9}  {100 * x0:.0f}%")

    print("\nS3 text: long-term carrier fraction at rho = 1e-3")
    for mu in [1e-4, 1e-6]:
        row = [f"c={100 * c:g}%: {100 * np.nan_to_num(equilibrium_fraction(c, mu, 1e-3), nan=0.0):.1f}%"
               for c in [0, 5e-4, 8e-4, 8.8e-4, 9e-4, 9.5e-4]]
        print(f"  mu={mu:g}: " + ", ".join(row))

    print("\nTable S4: serial transfer, YPD 30 C protocol "
          f"({figS2.DOUBLINGS} doublings/transfer, {figS2.BOTTLENECK:,} cells, {figS2.N_REP:,} populations)")
    n_cycles = figS2.TIMEPOINTS[-1] // figS2.DOUBLINGS
    idx = [t // figS2.DOUBLINGS for t in figS2.TIMEPOINTS]
    for res, (c, mu, lab) in zip(figS2.simulate(), figS2.SCENARIOS):
        det = deterministic(c, mu, n_cycles, figS2.DOUBLINGS)[idx]
        print(f"  {lab} (mu={mu:g})")
        print("    generation        " + "".join(f"{t:>8,}" for t in figS2.TIMEPOINTS))
        print("    mean x            " + "".join(f"{v:>8.3f}" for v in res.mean(1)))
        print("    deterministic x   " + "".join(f"{v:>8.3f}" for v in det))
        print("    frac with x > 0.5 " + "".join(f"{v:>8.3f}" for v in (res > 0.5).mean(1)))
        print("    frac no carriers  " + "".join(f"{v:>8.4f}" for v in (res == 0).mean(1)))


if __name__ == "__main__":
    main()
