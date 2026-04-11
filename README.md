# agent-catalog (Python SDK)

Python consumer SDK for the agent-catalog spec. Fetch, validate, and act on agent-catalog manifests.

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

See `../../spec/spec.md` for the spec.
