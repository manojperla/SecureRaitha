# Cross-owner document access

Alice is authenticated, but document ownership is not checked.

## Run

From the repository root:

```sh
python lab.py up api.broken-object-authorization.cross-owner-document
python lab.py verify api.broken-object-authorization.cross-owner-document
python lab.py up api.broken-object-authorization.cross-owner-document --fixed
python lab.py verify api.broken-object-authorization.cross-owner-document --fixed
python lab.py down api.broken-object-authorization.cross-owner-document --purge
```

Endpoint: `127.0.0.1:8102` (HTTP).

## Reproduce

GET /documents/2 with Authorization: Bearer alice-demo-token returns Bob's synthetic document. The `verify` command performs this bounded demonstration and checks normal behavior too.

## Remediation

Check record ownership after authentication. The fixed variant returns 403 for Bob's document.

The target and fixed branch are in `tooling/target.py`; demonstration assertions are in `tooling/verify.py`. Both are shared to keep these starter labs small. Data is synthetic and resets with each request or process. No real credentials or external services are used.
