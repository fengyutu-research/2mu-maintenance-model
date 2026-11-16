"""Two-state population model of 2μ plasmid maintenance.

Cells either carry 2μ (carriers, fraction x) or not ([cir0], fraction 1 - x).

Parameters
----------
c   : growth cost, the relative reduction in the carrier division rate (0 <= c < 1)
mu  : probability that a carrier division produces one plasmid-free daughter
rho : re-introduction rate by mating, relative to the division rate (rho = m / b)

Time G is measured in doublings of the whole population. The carrier fraction follows

    dx/dG = ln2 * x * [(rho - c)(1 - x) - (1 - c) mu] / (1 - c x)

All functions use NumPy only and broadcast over array inputs.
"""
import numpy as np

LN2 = np.log(2.0)


def dx_dG(x, c, mu, rho=0.0):
    """Rate of change of the carrier fraction per population doubling."""
    return LN2 * x * ((rho - c) * (1 - x) - (1 - c) * mu) / (1 - c * x)


def generations_to_fraction(c, mu, x0=1.0, q=0.5):
    """Generations for the carrier fraction to fall from x0 to q without mating (rho = 0).

    Closed-form integral of dx/dG with a = c + (1 - c) mu:
        G = [ln(x0/q) - (1 - a) ln((a - c x0)/(a - c q))] / (a ln2)
    """
    c = np.asarray(c, dtype=float)
    a = c + (1 - c) * mu
    return (np.log(x0 / q) - (1 - a) * np.log((a - c * x0) / (a - c * q))) / (a * LN2)


def persists(c, mu, rho):
    """True where 2μ persists in the long run: rho > c + (1 - c) mu."""
    return rho > c + (1 - c) * mu


def equilibrium_fraction(c, mu, rho):
    """Long-term carrier fraction x* = 1 - (1 - c) mu / (rho - c); NaN where 2μ cannot persist."""
    with np.errstate(divide="ignore", invalid="ignore"):
        x = 1 - (1 - c) * mu / (rho - c)
    return np.where(persists(c, mu, rho), np.clip(x, 0, 1), np.nan)


def rho_for_fraction(c, mu, q):
    """Re-introduction rate giving long-term carrier fraction q (q = 0 gives the persistence threshold)."""
    return c + (1 - c) * mu / (1 - q)


def critical_cost(rho, mu):
    """Largest tolerable cost c_crit = (rho - mu) / (1 - mu); negative means no cost is tolerable."""
    return (rho - mu) / (1 - mu)
