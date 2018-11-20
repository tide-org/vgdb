from abc import ABC, abstractmethod

class abstract_filter_predicate(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def process_lines(self, lines):
        result = []
        for line in lines:
            line_ok = True
            for excluded_line in self.excluded_lines:
                if excluded_line in line:
                    line_ok = False
            if line_ok:
                result.append(line)
        result = self.run_formatters(result)
        return result

    def run_formatters(self, lines):
        result = []
        for line in lines:
            for formatter in self.line_formatters:
                line = formatter(line)
            result.append(line)
        return result

    @property
    @abstractmethod
    def excluded_lines(self):
        return []

    @abstractmethod
    def line_formatters(self, formatters):
        return []
