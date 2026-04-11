"""Tests for the agent-catalog Python SDK discovery module."""
import json
from typing import Any

import httpx
import pytest

from agent_catalog.discovery import (
    CatalogNotFoundError,
    CatalogValidationError,
    fetch_catalog,
)

VALID_CATALOG = {
    "agentCatalogVersion": 1,
    "origin": "https://example.com",
    "name": "X",
    "description": "x",
}


def make_transport(responses: dict[str, dict[str, Any]]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url in responses:
            r = responses[url]
            return httpx.Response(
                status_code=r.get("status", 200),
                headers=r.get("headers", {"Content-Type": "application/json"}),
                content=r["body"],
            )
        return httpx.Response(404, content=b"not found")
    return httpx.MockTransport(handler)


@pytest.mark.asyncio
async def test_fetches_from_well_known_fallback():
    transport = make_transport({
        "https://example.com/.well-known/agent-catalog.json": {
            "body": json.dumps(VALID_CATALOG).encode(),
        }
    })
    async with httpx.AsyncClient(transport=transport) as client:
        catalog = await fetch_catalog("https://example.com", client=client)
    assert catalog["origin"] == "https://example.com"


@pytest.mark.asyncio
async def test_uses_link_header_when_present():
    transport = make_transport({
        "https://example.com/": {
            "headers": {
                "Content-Type": "text/html",
                "Link": '<https://example.com/custom-catalog.json>; rel="agent-catalog"',
            },
            "body": b"<html></html>",
        },
        "https://example.com/custom-catalog.json": {
            "body": json.dumps(VALID_CATALOG).encode(),
        },
        "https://example.com/.well-known/agent-catalog.json": {
            "body": json.dumps({**VALID_CATALOG, "name": "WRONG"}).encode(),
        },
    })
    async with httpx.AsyncClient(transport=transport) as client:
        catalog = await fetch_catalog(
            "https://example.com/", client=client, use_link_header=True
        )
    assert catalog["name"] == "X"


@pytest.mark.asyncio
async def test_rejects_non_https_origin():
    transport = make_transport({})
    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(ValueError, match="HTTPS"):
            await fetch_catalog("http://example.com", client=client)


@pytest.mark.asyncio
async def test_rejects_invalid_catalog_from_wire():
    transport = make_transport({
        "https://example.com/.well-known/agent-catalog.json": {
            "body": json.dumps({"origin": "https://example.com"}).encode(),
        }
    })
    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(CatalogValidationError):
            await fetch_catalog("https://example.com", client=client)


@pytest.mark.asyncio
async def test_404_raises_not_found():
    transport = make_transport({})
    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(CatalogNotFoundError):
            await fetch_catalog("https://example.com", client=client)
