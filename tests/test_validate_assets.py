from pathlib import Path
import unittest

from tools.validate_assets import validate_repository


ROOT = Path(__file__).resolve().parents[1]


class RepositoryValidationTests(unittest.TestCase):
    def test_repository_assets_validate_cleanly(self):
        self.assertEqual(validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
