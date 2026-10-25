import contextlib
import io
import json
import unittest
import urllib.error
from unittest import mock

from sosmed_scanner.cli import main

URLOPEN = "sosmed_scanner.network.urllib.request.urlopen"


def run_main(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


def ok_response(status=200):
    response = mock.MagicMock()
    response.status = status
    manager = mock.MagicMock()
    manager.__enter__.return_value = response
    return manager


class TestEndToEnd(unittest.TestCase):
    def test_cli_to_network_found(self):
        with mock.patch(URLOPEN, return_value=ok_response()) as urlopen:
            code, out, _ = run_main(["alice", "-p", "github", "--delay", "0"])

        self.assertEqual(code, 0)
        self.assertIn("found", out)
        requested = urlopen.call_args[0][0]
        self.assertEqual(requested.full_url, "https://github.com/alice")

    def test_multiple_platforms_produce_one_line_each(self):
        error = urllib.error.HTTPError("u", 404, "Not Found", None, None)
        with mock.patch(URLOPEN, side_effect=error):
            code, out, _ = run_main(
                ["alice", "-p", "github", "-p", "dev", "--delay", "0"]
            )

        self.assertEqual(code, 0)
        self.assertEqual(len(out.strip().splitlines()), 2)
        self.assertIn("not_found", out)

    def test_network_failure_is_reported_as_unknown(self):
        with mock.patch(URLOPEN, side_effect=urllib.error.URLError("offline")):
            code, out, _ = run_main(["alice", "-p", "github", "--json", "--delay", "0"])

        data = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(data[0]["status"], "unknown")
        self.assertIn("offline", data[0]["detail"])

    def test_verbose_prints_debug_details_to_stderr(self):
        with mock.patch(URLOPEN, return_value=ok_response()):
            _, _, err = run_main(["alice", "-p", "github", "-v", "--delay", "0"])

        self.assertIn("DEBUG:", err)
        self.assertIn("https://github.com/alice", err)

    def test_quiet_mode_has_no_debug_output(self):
        with mock.patch(URLOPEN, return_value=ok_response()):
            _, _, err = run_main(["alice", "-p", "github", "--delay", "0"])

        self.assertEqual(err, "")


if __name__ == "__main__":
    unittest.main()