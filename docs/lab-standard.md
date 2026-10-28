# Lab standard

Every lab must declare a unique ID, title, category, technique tags, difficulty, kind, runtime, port, resource estimate, and external dependencies. Use one of web, api, network, or ai as the primary category. Metadata is JSON-compatible YAML. Keep IDs stable and ports unique.

Provide repeatable startup, normal-behavior checks, a bounded vulnerability demonstration, and a fixed variant that rejects the same demonstration without breaking normal behavior. Explain the scenario, expected results, mitigation, and limitations. All example data must be synthetic.

Compose deployments publish only on loopback and use disposable state, non-root processes, resource limits, and no host mounts. Document any lab requiring a different isolation model before adding it.

For CVE reproductions, use kind cve-reproduction and record the CVE, upstream advisory, exact affected version, image digest or dependency lock, and fixed version. The current shared Python base uses a version tag; it is not an immutable archival image.
