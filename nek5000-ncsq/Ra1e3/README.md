# Ra1e3 — square cavity, Ra = 10³, Pr = 0.71

Conduction-dominated natural convection: a single clockwise recirculation cell
with near-vertical isotherms.

Properties in `ncsq.par` are `viscosity = 8.35e-02`, `conductivity = 1.175e-01`,
giving an effective Ra of 999.9 and Pr of 0.7106 — within 0.01 % of target.

**Validated.** Hot-wall Nusselt numbers agree with the converged SEDG-LBM and
Wang et al. reference values to within 0.01 %:

| | Nu₀ | Nu₀ᵐᵃˣ | Nu₀ᵐⁱⁿ |
|---|---|---|---|
| SEDG-LBM (N=9) | 1.1178 | 1.5063 | 0.6913 |
| **Nek5000** | **1.11776** | **1.50622** | **0.691258** |

Mid-plane temperature profiles overlay the reference data — see
[`../report/ncsq_report.pdf`](../report/ncsq_report.pdf) §4.

`postproc/` holds the digitized reference profiles (`fig4a.csv`, `fig4b.csv`),
the extracted Nek5000 centrelines (`x=0.5.csv`, `y=0.5.csv`) and the ParaView
state file. See the [parent README](../README.md) for the full description,
geometry, and run instructions.
