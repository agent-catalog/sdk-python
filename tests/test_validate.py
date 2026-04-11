"""Tests for the agent-catalog Python SDK validation module."""
import json
from pathlib import Path

import pytest

from agent_catalog.validate import validate_catalog

REPO_ROOT = Path(__file__).resolve().parents[3]
GOLD_STANDARD = REPO_ROOT / "spec" / "conformance" / "positive" / "gold-standard.json"


def test_validates_gold_standard():
    catalog = json.loads(GOLD_STANDARD.read_text())
    result = validate_catalog(catalog)
    assert result.errors == []
    assert result.valid is True


def test_rejects_missing_version():
    result = validate_catalog({"origin": "https://example.com"})
    assert result.valid is False
    assert len(result.errors) > 0


def test_rejects_dangling_cross_reference():
    result = validate_catalog({
        "agentCatalogVersion": 1,
        "origin": "https://example.com",
        "apis": [{
            "id": "a",
            "name": "A",
            "description": "x",
            "format": "openapi",
            "url": "https://example.com/o.yaml",
            "requires": {"identity": "ghost"},
        }],
    })
    assert result.valid is False
    assert any("ghost" in err for err in result.errors)
