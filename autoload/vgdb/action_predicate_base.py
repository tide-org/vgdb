from abc import ABC, abstractmethod
import re
import vim
import sys

class action_predicate_base(ABC):

    def __init__(self, action_dict):
        self.action_dict = action_dict

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError('run() must be implemented')
