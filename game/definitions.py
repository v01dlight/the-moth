import re
from game.catalog import Catalog, ItemInformation


class Definitions(Catalog):
    def entry_start(self, line):
        return re.search(r":", line)

    def add_entry(self, lines):
        line = lines[0]
        (key, value) = line.split(":", 1)
        key = re.sub(r"\s*\([A-Z]+\)$", "", key)
        self[key] = ItemInformation(key, value.strip())
