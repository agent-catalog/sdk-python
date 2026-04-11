"""Python consumer SDK for the agent-catalog spec."""
from .discovery import (
    CatalogNotFoundError,
    CatalogValidationError,
    fetch_catalog,
)
from .docs import fetch_doc
from .mcps import install_mcp
from .skills import install_skill
from .types import (
    AgentEntry,
    ApiEntry,
    AuthAuthorizationEntry,
    AuthIdentityEntry,
    AuthSection,
    Catalog,
    CommonEntryFields,
    DocEntry,
    McpEntry,
    Publisher,
    RequiresField,
    SdkEntry,
    SkillEntry,
)
from .validate import ValidationResult, validate_catalog
from .web_bot_auth import build_signed_request

__all__ = [
    "AgentEntry",
    "ApiEntry",
    "AuthAuthorizationEntry",
    "AuthIdentityEntry",
    "AuthSection",
    "Catalog",
    "CatalogNotFoundError",
    "CatalogValidationError",
    "CommonEntryFields",
    "DocEntry",
    "McpEntry",
    "Publisher",
    "RequiresField",
    "SdkEntry",
    "SkillEntry",
    "ValidationResult",
    "build_signed_request",
    "fetch_catalog",
    "fetch_doc",
    "install_mcp",
    "install_skill",
    "validate_catalog",
]
