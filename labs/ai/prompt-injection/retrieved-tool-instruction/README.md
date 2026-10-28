# Untrusted retrieval triggers an agent tool

A deterministic toy agent interprets a tool directive embedded in retrieved text. This is a trust-boundary simulation, not a real LLM exploit or a model safety benchmark.

## Run

From the repository root:

```sh
python lab.py up ai.prompt-injection.retrieved-tool-instruction
python lab.py verify ai.prompt-injection.retrieved-tool-instruction
python lab.py up ai.prompt-injection.retrieved-tool-instruction --fixed
python lab.py verify ai.prompt-injection.retrieved-tool-instruction --fixed
python lab.py down ai.prompt-injection.retrieved-tool-instruction --purge
```

Endpoint: `127.0.0.1:8104` (HTTP).

## Reproduce

POST /agent with retrieved_document containing TOOL: read_internal_note. The vulnerable simulator returns a synthetic internal note. The `verify` command performs this bounded demonstration and checks normal behavior too.

## Remediation

Keep retrieved content separate from tool authorization. The fixed simulator never dispatches tools from retrieved text. Production agents also need independent tool policies and model-specific evaluation.

The target and fixed branch are in `tooling/target.py`; demonstration assertions are in `tooling/verify.py`. Both are shared to keep these starter labs small. Data is synthetic and resets with each request or process. No real credentials or external services are used.
