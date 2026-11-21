import unittest

from sosmed_scanner.network import HttpResult
from sosmed_scanner.scanner import (
    FOUND,
    NOT_FOUND,
    PLATFORMS,
    UNKNOWN,
    InvalidUsernameError,
    classify,
    scan_username,
    select_platforms,
    validate_username,
)


def fake_fetch_factory(statuses):
    """Build a fetch function that returns canned statuses by URL."""

    def fake_fetch(url):
        status = statuses.get(url, 404)
        if status is None:
            return HttpResult(url=url, status=None, error="timed out")
        return HttpResult(url=url, status=status)

    return fake_fetch


class TestValidateUsername(unittest.TestCase):
    def test_accepts_valid_username(self):
        self.assertEqual(validate_username("  john_doe-1.x "), "john_doe-1.x")

    def test_rejects_invalid_characters(self):
        for bad in ["", "a b", "a/b", "name?x=1", "x" * 40]:
            with self.subTest(username=bad):
                with self.assertRaises(InvalidUsernameError):
                    validate_username(bad)


class TestClassify(unittest.TestCase):
    def test_status_mapping(self):
        self.assertEqual(classify(HttpResult("u", 200)), FOUND)
        self.assertEqual(classify(HttpResult("u", 404)), NOT_FOUND)
        self.assertEqual(classify(HttpResult("u", 429)), UNKNOWN)
        self.assertEqual(classify(HttpResult("u", None, "boom")), UNKNOWN)


class TestSelectPlatforms(unittest.TestCase):
    def test_default_is_all_platforms(self):
        self.assertEqual(select_platforms(None), PLATFORMS)

    def test_case_insensitive_selection(self):
        self.assertEqual(list(select_platforms(["github"])), ["GitHub"])

    def test_unknown_platform_raises(self):
        with self.assertRaises(ValueError):
            select_platforms(["nope"])


class TestScanUsername(unittest.TestCase):
    def test_reports_found_not_found_and_unknown(self):
        statuses = {
            "https://github.com/alice": 200,
            "https://gitlab.com/alice": 404,
            "https://www.reddit.com/user/alice": 429,
            "https://medium.com/@alice": None,
        }
        results = scan_username("alice", fetch=fake_fetch_factory(statuses))
        by_name = {item.platform: item for item in results}

        self.assertEqual(len(results), len(PLATFORMS))
        self.assertEqual(by_name["GitHub"].status, FOUND)
        self.assertEqual(by_name["GitLab"].status, NOT_FOUND)
        self.assertEqual(by_name["Reddit"].status, UNKNOWN)
        self.assertEqual(by_name["Reddit"].detail, "HTTP 429")
        self.assertEqual(by_name["Medium"].status, UNKNOWN)
        self.assertEqual(by_name["Medium"].detail, "timed out")

    def test_platform_filter(self):
        results = scan_username(
            "alice", platforms=["GitHub"], fetch=fake_fetch_factory({})
        )
        self.assertEqual([item.platform for item in results], ["GitHub"])

    def test_delay_between_requests_only(self):
        pauses = []
        scan_username(
            "alice",
            platforms=["GitHub", "GitLab", "DEV"],
            fetch=fake_fetch_factory({}),
            delay=0.5,
            sleep=pauses.append,
        )
        self.assertEqual(pauses, [0.5, 0.5])

    def test_invalid_username_makes_no_requests(self):
        calls = []

        def fetch(url):
            calls.append(url)
            return HttpResult(url, 200)

        with self.assertRaises(InvalidUsernameError):
            scan_username("bad name", fetch=fetch)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()