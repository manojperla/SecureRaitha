# Contributing

1. Choose a primary target category and technique, then create a scenario directory using `templates/lab` as a guide.
2. Add metadata and Compose configuration. For custom targets, create lab-local target, demonstrate, and remediation directories and extend the CLI verifier dispatch accordingly.
3. Add meaningful checks for both vulnerable and fixed behavior, including a normal control case.
4. Run `python -m unittest discover -s tests -v` and `python lab.py catalog`.
5. On a Docker host, run up, verify, up --fixed, verify --fixed, and down --purge for the new lab. Confirm remote interfaces cannot reach its published port.

Do not commit secrets, real personal data, malware, or demonstrations targeting arbitrary remote hosts. The starter verifier deliberately accepts only loopback ports.
