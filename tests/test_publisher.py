import json
from pathlib import Path
import tempfile
import unittest

from reference.publisher import publish


ROOT = Path(__file__).resolve().parents[1]


class PublisherTests(unittest.TestCase):
    def test_publishes_valid_profile_at_well_known_path(self):
        profile = ROOT / "examples" / "public-information-site.json"
        with tempfile.TemporaryDirectory() as directory:
            output = publish(profile, Path(directory))
            self.assertEqual(output, Path(directory) / ".well-known" / "asp")
            self.assertEqual(json.loads(output.read_text())["domain"], "example.org")


if __name__ == "__main__":
    unittest.main()
