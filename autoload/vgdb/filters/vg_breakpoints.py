import sys
sys.path.append("..")

from abstract_filter_predicate import abstract_filter_predicate

class vg_breakpoints(abstract_filter_predicate):

    def __init__(self):
        pass

    def process_lines(self, lines):
        lines = super(vg_breakpoints, self).process_lines(lines)
        return lines

    @property
    def excluded_lines(self):
        return []

    @property
    def line_formatters(self):
        return []

    def line_matchers(self, matchers, vim_global):
        return []
