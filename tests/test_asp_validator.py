import json
from pathlib import Path
import unittest

from reference.asp_validator import validate_profile


ROOT = Path(__file__).resolve().parents[1]


class AspValidatorTests(unittest.TestCase):
    def test_accepts_canonical_example(self):
        profile = json.loads((ROOT / "examples" / "public-information-site.json").read_text())
        self.assertEqual(validate_profile(profile), [])

    def test_rejects_bad_domain(self):
        profile = json.loads((ROOT / "examples" / "public-information-site.json").read_text())
        profile["domain"] = "not a domain"
        self.assertIn("domain must be a lowercase hostname", validate_profile(profile))


if __name__ == "__main__":
    unittest.main()
