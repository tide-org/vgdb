from abc import ABC, abstractmethod

class action_predicate_base(ABC):

    @abstractmethod
    def run(self, command_item, buffer_name=""):
        raise NotImplementedError('run() must be implemented')
