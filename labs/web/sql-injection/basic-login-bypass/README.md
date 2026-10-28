# SQL injection in a login form

An interpolated SQLite query accepts an injected username and logs in as admin.

## Run

From the repository root:

```sh
python lab.py up web.sql-injection.basic-login-bypass
python lab.py verify web.sql-injection.basic-login-bypass
python lab.py up web.sql-injection.basic-login-bypass --fixed
python lab.py verify web.sql-injection.basic-login-bypass --fixed
python lab.py down web.sql-injection.basic-login-bypass --purge
```

Endpoint: `127.0.0.1:8101` (HTTP).

## Reproduce

POST /login with username admin' --  and any password. The demonstration checks that admin is returned. The `verify` command performs this bounded demonstration and checks normal behavior too.

## Remediation

Use parameterized queries. The fixed variant binds username and password as SQL parameters.

The target and fixed branch are in `tooling/target.py`; demonstration assertions are in `tooling/verify.py`. Both are shared to keep these starter labs small. Data is synthetic and resets with each request or process. No real credentials or external services are used.
