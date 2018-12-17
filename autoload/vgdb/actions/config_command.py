import sys
sys.path.append("..")

from action_predicate_base import action_predicate_base

class config_command(action_predicate_base):

    def run(self):
        print("run stuff goes here")
