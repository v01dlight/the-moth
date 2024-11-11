from unittest import TestCase
from game.definitions import Definitions

class DefinitionsTest(TestCase):
    def test_entry_start(self):
        definitions = Definitions("", [])
        self.assertTrue(definitions.entry_start("TERM: definition"))

    def test_add_entry(self):
        definitions = Definitions("", [])
        definitions.add_entry(["TERM: definition"])
        self.assertEqual("definition", definitions["TERM"].description)
