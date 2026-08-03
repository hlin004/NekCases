# PDshear_1 — doubly periodic double shear layer, Dellar configuration (Nek5000)

Spectral-element counterpart to the shear-layer test used to probe the
incompressible limit of lattice Boltzmann schemes. This directory is the
**baseline**: no explicit filter, no Mach scaling.

**Reference:** P. J. Dellar, "Incompressible limits of lattice Boltzmann
equations using multiple relaxation times," *Journal of Computational Physics*,
vol. 190, no. 2, pp. 351–370, Sep. 2003.
doi:[10.1016/S0021-9991(03)00279-1](https://doi.org/10.1016/S0021-9991(03)00279-1)

## Problem

Unit square `[0,1]²`, **fully periodic**, 2-D incompressible.

Initial condition (`useric` in `shear.usr`), with ρ = 20 and δ = 0.05:

```
u = tanh(ρ(y − 1/4))     y ≤ 1/2          v = δ·sin(2π(x + 1/4))
    tanh(ρ(3/4 − y))     y > 1/2
```

Note the **`x + 1/4` phase shift** in the transverse perturbation — this is the
Minion–Brown/Dellar placement, which centres the roll-up in the domain. The
stock Nek5000 `shear4` example uses `sin(2πx)` instead; everything else about
the profile is the same family.

Re = 10³ (`viscosity = -1e3`). This is well below the Re = 10⁴–3×10⁴ range
Dellar reports, and ρ = 20 is a wider (easier) layer than the k = 30/80 used
there — so this is a resolved, low-Re baseline of that configuration, not a
quantitative reproduction of the paper's figures.

The passive-scalar block from the original example is commented out in
`useric`; this run is velocity-only.

## Discretization

| | |
|---|---|
| Mesh | 16 × 16 spectral elements, uniform, from `shear.box` via `genbox` |
| Order | `lx1 = 17`, `lx2 = 15` → **256 × 256** grid points |
| Over-integration | `lxd = 25` (`dealiasing = yes`) — full 3/2 rule |
| Stabilization | **none** beyond dealiasing (no explicit filter) |
| Time | `dt = 1e-3`, variable dt at `targetCFL = 1`, `endTime = 1` |
| Output | `writeControl = runTime`, every 0.1 → 10 field files |

## Result

Completed to t = 1.0 in **2640 steps** on 4 MPI ranks (Nek5000 20.0-dev,
53 s wall). Peak vorticity, logged each step by `userchk`, ends at ≈ 15.1;
the `max|u| > 8` abort guard never fired. Clean, stable run — dealiasing alone
is sufficient at this resolution and Reynolds number.

## Files

```
shear.box       genbox input: -16 -16 elements on [0,1]², P,P,P,P
shear.re2       mesh produced from it (rename of box.re2)
shear.ma2       partition map from genmap
shear.par       run-time parameters (see table above)
shear.usr       useric (IC) + userchk (peak-vorticity monitor / blow-up guard)
SIZE            ldim=2, lx1=17, lxd=25, lelg=300
shear.log.4     4-rank run log
shear0.f00001..10   field output, t = 0.1 … 1.0
shear.nek5000   VisIt/ParaView metadata
vorticity contour.pvsm   ParaView state file for the vorticity contours
README.txt      original build recipe (superseded by "Running" below)
build.log, makefile, nek5000, obj/   build artifacts — regenerable
```

## Related directories

This directory was `PDshear_1`, one of four variants sharing the same mesh and
`SIZE` byte-for-byte and differing only in `shear.par` and (for 3/4) a
Mach-number rescaling of the initial velocity in `shear.usr`:

| | filter | viscosity | IC scaling |
|---|---|---|---|
| **PDshear_1** | off | `-1e3` (Re) | — |
| PDshear_2 | explicit, 2 modes, w = 0.05 | `-1e3` (Re) | — |
| PDshear_3 | off | `8.66025e-7` (dimensional, Ma/Re) | × Ma, Ma = √3/2000 |
| PDshear_4 | explicit, 2 modes, w = 0.05 | `8.66025e-7` | × Ma, Ma = √3/2000 |

The Ma = √3/2000 factor in 3/4 rescales the velocity to lattice-Boltzmann
magnitudes so the SEM result can be compared against an LB run at the same
lattice Mach number — the compressibility-error question Dellar's paper is
about. 1/2 are the incompressible reference.

**`PDshear_2`, `PDshear_3` and `PDshear_4` were moved to Trash on 2026-08-02**
and are no longer on disk; they are restorable from
`~/.local/share/Trash/files/`.

## Running

```bash
export NEK_SOURCE_ROOT=/path/to/Nek5000
genbox && mv box.re2 shear.re2      # feed it shear.box
genmap                              # feed it shear
makenek shear
nekbmpi shear 4
visnek shear
```

`SESSION.NAME` here points at `.../PaulDellar_shear4/shear_17/` (a stale path
from an earlier `lx1 = 17` directory name); `nekbmpi` rewrites it, or fix it
before running elsewhere.

## Provenance

Renamed 2026-08-03. Older data, logs, plot scripts and ParaView state files may
still reference the old path.

| | |
|---|---|
| **Old path** | `/home/hailu/Nek5000/run/cases/PaulDellar_shear4/PDshear_1` |
| **New path** | `/home/hailu/Nek5000/run/cases/PaulDellar_shear4/shear_Dellar_Re1e3_N256_nofilt` |

The rename does not update `SESSION.NAME` (already stale — see above), the
absolute paths inside `vorticity contour.pvsm`, or the build directory recorded
in `makefile` / `.state` / `build.log`.