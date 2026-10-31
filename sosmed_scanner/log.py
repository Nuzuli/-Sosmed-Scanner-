"""Structured (JSON) logging helper."""
from __future__ import annotations

import json
import logging
from typing import Any


def log_event(
    logger: logging.Logger,
    event: str,
    *,
    level: int = logging.DEBUG,
    **fields: Any,
) -> None:
    """Emit one log record whose message is a JSON object.

    The payload always has an "event" key; extra keyword arguments
    become additional keys. Non-serializable values fall back to str().
    """
    if not logger.isEnabledFor(level):
        return
    payload = {"event": event, **fields}
    logger.log(level, json.dumps(payload, default=str, sort_keys=True))