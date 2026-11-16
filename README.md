# 2μ maintenance model

Code for the population model of 2μ plasmid maintenance in *Saccharomyces cerevisiae* used in [paper reference to be added later]. It reproduces the modelling panels of Figure 1, Supplementary Figures S1 and S2, and the numbers in Supplementary Tables S3 and S4.

## Model

Cells either carry 2μ (fraction *x*) or are plasmid-free. Carriers divide at a rate reduced by the growth cost *c*, a carrier division produces a plasmid-free daughter with probability *μ*, and mating re-introduces 2μ into plasmid-free cells at relative rate *ρ*. With time *G* measured in population doublings,

    dx/dG = ln2 · x [(ρ − c)(1 − x) − (1 − c) μ] / (1 − c x)

2μ persists in the long run only if *ρ* > *c* + (1 − *c*)*μ*, at the equilibrium *x*\* = 1 − (1 − *c*)*μ* / (*ρ* − *c*). The full derivation is in Supplementary Note 1.

## Quick start

```bash
pip install -r requirements.txt
python make_figures.py        # all figures -> figures/ (PDF + PNG), about 15 s
python scripts/tables.py      # numbers in Fig. 1A, Table S3, Table S4
python scripts/checks.py      # numerical checks of the closed-form results and the simulation
```

Each figure can also be made on its own, for example `python scripts/figS1.py`. The notebook `notebooks/figures.ipynb` runs the same scripts and shows the figures inline.

## Figures and scripts

| Figure | Script | Output in `figures/` |
| --- | --- | --- |
| Figure 1A: generations to 50% carriers without mating | `scripts/fig1.py` | `Fig1_A_generations_to_50pct` |
| Figure 1B, C: long-term carrier fraction vs cost and re-introduction rate | `scripts/fig1.py` | `Fig1_BC_carrier_heatmaps` |
| Figure 1A–C, combined preview | `scripts/fig1.py` | `Fig1_combined` |
| Figure S1: tolerable cost with mating | `scripts/figS1.py` | `FigS1_tolerable_cost` |
| Figure S2: comparison with Johnson et al. (2021) | `scripts/figS2.py` | `FigS2_comparison` |

All figures use a Helvetica-metric font (`fonts/`), no text smaller than 8 pt, editable text in PDFs and a transparent background.

## Repository layout

```
twomu/          model.py       closed-form results (time to 50% carriers, equilibrium, c_crit)
                simulation.py  serial-transfer simulation (deterministic growth, binomial transfer)
                style.py       shared figure style
scripts/        fig1.py, figS1.py, figS2.py, tables.py, checks.py
notebooks/      figures.ipynb
data/           johnson2021_fig9B.png (Fig. S2A; CC BY 4.0, see data/README.md)
fonts/          TeX Gyre Heros as TrueType (GUST Font License, see fonts/README.md)
figures/        generated figures
```

## Reproducibility

Figure 1, Figure S1 and Table S3 come from closed-form expressions and are exact. Figure S2 and Table S4 come from 2,000 simulated populations per scenario with a fixed random seed (20261009). NumPy does not guarantee identical random streams across versions, so with another NumPy version individual simulated populations may differ; summary values agree to within sampling error.

## Third-party material

- `data/johnson2021_fig9B.png`: Johnson MS et al. (2021) *eLife* 10:e63910, https://doi.org/10.7554/eLife.63910, © 2021 Johnson et al., CC BY 4.0.
- `fonts/`: TeX Gyre Heros, © B. Jackowski and J. M. Nowacki, GUST Font License.


