import unittest
import urllib.error
from unittest import mock

from sosmed_scanner.network import USER_AGENT, fetch_status

URLOPEN = "sosmed_scanner.network.urllib.request.urlopen"


class TestFetchStatus(unittest.TestCase):
    def test_returns_status_on_success(self):
        response = mock.MagicMock()
        response.status = 200
        with mock.patch(URLOPEN) as urlopen:
            urlopen.return_value.__enter__.return_value = response
            result = fetch_status("https://example.com/user")

        self.assertEqual(result.status, 200)
        self.assertIsNone(result.error)

    def test_sends_user_agent_header(self):
        response = mock.MagicMock()
        response.status = 200
        with mock.patch(URLOPEN) as urlopen:
            urlopen.return_value.__enter__.return_value = response
            fetch_status("https://example.com/user")
            request = urlopen.call_args[0][0]

        self.assertEqual(request.get_header("User-agent"), USER_AGENT)

    def test_http_error_returns_status_code(self):
        error = urllib.error.HTTPError(
            "https://example.com/x", 404, "Not Found", None, None
        )
        with mock.patch(URLOPEN, side_effect=error):
            result = fetch_status("https://example.com/x")

        self.assertEqual(result.status, 404)
        self.assertIsNone(result.error)

    def test_url_error_is_reported_not_raised(self):
        with mock.patch(URLOPEN, side_effect=urllib.error.URLError("no route")):
            result = fetch_status("https://example.com/x")

        self.assertIsNone(result.status)
        self.assertIn("no route", result.error)

    def test_timeout_is_reported_not_raised(self):
        with mock.patch(URLOPEN, side_effect=TimeoutError("timed out")):
            result = fetch_status("https://example.com/x")

        self.assertIsNone(result.status)
        self.assertIn("timed out", result.error)


if __name__ == "__main__":
    unittest.main()