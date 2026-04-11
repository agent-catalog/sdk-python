"""Schema + cross-reference validation for agent-catalog manifests."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

import jsonschema
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = REPO_ROOT / "spec" / "schema" / "agent-catalog-v1.schema.json"


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)


@lru_cache(maxsize=1)
def _load_validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text())
    return Draft202012Validator(schema)


def validate_catalog(catalog: Any) -> ValidationResult:
    validator = _load_validator()
    errors: list[str] = []
    for err in validator.iter_errors(catalog):
        path = "/" + "/".join(str(p) for p in err.absolute_path) if err.absolute_path else "(root)"
        errors.append(f"{path}: {err.message}")
    if errors:
        return ValidationResult(valid=False, errors=errors)

    xref_errors = _check_cross_references(catalog)
    if xref_errors:
        return ValidationResult(valid=False, errors=xref_errors)

    return ValidationResult(valid=True, errors=[])


def _check_cross_references(catalog: dict[str, Any]) -> list[str]:
    auth = catalog.get("auth") or {}
    identity_ids = {entry["id"] for entry in (auth.get("identity") or [])}
    authorization_ids = {entry["id"] for entry in (auth.get("authorization") or [])}

    errors: list[str] = []
    for collection_name in ("apis", "mcps", "agents", "skills", "sdks", "docs"):
        entries = catalog.get(collection_name) or []
        for entry in entries:
            requires = entry.get("requires")
            if not requires:
                continue
            ident = requires.get("identity")
            if ident and ident not in identity_ids:
                errors.append(
                    f"/{collection_name}/{entry['id']}/requires/identity: dangling reference '{ident}'"
                )
            auth_ref = requires.get("authorization")
            if auth_ref and auth_ref not in authorization_ids:
                errors.append(
                    f"/{collection_name}/{entry['id']}/requires/authorization: dangling reference '{auth_ref}'"
                )
    return errors
