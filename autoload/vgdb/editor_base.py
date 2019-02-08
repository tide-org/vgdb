from abc import ABC, abstractmethod

class editor_base(ABC):

    @staticmethod
    @abstractmethod
    def set_dictionary_value(self, parent_keys, value):
        raise NotImplementedError('set_dictionary_value() must be implemented')

    @abstractmethod
    def set_editor_dictionary(self, config_dictionary):
        raise NotImplementedError('set_editor_dictionary_defaults() must be implemented')

    @abstractmethod
    def get_config_location(self):
        raise NotImplementedError('get_config_location() must be implemented')
