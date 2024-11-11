from unittest import TestCase
from game.multiline_catalog import MultilineCatalog, MultilineInformation
from game.section import Section

class MultilineCatalogTest(TestCase):
    def test_only_category(self):
        catalog = MultilineCatalog("description", {
            "VALID": MultilineInformation("valid", "valid", "valid"),
            "INVALID": MultilineInformation("invalid", "invalid", "invalid"),
        }).only_category("valid")
        self.assertIn("VALID", catalog)
        self.assertNotIn("INVALID", catalog)

    def test_entry_start(self):
        practices = MultilineCatalog("", [])
        self.assertTrue(practices.entry_start("SOMETHING (WITH SPACES)"))
        self.assertTrue(practices.entry_start("SPECIAL’S (PRACTICE)"))

    def test_add_entry(self):
        practices = MultilineCatalog("", [])
        practices.add_entry(Section([
            "TITLE (PRACTICE)",
            "description",
        ]))
        practice = practices["TITLE"]
        self.assertEqual("TITLE", practice.title)
        self.assertEqual("PRACTICE", practice.category)
        self.assertEqual("description", practice.description)


class MultilineInformationTest(TestCase):
    def test_str(self):
        self.assertEqual(
            "Title (Category)\ndescription",
            str(MultilineInformation("Title", "Category", "description")),
        )
