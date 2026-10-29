import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import promote_ideas


class TestIdeaPromotion(unittest.TestCase):
    def test_allowlist_only_idea_markdown(self):
        accepted = [
            "docs/ideas/IDEA-022-anonim-nyitooldal-telepitesi-utmutato.md",
            "docs/ideas/IDEA-009-guest.md",
        ]
        rejected = [
            "docs/ideas/README.md",
            "docs/ideas/catalog.json",
            "docs/implementation-plan/06-react-pwa-es-ux.md",
            "docs/ideas/IDEA-022.md",
            "docs/ideas/IDEA-022-../secret.md",
            ".github/workflows/dev-status.yml",
        ]
        for path in accepted:
            self.assertIsNotNone(promote_ideas.IDEA_PATH.fullmatch(path))
        for path in rejected:
            self.assertIsNone(promote_ideas.IDEA_PATH.fullmatch(path))

    def test_status_parser(self):
        raw = (b"A\x00docs/ideas/IDEA-022-new.md\x00"
               b"M\x00docs/ideas/IDEA-009-guest.md\x00")
        self.assertEqual(promote_ideas.parse_name_status(raw), [
            ("A", "docs/ideas/IDEA-022-new.md"),
            ("M", "docs/ideas/IDEA-009-guest.md"),
        ])
        with self.assertRaises(ValueError):
            promote_ideas.parse_name_status(b"A\x00broken")

    def test_existing_catalog_is_valid(self):
        result = promote_ideas.validate_full_catalog({})
        self.assertGreaterEqual(result, 22)

    def test_no_arbitrary_files_in_proposal(self):
        with mock.patch.object(
                promote_ideas, "git",
                return_value=(b"M\x00docs/ideas/README.md\x00"
                              b"M\x00docs/implementation-plan/06-react-pwa-es-ux.md\x00"
                              b"A\x00docs/ideas/IDEA-023-next.md\x00")):
            self.assertEqual(promote_ideas.proposed_files("base", "head"),
                             ["docs/ideas/IDEA-023-next.md"])


if __name__ == "__main__":
    unittest.main()
