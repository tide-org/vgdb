from abc import ABC, abstractmethod
import re
import vim
import sys

class filter_predicate_base(ABC):

    def __init__(self, lines):
        lines = self.__run_pre_processors(lines)
        self.__get_set_matches(lines)
        lines = self.__process_lines(lines)
        self.processed_lines = self.__run_post_processors(lines)

    def __process_lines(self, lines):
        result = []
        for line in lines:
            if line:
                line = self.__check_for_excluded(line)
                if line:
                    result.append(line)
        result = self.__run_formatters(result)
        return result

    def __check_for_excluded(self, line):
        for excluded_line in self.excluded_lines:
            if excluded_line in line:
                return
        return line

    def __run_formatters(self, lines):
        result = []
        for formatter in self.line_formatters:
            single_formatter = []
            for line in lines:
                if line:
                    tmp_line = formatter(line)
                    if isinstance(tmp_line, list):
                        single_formatter.extend(tmp_line)
                    else:
                        single_formatter.append(tmp_line)
            lines = single_formatter
        return lines

    def __get_set_matches(self, lines):
        for matcher in self.line_matchers:
            if matcher['type'].lower() == 'array':
                self.__iterate_lines_for_array_match(lines, matcher)

    def __iterate_lines_for_array_match(self, lines, matcher):
        matches_list = []
        regex = re.compile(matcher['regex'])
        for line in lines:
            if line:
                match = re.search(matcher['regex'], line)
                if match:
                    matches_list.append(match.group(1))
        vim.command("let g:" + matcher['vg_name'] + " = %s" % matches_list)

    def __run_pre_processors(self, lines):
        for processor in self.pre_processors:
            print("pre running: " + processor.__name__)
            lines = processor(lines)
        return lines

    def __run_post_processors(self, lines):
        for processor in self.post_processors:
            print("post running: " + processor.__name__)
            lines = processor(lines)
        return lines

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

    @property
    def pre_processors(self):
        return []

    @property
    def post_processors(self):
        return []
