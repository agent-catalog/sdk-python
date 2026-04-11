"""Tests for installMcp."""
from typing import Any

import pytest

from agent_catalog.mcps import install_mcp


def test_returns_http_connection():
    mcp: dict[str, Any] = {
        "id": "x", "name": "X", "description": "x",
        "transport": "http", "url": "https://mcp.example.com/x",
    }
    result = install_mcp(mcp)
    assert result["connection"] == {"kind": "http", "url": "https://mcp.example.com/x"}


def test_returns_stdio_connection():
    mcp: dict[str, Any] = {
        "id": "x", "name": "X", "description": "x",
        "transport": "stdio",
        "command": "acme-mcp",
        "args": ["--root", "/x"],
        "install": {"npm": "@acme/mcp-x"},
    }
    result = install_mcp(mcp)
    assert result["connection"] == {"kind": "stdio", "command": "acme-mcp", "args": ["--root", "/x"]}
    assert result["installInstructions"] == {"npm": "@acme/mcp-x"}
