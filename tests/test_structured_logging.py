import unittest
import urllib.error
from unittest import mock

from sosmed_scanner.network import HttpResult, fetch_status
from sosmed_scanner.scanner import scan_username

NETWORK_LOGGER = "sosmed_scanner.network"
SCANNER_LOGGER = "sosmed_scanner.scanner"
URLOPEN = "sosmed_scanner.network.urllib.request.urlopen"


def fake_fetch(url):
    return HttpResult(url=url, status=200 if "github" in url else 404)


class TestNetworkLogging(unittest.TestCase):
    def test_success_logs_start_and_done_fields(self):
        response = mock.MagicMock()
        response.status = 200
        with mock.patch(URLOPEN) as urlopen:
            urlopen.return_value.__enter__.return_value = response
            with self.assertLogs(NETWORK_LOGGER, level="DEBUG") as captured:
                fetch_status("https://example.com/alice", timeout=3)

        messages = [record.getMessage() for record in captured.records]
        self.assertEqual(
            messages,
            [
                "fetch_start url=https://example.com/alice timeout=3",
                "fetch_done url=https://example.com/alice status=200",
            ],
        )

    def test_http_error_logs_status_field(self):
        error = urllib.error.HTTPError("u", 404, "Not Found", None, None)
        with mock.patch(URLOPEN, side_effect=error):
            with self.assertLogs(NETWORK_LOGGER, level="DEBUG") as captured:
                fetch_status("https://example.com/none")

        messages = [record.getMessage() for record in captured.records]
        self.assertIn("fetch_done url=https://example.com/none status=404", messages)

    def test_network_failure_logs_error_field(self):
        failure = urllib.error.URLError("offline")
        with mock.patch(URLOPEN, side_effect=failure):
            with self.assertLogs(NETWORK_LOGGER, level="DEBUG") as captured:
                fetch_status("https://example.com/x")

        messages = [record.getMessage() for record in captured.records]
        self.assertTrue(
            any(m.startswith("fetch_failed url=https://example.com/x error=")
                for m in messages)
        )


class TestScannerLogging(unittest.TestCase):
    def test_scan_logs_structured_summary(self):
        with self.assertLogs(SCANNER_LOGGER, level="DEBUG") as captured:
            scan_username("alice", platforms=["github", "gitlab"], fetch=fake_fetch)

        messages = [record.getMessage() for record in captured.records]
        self.assertEqual(messages[0], "scan_start username=alice platforms=2 delay=0.0")
        self.assertIn(
            "platform_result platform=GitHub status=found "
            "url=https://github.com/alice",
            messages,
        )
        self.assertIn(
            "platform_result platform=GitLab status=not_found "
            "url=https://gitlab.com/alice",
            messages,
        )
        self.assertEqual(messages[-1], "scan_done username=alice checked=2 found=1")


if __name__ == "__main__":
    unittest.main()