from unittest import TestCase
from unittest.mock import Mock, MagicMock
from ai.suggestion import SuggestionClient
from game.information import GameInformation
from game.catalog import Catalog, ItemInformation


class SuggestionTest(TestCase):
    def setUp(self):
        self.llm_client = Mock()
        self.completion = MagicMock()
        self.llm_client.chat.completions.create.return_value = self.completion
        self.item = ItemInformation("B", "C")

        self.client = SuggestionClient(GameInformation({
            "A": Catalog("A", {
                "B": self.item,
            }),
        }), self.llm_client)

    def test_suggest(self):
        self.mock_prediction("B")
        self.assertEqual(self.item, self.client.suggest("A", "a test message"))

    def test_hallucination(self):
        self.mock_prediction("C")
        self.assertRegex(
            self.client.suggest("A", "a test message").description,
            r"C",
        )

    def mock_prediction(self, prediction):
        self.completion.choices[0].message.content = prediction
