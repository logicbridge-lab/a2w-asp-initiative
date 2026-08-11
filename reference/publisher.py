"""Publish a validated ASP to a static site's well-known location."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from reference.asp_validator import validate_profile


def publish(profile_path: Path, public_directory: Path) -> Path:
    """Validate profile_path and copy it to public_directory/.well-known/asp."""
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    errors = validate_profile(profile)
    if errors:
        raise ValueError("; ".join(errors))
    destination = public_directory / ".well-known" / "asp"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish a validated ASP to a static public directory.")
    parser.add_argument("profile", type=Path)
    parser.add_argument("public_directory", type=Path)
    args = parser.parse_args()
    try:
        print(publish(args.profile, args.public_directory))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to publish ASP: {exc}")


if __name__ == "__main__":
    main()
