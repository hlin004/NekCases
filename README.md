# NekCases

A collection of simulation cases for [Nek5000](https://github.com/Nek5000/Nek5000) and
[nekRS](https://github.com/Nek5000/nekRS).

## Naming Convention

Each top-level directory is named after the code that runs it and the case it solves:

```
code_name-case_name
```

For example, `nek5000_cantera-flow_over_cylinder` is a flow-over-cylinder case run with
Nek5000 + Cantera.

## Contributing

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

### Guidelines

- Keep large binary files out of the repository where possible. Prefer a mesh generation
  script or compressed mesh (as in `nekrs_ascent-pb146/pb.re2.tgz`) over a large `.re2`.
- Do not commit simulation output — field files, logs, and restart files.
- Verify a case runs to completion before submitting it.
- Match the file naming already used in the repository so cases stay easy to compare.