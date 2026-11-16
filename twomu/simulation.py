"""Serial-transfer simulation of the two-state model without mating (rho = 0).

Each cycle: the population grows deterministically by `doublings` population doublings
(the expected dynamics dx/dG, integrated with a 4th-order Runge-Kutta scheme), then
`bottleneck` cells are transferred at random, so the number of carriers transferred is
Binomial(bottleneck, x). Randomness enters only through the transfer.
"""
import numpy as np

from .model import dx_dG


def grow(x, c, mu, doublings=10, steps=40):
    """Advance the carrier fraction x by `doublings` population doublings (RK4)."""
    h = doublings / steps
    for _ in range(steps):
        k1 = dx_dG(x, c, mu)
        k2 = dx_dG(x + 0.5 * h * k1, c, mu)
        k3 = dx_dG(x + 0.5 * h * k2, c, mu)
        k4 = dx_dG(x + h * k3, c, mu)
        x = x + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return np.clip(x, 0.0, 1.0)


def serial_transfer(c, mu, bottleneck, n_cycles, n_rep, rng, doublings=10):
    """Carrier fraction after each transfer.

    Returns an array of shape (n_cycles + 1, n_rep); row k is the state after k transfers
    (row 0 is the start, all cells carriers).
    """
    x = np.ones(n_rep)
    out = [x.copy()]
    for _ in range(n_cycles):
        x = rng.binomial(bottleneck, grow(x, c, mu, doublings)) / bottleneck
        out.append(x.copy())
    return np.array(out)


def deterministic(c, mu, n_cycles, doublings=10):
    """Same growth without bottleneck sampling; returns shape (n_cycles + 1,)."""
    x = np.ones(1)
    out = [1.0]
    for _ in range(n_cycles):
        x = grow(x, c, mu, doublings)
        out.append(float(x[0]))
    return np.array(out)
