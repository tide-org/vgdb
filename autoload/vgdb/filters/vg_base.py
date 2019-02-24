from filter_predicate_base import filter_predicate_base

class vg_base(filter_predicate_base):

    @property
    def pre_processors(self):
        return [self.split_to_array_by_newline_char]

    def split_to_array_by_newline_char(self, line):
        return line.split("\n")
