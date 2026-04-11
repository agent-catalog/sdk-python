"""Doc entry fetcher."""
from __future__ import annotations

import hashlib
from typing import Any

import httpx


async def fetch_doc(
    doc: dict[str, Any],
    *,
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    own_client = client is None
    if own_client:
        client = httpx.AsyncClient()
    try:
        response = await client.get(doc["url"])
        if response.status_code >= 400:
            raise RuntimeError(f"Failed to fetch doc {doc['url']}: HTTP {response.status_code}")
        content = response.text
        expected_hash = doc.get("hash")
        if expected_hash:
            actual = "sha256:" + hashlib.sha256(content.encode()).hexdigest()
            if actual != expected_hash:
                raise ValueError(
                    f"Doc hash mismatch for {doc['url']}: expected {expected_hash}, got {actual}"
                )
        result: dict[str, Any] = {"content": content}
        if "tokens" in doc:
            result["tokens"] = doc["tokens"]
        return result
    finally:
        if own_client and client is not None:
            await client.aclose()
