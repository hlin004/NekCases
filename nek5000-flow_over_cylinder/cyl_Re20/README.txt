# cyl10_4 (cyl_Re20)

2D external flow past a circular cylinder using Nek5000, Re = 20 (steady flow).

## Case setup
- Cylinder of diameter D = 1 centered at the origin
- Domain: x in [-50, 50], y in [-25, 25], built in Gmsh (cylinder.geo -> cylinder.msh)
- Boundaries (Gmsh physical groups):
    Wal (2): cylinder surface, no-slip wall
    Inf (4): inflow, uniform u = U = 1, v = 0
    Out (5): outflow
    Sym (3): top/bottom far field, symmetry
- Fluid: rho = 1, Re = U D / nu = 20 (par: viscosity = -20)

## Discretization
- 3480 quadrilateral spectral elements
- Polynomial order N = 5 (lx1 = 6), dealiasing lxd = 12
- Incompressible Navier-Stokes, fixed dt = 1e-4, endTime = 100 (100 D/U)
- Fields written every 2 time units (50 files)
- Drag/lift every 10 steps via torque_calc (Cd = 2F, scale = 2);
  history points via hpts() every 10 steps

## Result
- Drag coefficient at t = 100: Cd = 2.044 (pressure 1.233 + viscous 0.811)

## Folder layout
- cylinder.par / .usr / SIZE / .re2 / .ma2 / .geo / .msh : case inputs
- cylinder.his : probe-point list read by hpts()
- data/ : raw run output (cylinder0.f00001-f00050, cylinder.log.5,
  cylinder.nek5000); git-ignored, kept locally only
- post_process/ : drag history (cd10_4.txt), full history-point output
  (cylinder.his.xz; unpack with `xz -dk`), ParaView state (paraview output.pvsm) and images (mesh,
  velocity/pressure/vorticity contours, streamlines, pressure at infinity)
