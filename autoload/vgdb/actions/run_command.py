from action_predicate_base import action_predicate_base
from config_command import ConfigCommand
from command_handler import CommandHandler

class run_command(action_predicate_base):

    def run(self, command_item, buffer_name=''):
        config_command_buffer_name = command_item.get("buffer_name", '')
        if config_command_buffer_name != '':
            buffer_name = config_command_buffer_name
        return CommandHandler().run_command(command_item['command'], buffer_name)

