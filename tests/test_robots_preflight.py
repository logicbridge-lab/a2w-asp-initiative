import unittest

from crawler.preflight import robots_allows


class RobotsPolicyTests(unittest.TestCase):
    def test_allow_rule_permits_matching_path(self):
        robots = "User-agent: *\nAllow: /docs/api\nDisallow: /docs\n"
        self.assertTrue(robots_allows(robots, "/docs/api"))

    def test_disallow_rule_blocks_matching_path(self):
        robots = "User-agent: *\nDisallow: /private\n"
        self.assertFalse(robots_allows(robots, "/private/data"))

    def test_empty_robots_permits_path(self):
        self.assertTrue(robots_allows("User-agent: *\n", "/public"))


if __name__ == "__main__":
    unittest.main()
