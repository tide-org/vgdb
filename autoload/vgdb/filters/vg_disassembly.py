import sys
sys.path.append("..")

from filter_predicate_base import filter_predicate_base

class vg_disassembly(filter_predicate_base):

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
