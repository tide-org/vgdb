from abc import ABC, abstractmethod

class abstract_filter_predicate(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def process_lines(self, lines):
        result = []
        for line in lines:
            line = self.check_for_excluded(line)
            if line:
                result.append(self.run_formatters(line))
        return result

    def check_for_excluded(self, line):
        for excluded_line in self.excluded_lines:
            if excluded_line in line:
                return
        return line

    def run_formatters(self, line):
        for formatter in self.line_formatters:
            line = formatter(line)
        return line

    @property
    @abstractmethod
    def excluded_lines(self):
        return []

    @abstractmethod
    def line_formatters(self, formatters):
        return []
