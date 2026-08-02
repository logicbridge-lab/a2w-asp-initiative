"""Repository validation helpers for local use and GitHub Actions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_ASP_FIELDS = {
    "domain",
    "owner",
    "version",
    "scope",
    "resources",
    "actions",
    "policies",
    "workflows",
    "auth",
    "evidence",
    "observability",
}
REQUIRED_TARGET_FIELDS = {
    "domain",
    "category",
    "task_relevant_paths",
    "rate_limit_rps",
    "screenshots",
    "validation_status",
    "validation_notes",
}


def _load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(path.parents[1])}: invalid JSON ({exc})")
        return None


def validate_repository(root: Path) -> list[str]:
    """Return a list of repository asset validation errors."""
    errors: list[str] = []
    schema_path = root / "spec" / "schema.json"
    example_path = root / "examples" / "example-asp-draft.json"
    targets_path = root / "crawler" / "config" / "targets-month-one.json"

    for path in (schema_path, example_path, targets_path):
        if not path.is_file():
            errors.append(f"Missing required asset: {path.relative_to(root)}")

    if errors:
        return errors

    schema = _load_json(schema_path, errors)
    example = _load_json(example_path, errors)
    targets = _load_json(targets_path, errors)
    if errors:
        return errors

    required_by_schema = set(schema.get("required", []))
    if required_by_schema != REQUIRED_ASP_FIELDS:
        errors.append("ASP schema required fields do not match the canonical 11-field contract")

    missing_example_fields = REQUIRED_ASP_FIELDS - set(example)
    if missing_example_fields:
        errors.append(f"Example ASP missing fields: {sorted(missing_example_fields)}")

    domain_entries = targets.get("domains") if isinstance(targets, dict) else None
    if not isinstance(domain_entries, list) or not domain_entries:
        errors.append("Target configuration must contain a non-empty domains list")
        return errors

    names: set[str] = set()
    for index, entry in enumerate(domain_entries):
        if not isinstance(entry, dict):
            errors.append(f"Target {index} is not an object")
            continue
        missing = REQUIRED_TARGET_FIELDS - set(entry)
        if missing:
            errors.append(f"Target {entry.get('domain', index)} missing fields: {sorted(missing)}")
        domain = entry.get("domain")
        if domain in names:
            errors.append(f"Duplicate target domain: {domain}")
        names.add(domain)
        if entry.get("validation_status") not in {"unverified", "approved", "excluded"}:
            errors.append(f"Target {domain} has invalid validation_status")

    return errors


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate A2W/ASP repository assets.")
    parser.add_argument("root", nargs="?", default=Path(__file__).resolve().parents[1], type=Path)
    args = parser.parse_args()
    findings = validate_repository(args.root.resolve())
    if findings:
        print("Validation failed:")
        print("\n".join(f"- {item}" for item in findings))
        raise SystemExit(1)
    print("Repository assets are valid.")
