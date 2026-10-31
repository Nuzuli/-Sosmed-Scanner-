"""Low-level HTTP helpers built on the standard library only."""

import logging
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Optional

from sosmed_scanner import __version__
from sosmed_scanner.log import log_event

USER_AGENT = (
    f"sosmed-scanner/{__version__} (+https://github.com/Nuzuli/-Sosmed-Scanner-)"
)
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
    log_event(logger, "fetch_start", url=url, timeout=timeout)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            log_event(logger, "fetch_done", url=url, status=response.status)
            return HttpResult(url=url, status=response.status)
    except urllib.error.HTTPError as error:
        log_event(logger, "fetch_done", url=url, status=error.code)
        return HttpResult(url=url, status=error.code)
    except OSError as error:
        # URLError and TimeoutError are both subclasses of OSError.
        log_event(logger, "fetch_failed", url=url, error=error)
        return HttpResult(url=url, status=None, error=str(error))