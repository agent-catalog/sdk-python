"""Discovery handshake for agent-catalog."""
from __future__ import annotations

import re
from urllib.parse import urlparse

import httpx

from .types import Catalog
from .validate import validate_catalog


class CatalogNotFoundError(Exception):
    def __init__(self, origin: str) -> None:
        super().__init__(f"Catalog not found at {origin} (404)")
        self.origin = origin


class CatalogValidationError(Exception):
    def __init__(self, errors: list[str]) -> None:
        super().__init__("Fetched catalog failed validation:\n  " + "\n  ".join(errors))
        self.errors = errors


_LINK_RE = re.compile(r'<([^>]+)>\s*;\s*rel\s*=\s*"?agent-catalog"?', re.IGNORECASE)


async def fetch_catalog(
    origin: str,
    *,
    client: httpx.AsyncClient | None = None,
    use_link_header: bool = False,
) -> Catalog:
    if not origin.startswith("https://"):
        raise ValueError("agent-catalog requires HTTPS origins; refusing non-HTTPS URL")

    own_client = client is None
    if own_client:
        client = httpx.AsyncClient()

    try:
        catalog_url: str | None = None
        if use_link_header:
            try:
                probe = await client.get(origin)
                link = probe.headers.get("Link")
                if link:
                    match = _LINK_RE.search(link)
                    if match:
                        candidate_str = match.group(1)
                        # Resolve relative URLs against the origin
                        if candidate_str.startswith("/"):
                            parsed_origin = urlparse(origin)
                            candidate_str = f"{parsed_origin.scheme}://{parsed_origin.netloc}{candidate_str}"
                        if not candidate_str.startswith("https://"):
                            raise ValueError(
                                "Link header points at a non-HTTPS URL; refusing"
                            )
                        catalog_url = candidate_str
            except ValueError:
                raise
            except Exception:
                pass  # probe failures are not fatal — fall back to well-known

        if not catalog_url:
            parsed = urlparse(origin)
            catalog_url = f"{parsed.scheme}://{parsed.netloc}/.well-known/agent-catalog.json"

        response = await client.get(catalog_url, headers={"Accept": "application/json"})
        if response.status_code == 404:
            raise CatalogNotFoundError(origin)
        if response.status_code >= 400:
            raise RuntimeError(f"Failed to fetch catalog from {catalog_url}: HTTP {response.status_code}")

        catalog = response.json()
        result = validate_catalog(catalog)
        if not result.valid:
            raise CatalogValidationError(result.errors)
        return catalog  # type: ignore[return-value]
    finally:
        if own_client and client is not None:
            await client.aclose()
