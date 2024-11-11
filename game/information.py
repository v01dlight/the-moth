import re
import itertools
import enum
from game.case_insensitive_dict import CaseInsensitiveDict
from game.catalog import Catalog, ItemInformation
from game.multiline_catalog import MultilineCatalog
from game.section import Section
from game.definitions import Definitions
import random


class GameInformation(CaseInsensitiveDict):
    @classmethod
    def parse(cls, filename):
        sections = cls.parse_sections(filename)
        return cls.build_from_sections(sections)

    @classmethod
    def build_from_sections(cls, sections):
        info = {
            "GAME": Catalog("General Game Information", {
                "TITLE": ItemInformation("TITLE", sections[0][0]),
                "PREAMBLE": ItemInformation("PREAMBLE", "\n".join(sections[1])),
                "LICENSE": ItemInformation("LICENSE", "\n".join(sections[2])),
            }),
            "GLOSSARY": Definitions.build(sections[3], "General Definitions"),
            "CANTRIPS": Definitions.build(sections[5]),
            "CHARMS": Definitions.build(sections[6]),
            "SIGNS": Definitions.build(sections[7]),
            "HEXES": Definitions.build(sections[8]),
            "MONOGRAPHS": "\n".join(sections[9]),
            "RITUALS": MultilineCatalog.build(sections[11]),
            "INCANTATIONS": MultilineCatalog.build(sections[13] + sections[14] + sections[15] + sections[16] + sections[17], "Incantations"),
            "OBJECTS OF POWER": MultilineCatalog.build(sections[19], "Objects of Power"),
            "SPELLS": MultilineCatalog.build(
                sections[21] + sections[22] + sections[23] +
                ["FERMATA (SPELL)"] + sections[24][1:] +
                ["HUNT THE LOST (SPELL)"] + sections[25][1:] +
                sections[26][1:],
                "Spells",
            ),
            "ORDER": Catalog("Order Special Rules", {
                order: ItemInformation(order, "\n".join(sections[section_index].strip()))
                for (order, section_index) in [("MAKER", 65),
                                               ("WEAVER", 66),
                                               ("GOETIC", 67)]
            }),
            "HEART": Catalog("Heart", {
                heart: ItemInformation(heart, "\n".join(sections[section_id][1:]))
                for (heart, section_id) in [("GALANT", 32),
                                            ("STOIC", 33),
                                            ("EMPATH", 34),
                                            ("ARDENT", 35)]
            }),
            "FORTE ABILITY": MultilineCatalog.build(sections[36]),
            "SOUL": MultilineCatalog.build(sections[38], "Soul"),
            "CHARACTER ARCS": MultilineCatalog.build(sections[40], "Character Arcs"),
            "DISTRICTS OF SATYRINE": Catalog("Districts of Satyrine", {
                section[0]: ItemInformation(
                    section[0],
                    "\n".join(section[1:]),
                )
                for section in sections[42:59]
            }),
            "CREATURES": Catalog({
                section[0]: ItemInformation(
                    section[0],
                    "\n".join(section[1:]),
                ) for section in sections[60:64]
            }),
            "CHARACTER SECRETS": MultilineCatalog.build(sections[69]),
            "HOUSE SECRETS": MultilineCatalog.build(sections[70]),
            "CHARACTER CREATION": Catalog("Character Creation", {
                section[0]: ItemInformation(
                    section[0],
                    "\n".join(section[1:]),
                ) for section in sections[71:]
            })
        }

        info.update(cls.separate_categories(
            MultilineCatalog.build(sections[10]),
            ["CONJURATIONS", "INVOCATIONS", "ENCHANTMENTS"],
        ))

        info.update(cls.separate_categories(
            MultilineCatalog.build(sections[29], "Ephemera Objects"),
            ["EPHEMERA OBJECTS"] + [f"VANCE {size} SPELL" for size in ["ALPHA", "BETA", "OMEGA"]],
        ))

        return GameInformation(info)

    @classmethod
    def separate_categories(cls, catalog: MultilineCatalog, categories):
        return {
            category: catalog.only_category(category)
            for category in categories
        }

    @classmethod
    def parse_sections(cls, filename):
        with open(filename) as file:
            sections = [Section()]

            for line in file.readlines():
                line = line.strip()
                if not sections[-1].should_include(line):
                    sections.append(Section())
                sections[-1].append(line)
            return [
                section
                for section
                in sections
                if len(section.nonempty_lines()) > 0
            ]

    def categories(self):
        return enum.StrEnum("Categories", list(self.keys()))

    def lookup(self, category, item):
        if item in self[category]:
            return self[category][item]

    def random(self, category):
        return random.choice(list(self[category].values()))
