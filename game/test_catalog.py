from unittest import TestCase, main
from game.information import Section, Definitions, Catalog, GameInformation
from game.multiline_catalog import MultilineCatalog, MultilineInformation
from game.catalog import ItemInformation


class CatalogTest(TestCase):
    def test_description_text(self):
        self.assertEqual("Two\nlines", Catalog.description_text(Section(["Two", "lines"])))
        self.assertEqual("Section List Page", Catalog.description_text(Section(["SECTION", "", "----", "Section List Page", "---"])))
        self.assertEqual("description", Catalog.description_text(Section(["SECTION TITLE", "description"])))


class ItemInformationTest(TestCase):
    def test_str(self):
        self.assertEqual("Title\nfoo", str(ItemInformation("Title", "foo")))
