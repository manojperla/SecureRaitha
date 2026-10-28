# Unauthenticated TCP configuration access

A toy TCP administrative service exposes a synthetic configuration value without authentication.

## Run

From the repository root:

```sh
python lab.py up network.insecure-service-config.exposed-admin-protocol
python lab.py verify network.insecure-service-config.exposed-admin-protocol
python lab.py up network.insecure-service-config.exposed-admin-protocol --fixed
python lab.py verify network.insecure-service-config.exposed-admin-protocol --fixed
python lab.py down network.insecure-service-config.exposed-admin-protocol --purge
```

Endpoint: `127.0.0.1:8103` (TCP).

## Reproduce

Send GET CONFIG followed by a newline to the TCP port. PING remains a harmless readiness command. The `verify` command performs this bounded demonstration and checks normal behavior too.

## Remediation

Remove configuration access from the unauthenticated listener. The fixed variant denies GET CONFIG; it does not implement a full authenticated management plane.

The target and fixed branch are in `tooling/target.py`; demonstration assertions are in `tooling/verify.py`. Both are shared to keep these starter labs small. Data is synthetic and resets with each request or process. No real credentials or external services are used.
