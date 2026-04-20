# agent-catalog (Python SDK)

Python consumer SDK for agent-catalog v1. Handles the full discovery handshake, schema validation, hash and signature verification, and provides helpers for acting on catalog entries.

Requires Python 3.11+.

## Install

```bash
pip install agent-catalog
```

## Quick start

```python
from agent_catalog import fetch_catalog

catalog = await fetch_catalog("https://acme.example")
# catalog is validated against the JSON Schema

for api in catalog.get("apis") or []:
    print(api["name"], api["url"])
```

## API

**`fetch_catalog(url, options?)`**

Runs the full discovery handshake: checks for a `Link: rel="agent-catalog"` header first, falls back to `/.well-known/agent-catalog.json`, validates the response against the bundled JSON Schema, optionally verifies the Sigstore signature. Returns a typed dict or raises a typed exception. HTTPS only; cross-origin redirects trigger re-validation.

**`install_skill(entry, options?)`**

Runs `npx skills add <source>` for a `skills[]` entry. Respects the `pinned` flag — raises by default on `pinned: false` entries unless the caller opts in.

**`install_mcp(entry, options?)`**

For `transport: stdio` entries, runs the install command from the entry's `install` map. For `transport: http` and `transport: sse` entries, returns the connection details without starting the server.

**`fetch_doc(entry, options?)`**

Fetches a `docs[]` entry URL, verifies the SHA-256 hash if present, and returns the markdown content and advisory token count.

**`build_signed_request(url, identity_key)`**

Signs an outgoing HTTP request per RFC 9421 (Web Bot Auth) using the provided identity key. Returns the request with `Signature` and `Signature-Input` headers attached.

## Related repos

- [agent-catalog/spec](https://github.com/agent-catalog/spec) — the normative specification and JSON Schema
- [agent-catalog/server](https://github.com/agent-catalog/server) — reference server and CLI
- [agent-catalog/sdk-typescript](https://github.com/agent-catalog/sdk-typescript) — TypeScript consumer SDK
- [agent-catalog/examples](https://github.com/agent-catalog/examples) — gold-standard example deployment
