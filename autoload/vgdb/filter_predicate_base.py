from abc import ABC, abstractmethod
import re
import vim

class filter_predicate_base(ABC):

    def __init__(self, lines):
        self.__get_set_matches(lines)
        self.processed_lines = self.__process_lines(lines)

    def __process_lines(self, lines):
        result = []
        for line in lines:
            line = self.__check_for_excluded(line)
            if line:
                result.append(self.__run_formatters(line))
        return result

    def __check_for_excluded(self, line):
        for excluded_line in self.excluded_lines:
            if excluded_line in line:
                return
        return line

    def __run_formatters(self, line):
        for formatter in self.line_formatters:
            line = formatter(line)
        return line

    def __get_set_matches(self, lines):
        for matcher in self.line_matchers:
            if matcher['type'].lower() == 'array':
                self.__iterate_lines_for_array_match(lines, matcher)

    def __iterate_lines_for_array_match(self, lines, matcher):
        matches_list = []
        regex = re.compile(matcher['regex'])
        for line in lines:
            match = re.search(matcher['regex'], line)
            if match:
                matches_list.append(match.group(1))
        vim.command("let g:" + matcher['vg_name'] + " = %s"% matches_list)

    # the following properties/methods are intended to be overwritten

    @property
    def excluded_lines(self):
        return []

    @property
    def line_formatters(self):
        return []

    @property
    def line_matchers(self):
        return []
