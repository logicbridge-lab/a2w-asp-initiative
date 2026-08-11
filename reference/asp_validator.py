"""Small dependency-free validator for A2W/ASP Draft 0.1 profiles."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {
    "domain", "owner", "version", "scope", "resources", "actions", "policies",
    "workflows", "auth", "evidence", "observability",
}
DOMAIN_RE = re.compile(r"^([a-z0-9]+(?:-[a-z0-9]+)*\.)+[a-z]{2,}$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def validate_profile(profile: Any) -> list[str]:
    """Return deterministic validation errors; empty means Draft 0.1 valid."""
    if not isinstance(profile, dict):
        return ["profile must be a JSON object"]
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(profile))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    domain = profile.get("domain")
    if not isinstance(domain, str) or not DOMAIN_RE.fullmatch(domain):
        errors.append("domain must be a lowercase hostname")
    version = profile.get("version")
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        errors.append("version must use semantic versioning")

    owner = profile.get("owner")
    if not isinstance(owner, dict) or not isinstance(owner.get("name"), str) or not isinstance(owner.get("contact_email"), str):
        errors.append("owner must include name and contact_email")
    for name in ("resources", "actions", "workflows"):
        if name in profile and not isinstance(profile[name], list):
            errors.append(f"{name} must be an array")
    if "policies" in profile and not isinstance(profile["policies"], dict):
        errors.append("policies must be an object")

    auth = profile.get("auth")
    if not isinstance(auth, dict) or auth.get("type") not in {"none", "api_key", "oauth2", "custom"} or not isinstance(auth.get("required"), bool) or not isinstance(auth.get("parameters"), dict):
        errors.append("auth must include required, supported type, and parameters")
    evidence = profile.get("evidence")
    if not isinstance(evidence, dict) or evidence.get("source") not in {"domain_authored", "inferred"} or not isinstance(evidence.get("confidence"), (int, float)) or not 0 <= evidence.get("confidence", -1) <= 1 or not isinstance(evidence.get("references"), list):
        errors.append("evidence must include source, confidence from 0 to 1, and references")
    observability = profile.get("observability")
    if not isinstance(observability, dict) or not isinstance(observability.get("logs"), bool) or not isinstance(observability.get("metrics"), list) or not isinstance(observability.get("status_endpoint"), str) or not isinstance(observability.get("feedback_channel"), str):
        errors.append("observability must include logs, metrics, status_endpoint, and feedback_channel")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an A2W/ASP Draft 0.1 JSON profile.")
    parser.add_argument("profile", type=Path)
    args = parser.parse_args()
    try:
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid JSON: {exc}")
    errors = validate_profile(profile)
    if errors:
        print("Invalid ASP:")
        print("\n".join(f"- {error}" for error in errors))
        raise SystemExit(1)
    print("Valid A2W/ASP Draft 0.1 profile.")


if __name__ == "__main__":
    main()
