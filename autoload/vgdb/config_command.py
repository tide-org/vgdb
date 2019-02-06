from singleton import singleton
from config import Config
import action as Action
from config_command_item import ConfigCommandItem

@singleton
class ConfigCommand(object):

    metadata_dict_keys = [ 'when' ]

    def run_config_command(self, cci):
        for command_action in cci.command_action_list:
            if command_action.is_ok_to_run():
                self.__initialise_buffer(cci.buffer_name)
                action_args = command_action.get_action_args()
                lines = Action.run_action(command_action.type, action_args)
                self.__set_buffer_lines(lines, cci, command_action)

    def __initialise_buffer(self, buffer_name):
        if buffer_name not in Config().get()["internal"]["buffer_caches"]:
            Config().get()["internal"]["buffer_caches"][buffer_name] = []

    def __set_buffer_lines(self, lines, cci, command_action):
        if lines:
            if not cci.buffer_name:
                lines.insert(0, "no buffer name. command_action_name: " + command_action.type + " command_action: " + str(command_action) )
                internal_buffer_name = 'default'
            else:
                internal_buffer_name = cci.buffer_name
            Config().get()["internal"]["buffer_caches"][internal_buffer_name] = lines
