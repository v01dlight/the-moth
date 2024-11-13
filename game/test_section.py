from unittest import TestCase
from game.section import Section


class SectionTest(TestCase):
    def test_should_include(self):
        self.assertTrue(Section(['anything']).should_include("ALL CAPS"))
