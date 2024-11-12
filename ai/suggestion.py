import logging
from game.catalog import ItemInformation


class SuggestionClient():
    def __init__(self, game, llm_client):
        self.game = game
        self.llm_client = llm_client

    def suggest(self, category, prompt):
        catalog = self.game[category]
        prediction = self.prediction(category, prompt)
        if prediction in catalog:
            return catalog[prediction]
        else:
            return ItemInformation("AI Hallucination", f"ChatGPT hallucinated and suggested {prediction}")

    def prediction(self, category, prompt):
        return self.completion(
            self.messages(category, prompt)
        ).choices[0].message.content

    def completion(self, messages):
        return self.llm_client.chat.completions.create(
            messages=messages,
            model="gpt-4-turbo",
        )

    def messages(self, category, prompt):
        return [
            {
                "role": "system",
                "content": "\n".join([
                    f"You are an Invisible Sun GM, tasked with selecting relevant game materials. You have been asked to select from {category} among the following:",
                    "",
                    *[f"{item.title}\n{item.description}\n" for item in self.game[category].values()],
                    "",
                    "Your response should be the title of the item you selected.",
                ]),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]


class LoggedSuggestionClient(SuggestionClient):
    def prediction(self, category, prompt):
        prediction = super().prediction(category, prompt)
        logging.debug(f"Prediction {prediction}")
        return prediction

    def completion(self, messages):
        logging.debug(f"Messages {messages}")
        completion = super().completion(messages)
        logging.debug(f"Completion {completion}")
        return completion
