"""Numerical checks of the closed-form results and the simulation.

1. The carrier-fraction equation dx/dG matches direct integration of the cell-number
   equations dX/dt, dY/dt (with mating), with G = log2(N/N0).
2. The closed-form generations-to-50% agrees with direct integration of dx/dG.
3. The equilibrium x* is reached by long integration, and x -> 0 below the threshold.
4. The RK4 growth step matches the exact no-cost solution x = 2^(-mu G).
5. With no cost, the simulated mean after transfer matches the exact mean (no bias from sampling).
Run: python scripts/checks.py   (prints PASS/FAIL for each check)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np

from twomu import (dx_dG, generations_to_fraction, equilibrium_fraction, grow, serial_transfer)


def rk4(f, y, t_end, n):
    h = t_end / n
    for _ in range(n):
        k1 = f(y); k2 = f(y + 0.5 * h * k1); k3 = f(y + 0.5 * h * k2); k4 = f(y + h * k3)
        y = y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return y


def report(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")
    return ok


def main():
    ok = True
    b = 1.0
    # 1. cell numbers vs carrier fraction, on the population-doubling clock
    for c, mu, rho in [(0.01, 1e-3, 0.05), (0.002, 1e-4, 0.0), (0.0, 1e-2, 0.03)]:
        m = rho * b
        def cells(y):
            X, Y = y; N = X + Y
            return np.array([b * (1 - c) * (1 - mu) * X + m * X * Y / N,
                             b * Y + b * (1 - c) * mu * X - m * X * Y / N])
        X, Y = rk4(cells, np.array([0.7, 0.3]), 50.0, 50000)
        G = np.log2((X + Y) / 1.0)
        x_from_cells = X / (X + Y)
        x_from_G = rk4(lambda x: dx_dG(x, c, mu, rho), np.array(0.7), G, 50000)
        ok &= report("cell-number equations = dx/dG", abs(x_from_cells - x_from_G) < 1e-8,
                     f"(c={c}, mu={mu}, rho={rho}: {x_from_cells:.10f} vs {float(x_from_G):.10f})")
    # 2. closed-form time to 50%
    for c in [0, 0.001, 0.01, 0.03]:
        G50 = generations_to_fraction(c, 1e-4)
        x = rk4(lambda x: dx_dG(x, c, 1e-4), np.array(1.0), G50, 200000)
        ok &= report("closed-form generations to 50%", abs(float(x) - 0.5) < 1e-7,
                     f"(c={c}: G50={G50:,.1f}, x(G50)={float(x):.9f})")
    # 3. equilibrium
    for c, mu, rho in [(1e-3, 1e-4, 1e-2), (5e-4, 1e-4, 1e-3), (1e-3, 1e-4, 5e-4)]:
        x_inf = float(rk4(lambda x: dx_dG(x, c, mu, rho), np.array(1.0), 3e5, 300000))
        x_star = float(np.nan_to_num(equilibrium_fraction(c, mu, rho), nan=0.0))
        ok &= report("long-run x = x*", abs(x_inf - x_star) < 1e-4,
                     f"(c={c}, mu={mu}, rho={rho}: {x_inf:.5f} vs {x_star:.5f})")
    # 4. RK4 growth step vs exact no-cost solution
    x = np.ones(1)
    for _ in range(1019):
        x = grow(x, 0.0, 1e-4)
    exact = 2 ** (-1e-4 * 10190)
    ok &= report("RK4 growth vs exact 2^(-mu G)", abs(x[0] - exact) < 1e-10, f"({x[0]:.12f} vs {exact:.12f})")
    # 5. unbiased transfer: mean after many populations equals the deterministic value
    rng = np.random.default_rng(1)
    res = serial_transfer(0.0, 1e-4, 8000, 100, 20000, rng)
    exact = 2 ** (-1e-4 * 1000)
    se = res[-1].std() / np.sqrt(res.shape[1])
    ok &= report("simulated mean = exact mean (no cost)", abs(res[-1].mean() - exact) < 4 * se,
                 f"({res[-1].mean():.6f} vs {exact:.6f}, 4 SE = {4 * se:.6f})")
    print("\nAll checks passed." if ok else "\nSome checks FAILED.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
