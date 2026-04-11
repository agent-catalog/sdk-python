"""Type definitions for agent-catalog entries.

Uses TypedDict for structural compatibility with the JSON shapes the spec defines.
Optional fields are marked with NotRequired (Python 3.11+).
"""
from __future__ import annotations

from typing import Any, Literal, NotRequired, TypedDict


class CommonEntryFields(TypedDict):
    id: str
    name: str
    description: str
    whenToUse: NotRequired[str]
    hash: NotRequired[str]
    tags: NotRequired[list[str]]
    requires: NotRequired["RequiresField"]


class RequiresField(TypedDict, total=False):
    identity: str
    authorization: str


class ApiEntry(CommonEntryFields):
    format: Literal["openapi", "asyncapi", "graphql", "grpc", "api-catalog"]
    url: str


class McpEntry(CommonEntryFields):
    transport: Literal["stdio", "http", "sse"]
    url: NotRequired[str]
    command: NotRequired[str]
    args: NotRequired[list[str]]
    install: NotRequired[dict[str, str]]
    card: NotRequired[str]


class AgentEntry(CommonEntryFields):
    card: str


class SkillEntry(CommonEntryFields):
    source: str
    pinned: bool
    commit: NotRequired[str]


class SdkEntry(CommonEntryFields):
    language: str
    package: str
    docs: NotRequired[str]


class DocEntry(CommonEntryFields):
    url: str
    tokens: NotRequired[int]
    purpose: NotRequired[str]


class AuthIdentityEntry(TypedDict):
    id: str
    name: NotRequired[str]
    description: str
    scheme: str
    keyDirectoryUrl: NotRequired[str]


class AuthAuthorizationEntry(TypedDict):
    id: str
    name: NotRequired[str]
    description: str
    scheme: str
    metadataUrl: NotRequired[str]
    header: NotRequired[str]
    obtainAt: NotRequired[str]


class AuthSection(TypedDict, total=False):
    identity: list[AuthIdentityEntry]
    authorization: list[AuthAuthorizationEntry]


class Publisher(TypedDict, total=False):
    name: str
    url: str
    contact: str


class Catalog(TypedDict):
    agentCatalogVersion: Literal[1]
    origin: str
    name: NotRequired[str]
    description: NotRequired[str]
    publisher: NotRequired[Publisher]
    apis: NotRequired[list[ApiEntry]]
    mcps: NotRequired[list[McpEntry]]
    agents: NotRequired[list[AgentEntry]]
    skills: NotRequired[list[SkillEntry]]
    sdks: NotRequired[list[SdkEntry]]
    docs: NotRequired[list[DocEntry]]
    auth: NotRequired[AuthSection]
    signature: NotRequired[dict[str, Any] | None]
