# Case: ncsq — natural convection in a square cavity

**Code:** Nek5000 (20.0-dev)
**Purpose:** Benchmark the Nek5000 Boussinesq natural-convection setup against
published reference solutions at two Rayleigh numbers.
**Status:** Both cases run to completion and are validated. See
[`report/ncsq_report.pdf`](report/ncsq_report.pdf).

**Reference:** S. S. Patel, M. Min, K. C. Uga, and T. Lee, "A spectral-element
discontinuous Galerkin lattice Boltzmann method for simulating natural
convection heat transfer in a horizontal concentric annulus," *Computers &
Fluids*, vol. 95, pp. 197–209, May 2014.
doi:[10.1016/j.compfluid.2014.02.021](https://doi.org/10.1016/j.compfluid.2014.02.021)

## Cases

| | Target Ra | Pr | `viscosity` | `conductivity` |
|---|---|---|---|---|
| [`Ra1e3/`](Ra1e3/) | 10³ | 0.71 | `8.35e-02` | `1.175e-01` |
| [`Ra1e6/`](Ra1e6/) | 10⁶ | 0.71 | `2.6e-03` | `3.7e-03` |

The two cases share an identical mesh, `SIZE` and `ncsq.usr`. They differ **only**
in the transport properties set in `ncsq.par`.

## Problem

Unit square `[0,1]²`, 2-D incompressible, Boussinesq.

- All four walls no-slip, `u = 0`.
- Left wall `x = 0` hot, `T_h = 1`; right wall `x = 1` cold, `T_c = 0`
  (set in `userbc`).
- Top and bottom walls adiabatic (`I` in the temperature BC field of `ncsq.box`).
- Initial condition: fluid at rest, `T ≡ 0`.
- Buoyancy applied in `userf` as the acceleration `ffy = 9.81*temp`.

With `rho = cp = beta = L = 1`, `ΔT = 1` and `g = 9.81`, the properties for a
target (Ra, Pr) follow from

```
mu = sqrt(g*Pr/Ra)          conductivity k = sqrt(g/(Pr*Ra))
Ra = g*beta*ΔT*L^3/(nu*alpha)       Pr = nu/alpha = mu*cp/k
```

## Discretization

| | |
|---|---|
| Mesh | 10 × 10 uniform spectral elements on `[0,1]²`, from `genbox` (`ncsq.box`) |
| Order | `lx1 = 8` → N = 7, giving 6 400 grid points |
| Formulation | `equation = incompNS`, `stressFormulation = yes` |
| Time | variable dt at `targetCFL = 0.4`, `endTime = 100` |
| Output | `writeControl = runTime`, interval 1 → 100 field files |
| Tolerance | `residualTol = 1e-06` |

## Results

Hot-wall Nusselt numbers, computed in post-processing from the final field.

**Ra = 10³ (`Ra1e3`)**

| | Nu₀ | Nu₀ᵐᵃˣ | Nu₀ᵐⁱⁿ |
|---|---|---|---|
| SEDG-LBM (N=9) | 1.1178 | 1.5063 | 0.6913 |
| Wang et al. | 1.1178 | 1.5063 | 0.6912 |
| de Vahl Davis | 1.117 | 1.505 | 0.692 |
| **Nek5000** | **1.11776** | **1.50622** | **0.691258** |

Within 0.01 % of the converged SEDG-LBM and Wang et al. values on all three
quantities. Mid-plane temperature profiles overlay the reference data.

**Ra = 10⁶ (`Ra1e6`)**

| | Nu₀ |
|---|---|
| SEDG-LBM | 8.820 |
| Wang et al. | 8.8192 |
| Dixit and Babu | 8.805 |
| Le Quéré | 8.8252 |
| **Nek5000** | **8.86074** |

0.40–0.63 % above the references.

### Known issue: `Ra1e6` properties are under-precise

`Ra1e6/ncsq.par` rounds the properties to two significant figures. Substituting
them back into the definitions gives an **effective Ra = 1.0198 × 10⁶ (+1.98 %)**
and **Pr = 0.7027 (−1.03 %)**, because `viscosity = 2.6e-03` instead of the exact
`2.63915e-03`. At the sensitivity `Nu₀ ∝ Ra^0.273` implied by the reference data,
that predicts a **+0.53 %** shift in Nu₀ — which is the size of the observed
offset. The discrepancy is therefore a property-specification artifact, not a
solver or discretization error.

To rerun at the intended conditions, set

```
viscosity    = 2.63915e-03
conductivity = 3.71711e-03
```

`Ra1e3` is unaffected: its four-digit properties give an effective Ra of 999.9.

No grid-refinement study was performed for either case. At Ra = 10⁶ the thermal
boundary layer spans roughly half an element (about four GLL points), which is
adequate but not generous, and is far coarser than the E = 576, N = 9 mesh used
in the reference.

## Layout

```
Ra1e3/, Ra1e6/
  ncsq.box        genbox input: -10 -10 elements on [0,1]², W walls, t/t/I/I
  ncsq.re2        mesh produced from it (rename of box.re2); identical in both cases
  ncsq.ma2        partition map from genmap
  ncsq.par        run-time parameters — the only file that differs between cases
  ncsq.usr        uservp / userf (buoyancy) / userbc (hot & cold walls) / useric
  SIZE            ldim=2, lx1=8, lxd=10, lelt=128
  postproc/       extracted results and ParaView state (tracked)

report/
  ncsq_report.pdf   combined report for both cases
  ncsq_report.tex   its source
  make_figs.py      regenerates the profile figures from Ra1e3/postproc
  figures/          field visualizations and generated profile plots
```

### `Ra1e3/postproc`

| File | Contents |
|---|---|
| `fig4a.csv` | Reference T(y) at x = 0.5, digitized from Fig. 4(a) of the paper |
| `fig4b.csv` | Reference T(x) at y = 0.5, digitized from Fig. 4(b) |
| `x=0.5.csv` | Nek5000 vertical mid-plane, ParaView Plot-Over-Line export |
| `y=0.5.csv` | Nek5000 horizontal mid-plane, same |
| `data.pvsm` | ParaView state used to produce the field figures |

## Running

```bash
export NEK_SOURCE_ROOT=/path/to/Nek5000
cd Ra1e3                       # or Ra1e6
genbox && mv box.re2 ncsq.re2  # feed it ncsq.box   (re2 is committed; only needed to rebuild)
genmap                         # feed it ncsq
makenek ncsq
nekbmpi ncsq 14
visnek ncsq
```

Rebuild the report figures and PDF with:

```bash
cd report && python3 make_figs.py && pdflatex ncsq_report.tex
```

## Provenance

Archived 2026-08-17 from `/home/hailu/Nek5000/run/cases/ncsq/{ncsq4,ncsq5}`.

### Renamed on archiving

The case directories were renamed on 2026-08-18 to identify them by Rayleigh
number rather than by their position in the original numbered series:

| Original | Archived as |
|---|---|
| `ncsq4` | [`Ra1e3/`](Ra1e3/) |
| `ncsq5` | [`Ra1e6/`](Ra1e6/) |

The old names still appear in the source directory listed above, in the original
`README.txt` files of that series, and in earlier draft write-ups that refer to
"case ncsq4" and "case ncsq5". Nothing inside the case files depends on the
directory name — the Nek5000 session name is `ncsq` in both — so the rename is
cosmetic and the cases run unchanged.

Only inputs and extracted results were copied. The raw field output
(`ncsq0.f00001`–`f00100`, ~94 MB across the two cases) and the build directories
were left in place and are excluded by `.gitignore`. `data.pvsm` contains
absolute paths to the original location and will need repointing before it opens
elsewhere.

The `ncsq` series in that directory contains further cases beyond these two —
higher Rayleigh numbers, a variable-Prandtl variant, and a low-Mach
variable-property study — which are not part of this archive.
