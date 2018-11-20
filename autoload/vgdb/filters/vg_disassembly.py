import sys
sys.path.append("..")

from abstract_filter_predicate import abstract_filter_predicate

class vg_disassembly(abstract_filter_predicate):

    def __init__(self):
        pass

    def process_lines(self, lines):
        lines = super(vg_disassembly, self).process_lines(lines)
        return lines

    @property
    def excluded_lines(self):
        return [
            'Dump of assembler code for',
            'End of assembler dump.'
        ]

    @property
    def line_formatters(self):
        return [
            self.remove_first_three_chars,
            self.trim_trailing_whitespace
        ]

    def remove_first_three_chars(self, line):
        return line[3:]

    def trim_trailing_whitespace(self, line):
        return line.rstrip()

