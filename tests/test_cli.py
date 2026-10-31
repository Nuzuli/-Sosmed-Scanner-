import contextlib
import io
import json
import logging
import unittest
from unittest import mock

from sosmed_scanner.cli import format_results, main
from sosmed_scanner.scanner import FOUND, NOT_FOUND, ScanResult

SAMPLE = [
    ScanResult("GitHub", "https://github.com/alice", FOUND),
    ScanResult("GitLab", "https://gitlab.com/alice", NOT_FOUND),
    ScanResult("Reddit", "https://www.reddit.com/user/alice", "unknown", "HTTP 429"),
]

SCAN = "sosmed_scanner.cli.scan_username"


def run_main(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class TestCli(unittest.TestCase):
    def test_text_output(self):
        with mock.patch(SCAN, return_value=SAMPLE):
            code, out, _ = run_main(["alice"])
        self.assertEqual(code, 0)
        self.assertIn("GitHub", out)
        self.assertIn("found", out)
        self.assertIn("(HTTP 429)", out)

    def test_json_output(self):
        with mock.patch(SCAN, return_value=SAMPLE):
            code, out, _ = run_main(["alice", "--json"])
        data = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["platform"], "GitHub")
        self.assertEqual(data[0]["status"], FOUND)

    def test_arguments_are_forwarded(self):
        with mock.patch(SCAN, return_value=[]) as scan:
            run_main(["alice", "-p", "github", "--delay", "0"])
        scan.assert_called_once_with("alice", platforms=["github"], delay=0.0)

    def test_invalid_username_returns_exit_code_2(self):
        code, out, err = run_main(["bad name"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("ERROR:", err)
        self.assertIn("Username must be", err)

    def test_unknown_platform_returns_exit_code_2(self):
        code, _, err = run_main(["alice", "-p", "nope"])
        self.assertEqual(code, 2)
        self.assertIn("Unknown platform", err)

    def test_unknown_platform_is_rejected_before_scanning(self):
        with mock.patch(SCAN) as scan:
            code, out, err = run_main(["alice", "-p", "github", "-p", "nope"])
        self.assertEqual(code, 2)
        scan.assert_not_called()
        self.assertEqual(out, "")
        self.assertIn("ERROR:", err)
        self.assertIn("Unknown platform: nope", err)
        self.assertIn("Available:", err)

    def test_platform_names_are_case_insensitive(self):
        with mock.patch(SCAN, return_value=[]) as scan:
            code, _, _ = run_main(["alice", "-p", "GITHUB", "--delay", "0"])
        self.assertEqual(code, 0)
        scan.assert_called_once_with("alice", platforms=["GITHUB"], delay=0.0)

    def test_verbose_flag_controls_log_level(self):
        package_logger = logging.getLogger("sosmed_scanner")
        with mock.patch(SCAN, return_value=[]):
            run_main(["alice", "-v"])
            self.assertEqual(package_logger.level, logging.DEBUG)
            run_main(["alice"])
            self.assertEqual(package_logger.level, logging.WARNING)


class TestFormatResults(unittest.TestCase):
    def test_one_line_per_result(self):
        self.assertEqual(len(format_results(SAMPLE).splitlines()), 3)


if __name__ == "__main__":
    unittest.main()