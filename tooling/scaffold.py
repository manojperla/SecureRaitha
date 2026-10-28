"""Generate the initial metadata and Compose files; not needed for deployment."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABS = [
    ('web', 'sql-injection', 'basic-login-bypass', 8101, 'SQL injection in a login form', 'CWE-89',
     'An interpolated SQLite query accepts an injected username and logs in as admin.',
     'POST /login with username admin\' --  and any password. The demonstration checks that admin is returned.',
     'Use parameterized queries. The fixed variant binds username and password as SQL parameters.'),
    ('api', 'broken-object-authorization', 'cross-owner-document', 8102, 'Cross-owner document access', 'CWE-639',
     'Alice is authenticated, but document ownership is not checked.',
     'GET /documents/2 with Authorization: Bearer alice-demo-token returns Bob\'s synthetic document.',
     'Check record ownership after authentication. The fixed variant returns 403 for Bob\'s document.'),
    ('network', 'insecure-service-config', 'exposed-admin-protocol', 8103, 'Unauthenticated TCP configuration access', 'CWE-306',
     'A toy TCP administrative service exposes a synthetic configuration value without authentication.',
     'Send GET CONFIG followed by a newline to the TCP port. PING remains a harmless readiness command.',
     'Remove configuration access from the unauthenticated listener. The fixed variant denies GET CONFIG; it does not implement a full authenticated management plane.'),
    ('ai', 'prompt-injection', 'retrieved-tool-instruction', 8104, 'Untrusted retrieval triggers an agent tool', 'CWE-94',
     'A deterministic toy agent interprets a tool directive embedded in retrieved text. This is a trust-boundary simulation, not a real LLM exploit or a model safety benchmark.',
     'POST /agent with retrieved_document containing TOOL: read_internal_note. The vulnerable simulator returns a synthetic internal note.',
     'Keep retrieved content separate from tool authorization. The fixed simulator never dispatches tools from retrieved text. Production agents also need independent tool policies and model-specific evaluation.'),
]

for category, technique, name, port, title, cwe, scenario, reproduction, mitigation in LABS:
    folder = ROOT / 'labs' / category / technique / name
    folder.mkdir(parents=True, exist_ok=True)
    lab_id = f'{category}.{technique}.{name}'
    metadata = {'id': lab_id, 'title': title, 'category': category, 'tags': [technique],
                'difficulty': 'beginner', 'kind': 'synthetic', 'runtime': 'docker-compose',
                'port': port, 'protocol': 'tcp' if category == 'network' else 'http',
                'resources': {'memory_mb': 128}, 'external_dependencies': [],
                'simulation': category == 'ai'}
    if category != 'ai':
        metadata['cwe'] = [cwe]
    (folder / 'lab.yaml').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    (folder / 'compose.yaml').write_text(f'''services:
  target:
    build:
      context: ../../../..
      dockerfile: tooling/Dockerfile
    environment:
      LAB_KIND: {category}
      LAB_FIXED: "${{LAB_FIXED:-0}}"
    ports:
      - "127.0.0.1:{port}:8080"
    read_only: true
    cap_drop: [ALL]
    security_opt: ["no-new-privileges:true"]
    mem_limit: 128m
    pids_limit: 64
    networks: [lab]
networks:
  lab:
    internal: true
''', encoding='utf-8')
    (folder / 'README.md').write_text(f'''# {title}

{scenario}

## Run

From the repository root:

```sh
python lab.py up {lab_id}
python lab.py verify {lab_id}
python lab.py up {lab_id} --fixed
python lab.py verify {lab_id} --fixed
python lab.py down {lab_id} --purge
```

Endpoint: `127.0.0.1:{port}` ({metadata['protocol'].upper()}).

## Reproduce

{reproduction} The `verify` command performs this bounded demonstration and checks normal behavior too.

## Remediation

{mitigation}

The target and fixed branch are in `tooling/target.py`; demonstration assertions are in `tooling/verify.py`. Both are shared to keep these starter labs small. Data is synthetic and resets with each request or process. No real credentials or external services are used.
''', encoding='utf-8')
