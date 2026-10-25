import unittest

import sosmed_scanner
from sosmed_scanner.network import USER_AGENT


class TestVersion(unittest.TestCase):
    def test_version_is_semantic(self):
        parts = sosmed_scanner.__version__.split(".")
        self.assertEqual(len(parts), 3)
        self.assertTrue(all(part.isdigit() for part in parts))

    def test_user_agent_contains_package_version(self):
        self.assertIn(sosmed_scanner.__version__, USER_AGENT)


if __name__ == "__main__":
    unittest.main()