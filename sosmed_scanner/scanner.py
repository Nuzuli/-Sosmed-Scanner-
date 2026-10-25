"""Scan public profile pages for a username."""

import logging
import re
import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Sequence

from sosmed_scanner.network import HttpResult, fetch_status

logger = logging.getLogger(__name__)

PLATFORMS: Dict[str, str] = {
    "GitHub": "https://github.com/{username}",
    "GitLab": "https://gitlab.com/{username}",
    "Reddit": "https://www.reddit.com/user/{username}",
    "Medium": "https://medium.com/@{username}",
    "DEV": "https://dev.to/{username}",
}

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9._-]{1,39}$")

FOUND = "found"
NOT_FOUND = "not_found"
UNKNOWN = "unknown"


class InvalidUsernameError(ValueError):
    """Raised when a username contains unsupported characters."""


@dataclass(frozen=True)
class ScanResult:
    """Result of checking one platform."""

    platform: str
    url: str
    status: str
    detail: Optional[str] = None


def validate_username(username: str) -> str:
    """Return the cleaned username or raise InvalidUsernameError."""
    cleaned = username.strip()
    if not USERNAME_PATTERN.match(cleaned):
        raise InvalidUsernameError(
            "Username must be 1-39 characters: letters, digits, '.', '_' or '-'."
        )
    return cleaned


def classify(result: HttpResult) -> str:
    """Map an HTTP result to found, not_found, or unknown."""
    if result.status == 200:
        return FOUND
    if result.status == 404:
        return NOT_FOUND
    return UNKNOWN


def select_platforms(names: Optional[Sequence[str]]) -> Dict[str, str]:
    """Return the platforms to scan, matching names case-insensitively."""
    if not names:
        return dict(PLATFORMS)
    lookup = {name.lower(): name for name in PLATFORMS}
    selected: Dict[str, str] = {}
    for name in names:
        key = lookup.get(name.lower())
        if key is None:
            raise ValueError(f"Unknown platform: {name}")
        selected[key] = PLATFORMS[key]
    return selected


def scan_username(
    username: str,
    platforms: Optional[Sequence[str]] = None,
    fetch: Callable[[str], HttpResult] = fetch_status,
    delay: float = 0.0,
    sleep: Callable[[float], None] = time.sleep,
) -> List[ScanResult]:
    """Check a username on each selected platform, one request at a time."""
    cleaned = validate_username(username)
    targets = select_platforms(platforms)
    results: List[ScanResult] = []

    for index, (name, template) in enumerate(targets.items()):
        if index > 0 and delay > 0:
            sleep(delay)
        url = template.format(username=cleaned)
        logger.debug("Checking %s", name)
        outcome = fetch(url)
        detail = outcome.error
        if detail is None and outcome.status not in (200, 404):
            detail = f"HTTP {outcome.status}"
        results.append(
            ScanResult(
                platform=name,
                url=url,
                status=classify(outcome),
                detail=detail,
            )
        )
    logger.debug("Scan finished: %d platform(s) checked", len(results))
    return results