"""Tests for buildSignedRequest."""
import pytest

from agent_catalog.web_bot_auth import build_signed_request


@pytest.mark.asyncio
async def test_attaches_signed_headers():
    async def stub_sign(canonical: str) -> str:
        return "stub-signature"
    result = await build_signed_request(
        url="https://example.com/api",
        method="GET",
        key_id="test-key",
        signature_agent="https://agent.example",
        sign=stub_sign,
    )
    assert result["headers"]["Signature"] == "sig1=:stub-signature:"
    assert result["headers"]["Signature-Agent"] == "https://agent.example"
    assert 'keyid="test-key"' in result["headers"]["Signature-Input"]
    assert 'tag="web-bot-auth"' in result["headers"]["Signature-Input"]
