# NekCases

A collection of simulation cases for [Nek5000](https://github.com/Nek5000/Nek5000) and
[nekRS](https://github.com/Nek5000/nekRS), including setups instrumented for in-situ
visualization with [Ascent](https://github.com/Alpine-DAV/ascent).

## Naming Convention

Each top-level directory is named after the code that runs it and the case it solves:

```
code_name-case_name
```

For example, `nek5000_cantera-flow_over_cylinder` is a flow-over-cylinder case run with
Nek5000 + Cantera.

## Cases

| Case | Code | Description |
| --- | --- | --- |
| [nek5000-flow_over_cylinder/](nek5000-flow_over_cylinder/) | Nek5000 | Flow over a cylinder (`cyl_Re20`) |
| [nek5000-lid_driven_cavity/](nek5000-lid_driven_cavity/) | Nek5000 | Lid-driven cavity, 2D and 3D variants |
| [nek5000-periodic_pipe/](nek5000-periodic_pipe/) | Nek5000 | Periodic pipe flow |
| [nek5000-TGV/](nek5000-TGV/) | Nek5000 | Taylor-Green vortex |
| [nekrs_ascent-pb146/](nekrs_ascent-pb146/) | nekRS + Ascent | 146-pebble bed, with in-situ rendering |
| [nekrs_ascent-turbPipe/](nekrs_ascent-turbPipe/) | nekRS + Ascent | Turbulent pipe flow, with in-situ rendering |

Each case directory has its own `README` with the details specific to that setup.

## Layout of a Case

Cases follow the usual Nek5000/nekRS file conventions:

| File | Purpose |
| --- | --- |
| `*.par` | Runtime parameters |
| `*.usr` | User routines (Nek5000) |
| `*.udf` / `*.oudf` | Host and device user routines (nekRS) |
| `SIZE` | Compile-time array sizes (Nek5000) |
| `*.re2`, `*.ma2` | Mesh and partitioning files |
| `*.box`, `*.geo`, `*.msh` | Mesh generation inputs |
| `ascent_actions.yaml` | In-situ visualization actions (Ascent cases) |
| `run.sh`, `script.sh` | Job submission / run scripts |

## Contributing

Contributions of new cases and fixes to existing ones are welcome.

### Adding a New Case

1. Create a top-level directory named `code_name-case_name` (see
   [Naming Convention](#naming-convention)).
2. Include everything needed to reproduce the run: mesh inputs, `.par`, user routines,
   `SIZE`, and any run scripts.
3. Add a `README.md` in the case directory covering:
   - what the case simulates and the relevant physical parameters
   - the code version it was tested with
   - how to build and run it
   - expected output, and any reference results if you have them
4. Add a `.gitignore` for run artifacts (output fields, logs, `obj/`, compiled binaries).
5. Add a row for the case to the [Cases](#cases) table above.

### Guidelines

- Keep large binary files out of the repository where possible. Prefer a mesh generation
  script or compressed mesh (as in `nekrs_ascent-pb146/pb.re2.tgz`) over a large `.re2`.
- Do not commit simulation output — field files, logs, and restart files.
- Verify a case runs to completion before submitting it.
- Match the file naming already used in the repository so cases stay easy to compare.

### Submitting

Fork the repository, make your changes on a branch, and open a pull request against
`main` describing the case and how you tested it. For bugs or questions about an existing
case, open an issue.
