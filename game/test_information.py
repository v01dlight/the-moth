from unittest import TestCase
import enum
from game.information import GameInformation
from game.multiline_catalog import MultilineCatalog, MultilineInformation
from game.catalog import Catalog, ItemInformation


class GameInformationTest(TestCase):
    def test_categories(self):
        game = GameInformation({ "SOMETHING": {} })
        self.assertEqual(
            "something",
            game.categories().SOMETHING.value,
        )

    def test_lookup(self):
        item = ItemInformation("INTERESTING", "FOUND")
        game = GameInformation({ "SOMETHING": { "INTERESTING": item } })
        self.assertEqual(
            item,
            game.lookup("SOMETHING", "INTERESTING"),
        )
        self.assertIsNone(game.lookup("SOMETHING", "MISSING"))

    def test_random(self):
        item = ItemInformation("INTERESTING", "FOUND")
        game = GameInformation({ "SOMETHING": { "INTERESTING": item } })
        self.assertEqual(item, game.random("SOMETHING"))

    def test_separate_categories(self):
        separated = GameInformation.separate_categories(MultilineCatalog("", {
            "A": MultilineInformation("A", "A", "A"),
            "B": MultilineInformation("B", "B", "B"),
            "C": MultilineInformation("C", "C", "C"),
        }), ["A", "B", "C"])
        self.assertIn("A", separated["A"])
        self.assertIn("B", separated["B"])
        self.assertIn("C", separated["C"])

    def test_case_insensitive_terms(self):
        item = ItemInformation("interesting", "Found")
        game = GameInformation({ "something": Catalog("", { "interesting": item }) })
        self.assertEqual(game["SOMETHING"]["INTERESTING"], item)
        self.assertEqual(game["something"]["interesting"], item)
        self.assertIn("interesting", game["something"])
