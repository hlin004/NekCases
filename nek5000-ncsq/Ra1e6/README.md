# Ra1e6 — square cavity, Ra = 10⁶, Pr = 0.71

Convection-dominated natural convection: the central vortex breaks into a
horizontally elongated core with two secondary eddies, motion is confined to
thin wall boundary layers, and the core is stably stratified.

| | Nu₀ |
|---|---|
| SEDG-LBM | 8.820 |
| Wang et al. | 8.8192 |
| Dixit and Babu | 8.805 |
| Le Quéré | 8.8252 |
| **Nek5000** | **8.86074** |

## Known issue: properties are under-precise

`ncsq.par` rounds the properties to two significant figures:

```
viscosity    = 2.6e-03      # exact value for Ra=1e6, Pr=0.71 is 2.63915e-03
conductivity = 3.7e-03      # exact value is 3.71711e-03
```

This gives an **effective Ra = 1.0198 × 10⁶ (+1.98 %)** and **Pr = 0.7027
(−1.03 %)**. At the sensitivity `Nu₀ ∝ Ra^0.273` implied by the reference data,
the Ra shift alone predicts **+0.53 %** in Nu₀ — matching the observed 0.40–0.63 %
offset. The result is a correct solution of a slightly different problem, not a
solver error.

Set the exact values above and rerun before using this case quantitatively. No
grid-refinement study has been done; at this Ra the thermal boundary layer spans
about half an element (~4 GLL points), far coarser than the E = 576, N = 9 mesh
used in the reference.

See [`../report/ncsq_report.pdf`](../report/ncsq_report.pdf) §5–6 for the full
analysis, and the [parent README](../README.md) for geometry and run
instructions.
