from action_predicate_base import action_predicate_base
from config_command import ConfigCommand

class run_config_command(action_predicate_base):

    def run(self, command_item, buffer_name=''):
        ConfigCommand().run_config_command(command_item['name'], buffer_name)
