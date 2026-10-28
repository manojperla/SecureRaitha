# New lab checklist

Create `labs/<category>/<technique>/<scenario>/` with:

- `lab.yaml`: JSON object with id, title, category, tags, difficulty, kind, runtime, port, resources, external_dependencies.
- `compose.yaml`: build definition with loopback publication and the isolation settings used by existing labs.
- `README.md`: scenario, startup, reproduction, expected results, fix, and cleanup.
- Optional `target/`, `demonstrate/`, `remediation/`: lab-specific implementation when the shared starter runtime is insufficient.

Use an existing lab as the executable example. Integrate the new demonstration with `tooling/verify.py` and add vulnerable/fixed coverage under `tests/`. Metadata alone does not implement a new target.
