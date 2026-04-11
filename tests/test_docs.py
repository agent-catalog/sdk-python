"""Tests for fetchDoc."""
from typing import Any

import httpx
import pytest

from agent_catalog.docs import fetch_doc


def make_client(body: bytes) -> httpx.AsyncClient:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=body)
    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


@pytest.mark.asyncio
async def test_fetches_doc_content():
    client = make_client(b"# Hello\n\nDoc content.")
    doc: dict[str, Any] = {
        "id": "x", "name": "x", "description": "x",
        "url": "https://example.com/doc.md",
        "tokens": 100,
    }
    result = await fetch_doc(doc, client=client)
    assert "# Hello" in result["content"]
    assert result["tokens"] == 100
    await client.aclose()


@pytest.mark.asyncio
async def test_verifies_matching_hash():
    client = make_client(b"hello world")
    doc: dict[str, Any] = {
        "id": "x", "name": "x", "description": "x",
        "url": "https://example.com/doc.md",
        "hash": "sha256:b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
    }
    result = await fetch_doc(doc, client=client)
    assert result["content"] == "hello world"
    await client.aclose()


@pytest.mark.asyncio
async def test_throws_on_hash_mismatch():
    client = make_client(b"different content")
    doc: dict[str, Any] = {
        "id": "x", "name": "x", "description": "x",
        "url": "https://example.com/doc.md",
        "hash": "sha256:b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
    }
    with pytest.raises(ValueError, match="hash"):
        await fetch_doc(doc, client=client)
    await client.aclose()
