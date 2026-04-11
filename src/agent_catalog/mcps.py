"""MCP entry installation/connection helpers."""
from __future__ import annotations

from typing import Any


def install_mcp(mcp: dict[str, Any]) -> dict[str, Any]:
    transport = mcp.get("transport")
    if transport == "http":
        url = mcp.get("url")
        if not url:
            raise ValueError(f"MCP entry '{mcp['id']}' has transport: http but no url")
        return {"connection": {"kind": "http", "url": url}}
    if transport == "sse":
        url = mcp.get("url")
        if not url:
            raise ValueError(f"MCP entry '{mcp['id']}' has transport: sse but no url")
        return {"connection": {"kind": "sse", "url": url}}
    if transport == "stdio":
        command = mcp.get("command")
        if not command:
            raise ValueError(f"MCP entry '{mcp['id']}' has transport: stdio but no command")
        result: dict[str, Any] = {
            "connection": {
                "kind": "stdio",
                "command": command,
                "args": mcp.get("args") or [],
            }
        }
        if mcp.get("install"):
            result["installInstructions"] = mcp["install"]
        return result
    raise ValueError(f"Unknown MCP transport: {transport}")
