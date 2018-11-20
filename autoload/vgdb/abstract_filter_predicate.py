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
        return result

    @property
    @abstractmethod
    def excluded_lines(self):
        pass
