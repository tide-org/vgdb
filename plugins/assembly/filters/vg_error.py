from filter_predicate_base import filter_predicate_base

class vg_error(filter_predicate_base):

    @property
    def line_formatters(self):
        return [
            self.keep_return_values,
            self.remove_unescaped_characters
        ]

    def keep_return_values(self, line):
        if line.startswith('&"'):
            return line.lstrip('&"')[:-4]

    def remove_unescaped_characters(self, line):
        return line.replace("\r", "").replace("'", "''").replace("\\t", "    ")

    @property
    def pre_processors(self):
        return [self.split_to_array_by_newline_char]

    @property
    def line_matchers_post(self):
        return [
            {
                'variable_name': 'no_program_counter',
                'regex': 'No function contains program counter for selected frame',
                'type': 'bool',
                'description': 'specifies whether the program counter can be determined'
            },
        ]

    def split_to_array_by_newline_char(self, line):
        result = line.split("\n")
        return result
