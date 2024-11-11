import re
from game.catalog import Catalog, ItemInformation


class MultilineCatalog(Catalog):
    def only_category(self, category):
        return MultilineCatalog(self.description, { title: self[title] for title in self if self[title].category == category })

    def entry_start(self, line):
        return re.match(r"(?P<title>^[-’A-Z ]+?)\s*\((?P<practice>[A-Z ]+)\)$", line)

    def add_entry(self, lines):
        title = self.entry_start(lines[0])[1]
        self[title] = MultilineInformation(
            title,
            self.entry_start(lines[0])["practice"],
            "\n".join(lines.strip()[1:]),
        )


class MultilineInformation(ItemInformation):
    def __init__(self, title, category, description):
        self.title = title
        self.category = category
        self.description = description

    def __str__(self):
        return f"{self.title} ({self.category})\n{self.description}"
