import json
import logging

from sosmed_scanner.log import log_event
from sosmed_scanner.network import HttpResult
from sosmed_scanner.scanner import scan_username

LOGGER_NAME = "sosmed_scanner.test"


def test_log_event_emits_valid_json(caplog):
    logger = logging.getLogger(LOGGER_NAME)
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        log_event(logger, "fetch_done", url="https://x.com/a", status=200)
    payload = json.loads(caplog.records[0].getMessage())
    assert payload == {
        "event": "fetch_done",
        "url": "https://x.com/a",
        "status": 200,
    }


def test_log_event_handles_non_serializable_values(caplog):
    logger = logging.getLogger(LOGGER_NAME)
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        log_event(logger, "scan_done", error=ValueError("boom"))
    payload = json.loads(caplog.records[0].getMessage())
    assert payload["event"] == "scan_done"
    assert payload["error"] == "boom"


def test_log_event_respects_level(caplog):
    logger = logging.getLogger(LOGGER_NAME)
    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        log_event(logger, "hidden")
        log_event(logger, "shown", level=logging.INFO)
    events = [json.loads(r.getMessage())["event"] for r in caplog.records]
    assert events == ["shown"]


def test_scan_username_logs_json_events(caplog):
    def fake_fetch(url):
        return HttpResult(url=url, status=200)

    with caplog.at_level(logging.DEBUG, logger="sosmed_scanner.scanner"):
        scan_username("octocat", platforms=["github"], fetch=fake_fetch)
    events = [json.loads(r.getMessage())["event"] for r in caplog.records]
    assert events == ["scan_start", "platform_result", "scan_done"]