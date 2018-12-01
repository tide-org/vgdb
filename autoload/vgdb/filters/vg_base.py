import sys
sys.path.append("..")

from filter_predicate_base import filter_predicate_base

class vg_base(filter_predicate_base):

    @property
    def line_formatters(self):
        return [
                self.keep_return_values,
                self.remove_unescaped_characters
            ]

    @property
    def pre_processors(self):
        return [ self.split_to_array_by_newline_char ]

    def keep_return_values(self, line):
        if line.startswith('~"'):
            return line.lstrip('~"')[:-4]

    def remove_unescaped_characters(self, line):
        return line.replace("\r","").replace("'", "''").replace("\\t", "    ")

    def split_to_array_by_newline_char(self, line):
        result = line.split("\n")
        return result
