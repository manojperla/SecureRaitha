# SecureRaitha

Deployable, intentionally vulnerable learning labs, grouped by target and tagged by technique.

| Category | Starter lab | Local port |
| --- | --- | --- |
| Web | SQLite login injection | 8101 |
| API | Cross-owner document access | 8102 |
| Network | Unauthenticated TCP administrative protocol | 8103 |
| AI | Retrieved instruction triggers tool use (deterministic simulation) | 8104 |

## Quick start

Requires Python 3.10+ and Docker with Docker Compose v2, configured for Linux containers. No Python packages are required. Initial image builds need internet access to pull the Python base image.

```sh
python lab.py list
python lab.py up web.sql-injection.basic-login-bypass
python lab.py verify web.sql-injection.basic-login-bypass
python lab.py up web.sql-injection.basic-login-bypass --fixed
python lab.py verify web.sql-injection.basic-login-bypass --fixed
python lab.py down web.sql-injection.basic-login-bypass --purge
```

`up` builds, starts, and verifies behavior. `--fixed` replaces the running vulnerable variant at the same port. `reset <id>` recreates a lab and removes its volumes; add `--fixed` to reset to the fixed variant. `down` stops one lab. Use `down --purge` for complete Compose volume cleanup. Images remain cached.

## Layout

`labs/<target>/<technique>/<scenario>/` contains deployment, metadata, and instructions. Each lab has one primary category; tags describe overlaps. Shared starter targets and demonstrations live in `tooling/target.py` and `tooling/verify.py`. More complex labs can introduce their own `target/`, `demonstrate/`, and `remediation/` directories.

`lab.yaml` and generated `catalog.yaml` use JSON syntax, a valid YAML subset, so the launcher needs no YAML dependency. Regenerate the index with `python lab.py catalog` after metadata changes. The CLI reads lab metadata directly.

## Local verification without Docker

```sh
python -m unittest discover -s tests -v
```

This starts temporary loopback services and verifies all four vulnerable and fixed variants. It checks application behavior, not container builds or network isolation.

For manual development, set `LAB_KIND` to `web`, `api`, `network`, or `ai`, optionally set `LAB_PORT` and `LAB_FIXED=1`, then run `python tooling/target.py`. The default listener is `127.0.0.1:8080`. Compose sets its own internal listener and publishes only to host loopback.

## Scope

These are purpose-built synthetic labs, not reproductions of vendor CVEs. The AI example uses a toy directive interpreter and needs no model, API key, or downloads. Its fixed variant illustrates a trust boundary, not a universal prompt-injection defense.

See [the lab standard](docs/lab-standard.md), [contributing](docs/contributing.md), and [isolation](docs/isolation.md).
