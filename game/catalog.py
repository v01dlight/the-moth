import re
import itertools
from game.case_insensitive_dict import CaseInsensitiveDict
from game.section import Section


class Catalog(CaseInsensitiveDict):
    @classmethod
    def build(cls, section, description=None):
        catalog = cls(description or cls.description_text(section))
        entries = []
        for line in section:
            if catalog.entry_start(line):
                entries.append(Section())
            if entries:
                entries[-1].append(line)

        for entry in entries:
            catalog.add_entry(entry)

        return catalog

    @classmethod
    def description_text(cls, section):
        if re.match(r"^[A-Z ]+$", section[0]):
            section = Section(section[1:])
        description_lines = itertools.takewhile(lambda line: line not in ["", "---"], section.strip())
        return "\n".join([line for line in description_lines if line != "----"])

    def __init__(self, description, entries=None):
        self.description = description
        super().__init__(entries or {})


class ItemInformation():
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return f"{self.title}\n{self.description}"

    def __eq__(self, o):
        return self.title == o.title and self.description == o.description
