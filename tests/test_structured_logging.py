import json
import logging
from contextlib import contextmanager
from typing import Iterator, List

from sosmed_scanner.log import log_event
from sosmed_scanner.network import HttpResult
from sosmed_scanner.scanner import scan_username

LOGGER_NAME = "structured_logging_test"


class _ListHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__(logging.DEBUG)
        self.messages: List[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.messages.append(record.getMessage())


@contextmanager
def capture(name: str, level: int = logging.DEBUG) -> Iterator[List[str]]:
    """Pasang penangkap langsung di logger, tidak bergantung pada caplog."""
    logger = logging.getLogger(name)
    handler = _ListHandler()
    saved_level, saved_disabled = logger.level, logger.disabled
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.disabled = False
    try:
        yield handler.messages
    finally:
        logger.removeHandler(handler)
        logger.setLevel(saved_level)
        logger.disabled = saved_disabled


def test_log_event_emits_valid_json():
    logger = logging.getLogger(LOGGER_NAME)
    with capture(LOGGER_NAME) as messages:
        log_event(logger, "fetch_done", url="https://x.com/a", status=200)
    assert json.loads(messages[0]) == {
        "event": "fetch_done",
        "url": "https://x.com/a",
        "status": 200,
    }


def test_log_event_handles_non_serializable_values():
    logger = logging.getLogger(LOGGER_NAME)
    with capture(LOGGER_NAME) as messages:
        log_event(logger, "scan_done", error=ValueError("boom"))
    payload = json.loads(messages[0])
    assert payload["event"] == "scan_done"
    assert payload["error"] == "boom"


def test_log_event_respects_level():
    logger = logging.getLogger(LOGGER_NAME)
    with capture(LOGGER_NAME, logging.INFO) as messages:
        log_event(logger, "hidden")
        log_event(logger, "shown", level=logging.INFO)
    assert [json.loads(m)["event"] for m in messages] == ["shown"]


def test_scan_username_logs_json_events():
    def fake_fetch(url):
        return HttpResult(url=url, status=200)

    with capture("sosmed_scanner.scanner") as messages:
        scan_username("octocat", platforms=["github"], fetch=fake_fetch)
    assert [json.loads(m)["event"] for m in messages] == [
        "scan_start",
        "platform_result",
        "scan_done",
    ]