"""Low-level HTTP helpers built on the standard library only."""

import logging
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Optional

USER_AGENT = "sosmed-scanner/0.2 (+https://github.com/Nuzuli/-Sosmed-Scanner-)"
DEFAULT_TIMEOUT = 8.0

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class HttpResult:
    """Outcome of a single HTTP request."""

    url: str
    status: Optional[int]
    error: Optional[str] = None


def fetch_status(url: str, timeout: float = DEFAULT_TIMEOUT) -> HttpResult:
    """Request a public URL and return its HTTP status code.

    Network problems never raise: they are reported through ``error``.
    """
    logger.debug("GET %s (timeout=%ss)", url, timeout)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return HttpResult(url=url, status=response.status)
    except urllib.error.HTTPError as error:
        logger.debug("HTTP %s from %s", error.code, url)
        return HttpResult(url=url, status=error.code)
    except OSError as error:
        # URLError and TimeoutError are both subclasses of OSError.
        logger.debug("Request failed for %s: %s", url, error)
        return HttpResult(url=url, status=None, error=str(error))