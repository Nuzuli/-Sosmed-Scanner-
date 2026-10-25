import unittest

from sosmed_scanner.network import HttpResult
from sosmed_scanner.scanner import FOUND, PLATFORMS, scan_username


class TestPyPIPlatform(unittest.TestCase):
    def test_pypi_is_registered(self):
        self.assertIn("PyPI", PLATFORMS)

    def test_pypi_profile_url_and_result(self):
        requested = []

        def fetch(url):
            requested.append(url)
            return HttpResult(url=url, status=200)

        results = scan_username("alice", platforms=["pypi"], fetch=fetch)

        self.assertEqual(requested, ["https://pypi.org/user/alice/"])
        self.assertEqual(results[0].platform, "PyPI")
        self.assertEqual(results[0].status, FOUND)


if __name__ == "__main__":
    unittest.main()