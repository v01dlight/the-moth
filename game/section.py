import re
import itertools


class Section(list):
    def at_paragraph_break(self):
        return self and self[-1] == ""

    def nonempty_lines(self):
        return [
            line
            for line
            in self
            if line != ""
        ]

    def should_include(self, line):
        return (line != "" and not re.search(r"^[A-Z, ]+$", line)) or not self.at_paragraph_break()

    def strip(self):
        is_empty_line = lambda line: line == ""
        strip_front = lambda lines: list(itertools.dropwhile(is_empty_line, lines))
        front_stripped = strip_front(self)
        rear_stripped = reversed(strip_front(reversed(front_stripped)))
        return Section(rear_stripped)
