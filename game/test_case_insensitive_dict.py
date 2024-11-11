from unittest import TestCase
from game.case_insensitive_dict import CaseInsensitiveDict


class CaseInsensitiveDictTest(TestCase):
    def setUp(self):
        self.dictionary = CaseInsensitiveDict({ "Something": "Interesting" })

    def test_uppercased_lookup(self):
        self.assertEqual(self.dictionary["SOMETHING"], "Interesting")

    def test_lowercased_lookup(self):
        self.assertEqual(self.dictionary["something"], "Interesting")

    def test_contains(self):
        self.assertIn("something", self.dictionary)

    def test_assignment(self):
        self.dictionary["new"] = "Something new"
        self.assertEqual("Something new", self.dictionary["NEW"])

    def test_init_keys(self):
        self.assertEqual(["Something"], list(self.dictionary.keys()))

    def test_set_keys(self):
        self.dictionary["new"] = "value"
        self.assertIn("new", self.dictionary.keys())
