from config import Config
from action_predicate_base import action_predicate_base
from command_handler import CommandHandler

class run_command_string(action_predicate_base):

    def run(self, command_item, buffer_name=''):
        variable_name = command_item['variable_name']
        variable_value = Config().get()["variables"][variable_name]
        result = CommandHandler().run_command(variable_value, buffer_name)
        return result
