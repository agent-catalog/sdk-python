"""Web Bot Auth (RFC 9421) request signing helper."""
from __future__ import annotations

import time
from typing import Any, Awaitable, Callable
from urllib.parse import urlparse

SignFn = Callable[[str], Awaitable[str]]


async def build_signed_request(
    *,
    url: str,
    method: str,
    key_id: str,
    signature_agent: str,
    sign: SignFn,
    ttl_seconds: int = 300,
) -> dict[str, Any]:
    created = int(time.time())
    expires = created + ttl_seconds
    parsed = urlparse(url)
    authority = parsed.netloc
    sig_params = (
        f'("@authority" "@method");keyid="{key_id}";created={created};'
        f'expires={expires};tag="web-bot-auth"'
    )
    signature_input = f"sig1={sig_params}"
    canonical = (
        f'"@authority": {authority}\n'
        f'"@method": {method.upper()}\n'
        f'"@signature-params": {sig_params}'
    )
    signature_value = await sign(canonical)
    return {
        "url": url,
        "method": method.upper(),
        "headers": {
            "Signature": f"sig1=:{signature_value}:",
            "Signature-Input": signature_input,
            "Signature-Agent": signature_agent,
        },
    }
