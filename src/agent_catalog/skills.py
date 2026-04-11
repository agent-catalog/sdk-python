"""Skill installation via the vercel-labs/skills CLI."""
from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable

ExecFn = Callable[[str, list[str]], Awaitable[tuple[str, str]]]


async def _default_exec(command: str, args: list[str]) -> tuple[str, str]:
    proc = await asyncio.create_subprocess_exec(
        command, *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"{command} exited with code {proc.returncode}: {stderr.decode()}")
    return stdout.decode(), stderr.decode()


async def install_skill(
    skill: dict[str, Any],
    *,
    exec: ExecFn = _default_exec,
    refuse_unpinned: bool = False,
) -> dict[str, Any]:
    if refuse_unpinned and not skill.get("pinned", False):
        raise ValueError(f"Skill '{skill['id']}' is unpinned and refuse_unpinned was set")
    stdout, _ = await exec("npx", ["skills", "add", skill["source"], "-y"])
    return {"installed": True, "source": skill["source"], "output": stdout}
