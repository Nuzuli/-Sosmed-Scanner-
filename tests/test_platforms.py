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


# Platforms added after the initial six. Every URL pattern here was
# verified live: an existing profile returned 200 and a nonexistent
# username returned 404.
NEW_PLATFORMS = {
    "YouTube": "https://www.youtube.com/@alice",
    "Mastodon": "https://mastodon.social/@alice",
    "Tumblr": "https://alice.tumblr.com",
    "Flickr": "https://www.flickr.com/photos/alice",
    "SoundCloud": "https://soundcloud.com/alice",
    "Dribbble": "https://dribbble.com/alice",
    "Linktree": "https://linktr.ee/alice",
    "Gravatar": "https://gravatar.com/alice",
    "Codeberg": "https://codeberg.org/alice",
    "SourceHut": "https://sr.ht/~alice",
    "Keybase": "https://keybase.io/alice",
    "Chess.com": "https://www.chess.com/member/alice",
    "Docker Hub": "https://hub.docker.com/u/alice",
    "Hugging Face": "https://huggingface.co/alice",
}


class TestNewPlatforms(unittest.TestCase):
    def test_all_new_platforms_are_registered(self):
        for name in NEW_PLATFORMS:
            self.assertIn(name, PLATFORMS)
        self.assertEqual(len(PLATFORMS), 20)

    def test_new_platform_profile_urls(self):
        for name, expected_url in NEW_PLATFORMS.items():
            with self.subTest(platform=name):
                requested = []

                def fetch(url):
                    requested.append(url)
                    return HttpResult(url=url, status=200)

                results = scan_username(
                    "alice", platforms=[name], fetch=fetch
                )

                self.assertEqual(requested, [expected_url])
                self.assertEqual(results[0].platform, name)
                self.assertEqual(results[0].status, FOUND)


if __name__ == "__main__":
    unittest.main()