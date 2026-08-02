"""Polite target preflight for A2W/ASP crawler candidates."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
import urllib.robotparser
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urljoin

USER_AGENT = "LogicBridge-A2W-Research/0.1 (+mailto:research@logicbridge.ai)"


@dataclass(frozen=True)
class PathCheck:
    path: str
    allowed: bool
    status_code: int | None
    detail: str


def robots_allows(robots_text: str, path: str, user_agent: str = USER_AGENT) -> bool:
    """Return whether robots.txt permits a path for this crawler's user agent."""
    parser = urllib.robotparser.RobotFileParser()
    parser.parse(robots_text.splitlines())
    return parser.can_fetch(user_agent, f"https://example.invalid{path}")


def _fetch(url: str, timeout: int) -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status, response.read().decode("utf-8", "replace")


def preflight_target(target: dict[str, object], timeout: int = 20) -> dict[str, object]:
    """Validate one target without crawling content beyond declared target paths."""
    domain = str(target["domain"])
    base_url = f"https://{domain}/"
    robots_url = urljoin(base_url, "robots.txt")
    try:
        robots_status, robots_text = _fetch(robots_url, timeout)
        robots_detail = f"HTTP {robots_status}"
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            robots_status, robots_text, robots_detail = 404, "", "HTTP 404; no robots directives found"
        else:
            return {**target, "validation_status": "excluded", "validation_notes": f"robots.txt HTTP {exc.code}"}
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {**target, "validation_status": "excluded", "validation_notes": f"robots.txt unavailable: {type(exc).__name__}"}

    checks: list[PathCheck] = []
    raw_paths = target.get("task_relevant_paths", [])
    paths = raw_paths if isinstance(raw_paths, list) else []
    for path in paths:
        allowed = robots_allows(robots_text, str(path))
        if not allowed:
            checks.append(PathCheck(str(path), False, None, "blocked by robots.txt"))
            continue
        try:
            status, _ = _fetch(urljoin(base_url, str(path).lstrip("/")), timeout)
            checks.append(PathCheck(str(path), True, status, f"HTTP {status}"))
        except urllib.error.HTTPError as exc:
            checks.append(PathCheck(str(path), True, exc.code, f"HTTP {exc.code}"))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            checks.append(PathCheck(str(path), True, None, type(exc).__name__))

    usable = any(check.allowed and check.status_code == 200 for check in checks)
    status = "approved" if usable else "excluded"
    notes = f"robots.txt: {robots_detail}; usable target paths: {sum(check.allowed and check.status_code == 200 for check in checks)}/{len(checks)}"
    return {**target, "validation_status": status, "validation_notes": notes, "preflight": {"robots_url": robots_url, "robots_status": robots_status, "paths": [asdict(check) for check in checks]}}


def main() -> None:
    parser = argparse.ArgumentParser(description="Preflight A2W/ASP crawl targets against robots.txt and declared paths.")
    parser.add_argument("targets", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()
    data = json.loads(args.targets.read_text(encoding="utf-8"))
    data["domains"] = [preflight_target(target, args.timeout) for target in data["domains"]]
    args.output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    counts = {state: sum(item["validation_status"] == state for item in data["domains"]) for state in ("approved", "excluded", "unverified")}
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main()
