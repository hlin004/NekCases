# cyl11_1 (cyl_Re100)

2D external flow past a circular cylinder using Nek5000, Re = 100 (unsteady,
vortex shedding).

## Case setup
- Cylinder of diameter D = 1 centered at the origin
- Domain: x in [-50, 50], y in [-25, 25], built in Gmsh (cylinder.geo -> cylinder.msh)
- Boundaries (Gmsh physical groups):
    Wal (2): cylinder surface, no-slip wall
    Inf (4): inflow, uniform u = U = 1, v = 0
    Out (5): outflow
    Sym (3): top/bottom far field, symmetry
- Fluid: rho = 1, Re = U D / nu = 100 (par: viscosity = -100)
- Same mesh family, SIZE and .usr logic as cyl_Re20; only Re and endTime differ

## Discretization
- 3480 quadrilateral spectral elements
- Polynomial order N = 5 (lx1 = 6), dealiasing lxd = 12
- Incompressible Navier-Stokes, fixed dt = 1e-4, endTime = 200 (200 D/U)
- Fields written every 2 time units (100 files)
- Drag every 10 steps via torque_calc (Cd = 2F, scale = 2);
  history points via hpts() every 10 steps

## Result
- Steady symmetric wake until t ~ 150 (Cd ~ 1.077); vortex shedding then
  starts and is still growing at t = 200 (Cd 1.26-1.31 over t = 190-200).
  The run is not long enough for converged mean Cd or Strouhal number.
- Only the streamwise force (dragx) was recorded, so no lift history.

## Folder layout
- cylinder.par / .usr / SIZE / .re2 / .ma2 / .geo / .msh : case inputs
- cylinder.his : probe-point list read by hpts()
- data/ : raw run output (cylinder0.f00001-f00100, cylinder.log.5,
  cylinder.nek5000); git-ignored, kept locally only
- post_process/ : drag history (cd11_1.txt), full history-point output
  (cylinder.his.zip; unpack with `unzip`), image (pinf at 0.png)
