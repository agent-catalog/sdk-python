"""Tests for installSkill."""
from typing import Any
from unittest.mock import AsyncMock

import pytest

from agent_catalog.skills import install_skill


@pytest.mark.asyncio
async def test_invokes_npx_skills_add():
    exec_mock = AsyncMock(return_value=("installed", ""))
    skill: dict[str, Any] = {
        "id": "test-skill",
        "name": "test-skill",
        "description": "x",
        "source": "owner/repo",
        "pinned": False,
    }
    result = await install_skill(skill, exec=exec_mock)
    exec_mock.assert_awaited_once_with("npx", ["skills", "add", "owner/repo", "-y"])
    assert result["installed"] is True


@pytest.mark.asyncio
async def test_refuses_unpinned_when_set():
    exec_mock = AsyncMock()
    skill: dict[str, Any] = {
        "id": "test-skill",
        "name": "test-skill",
        "description": "x",
        "source": "owner/repo",
        "pinned": False,
    }
    with pytest.raises(ValueError, match="pinned"):
        await install_skill(skill, exec=exec_mock, refuse_unpinned=True)
    exec_mock.assert_not_awaited()
