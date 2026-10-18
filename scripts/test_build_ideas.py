import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_ideas


class TestIdeas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = build_ideas.load_catalog()

    def test_initial_catalog(self):
        self.assertGreaterEqual(self.data["count"], 11)
        self.assertEqual(self.data["schema_version"], 1)

    def test_unique_ids(self):
        rows = self.data["ideas"]
        self.assertEqual(len(rows), len({x["id"] for x in rows}))

    def test_all_ideas_documented(self):
        for row in self.data["ideas"]:
            self.assertIn("## Eredeti felvetés", row["markdown"])
            self.assertIn("## Megoldási változatok", row["markdown"])
            self.assertIn("> ", row["markdown"])

    def test_initial_rice_not_fabricated(self):
        for row in self.data["ideas"]:
            self.assertIsNone(row["rice_score"])

    def test_reject_duplicate_frontmatter_key(self):
        path = build_ideas.IDEAS / "IDEA-001-qr-kioszk.md"
        original = path.read_text(encoding="utf-8")
        altered = original.replace('status: "ötlet"', 'status: "ötlet"\nstatus: "elemzett"')
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / path.name
            target.write_text(altered, encoding="utf-8")
            with self.assertRaises(build_ideas.CatalogError):
                build_ideas.read_idea(target)


if __name__ == "__main__":
    unittest.main()
