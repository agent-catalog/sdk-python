# agent-catalog (Python SDK)

Python SDK for fetching and validating agent-catalog manifests. Handles the discovery handshake, schema validation, hash verification, and provides helpers for installing skills and MCPs.

Requires Python 3.11+.

## Install

```bash
pip install agent-catalog
```

## Quick start

```python
from agent_catalog import fetch_catalog

catalog = await fetch_catalog("https://acme.example")
print(len(catalog.get("apis") or []), "APIs available")
```

## API

- `fetch_catalog(url)` -- discovery handshake (Link header, well-known fallback), schema validation, optional signature/hash verification
- `install_skill(entry)` -- runs `npx skills add <source>`
- `install_mcp(entry)` -- stdio: runs the install command; http/sse: returns connection details
- `fetch_doc(entry)` -- fetches a docs entry, verifies hash, returns markdown and token count
- `build_signed_request(url, key)` -- signs an outgoing request per RFC 9421 (Web Bot Auth)

## Spec

The full spec is in the [agent-catalog/spec](https://github.com/agent-catalog/spec) repo.
