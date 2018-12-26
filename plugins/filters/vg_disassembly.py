from filter_predicate_base import filter_predicate_base

class vg_disassembly(filter_predicate_base):

    @property
    def excluded_lines(self):
        return [
            'Dump of assembler code',
            'End of assembler dump.'
        ]

    @property
    def line_formatters(self):
        return [
            self.remove_first_three_chars,
            self.trim_trailing_whitespace,
            self.add_left_margin
        ]

    def add_left_margin(self, line):
        return "    " + line

    def remove_first_three_chars(self, line):
        return line[3:]

    def trim_trailing_whitespace(self, line):
        return line.rstrip()

    @property
    def line_matchers_pre(self):
        return [
            {
                'variable_name': 'no_program_counter',
                'regex': 'No function contains program counter for selected frame',
                'type': 'bool',
                'description': 'specifies whether the program counter can be determined'
            },
        ]
