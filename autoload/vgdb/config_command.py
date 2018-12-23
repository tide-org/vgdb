import vim
from singleton import singleton
from config import Config

@singleton
class ConfigCommand(object):

    variable_dictionary = {}
    cmd_hnd = None

    def __init__(self):
        pass

    def set_command_handler(self, command_handler):
        self.cmd_hnd = command_handler

    def run_config_command(self, command):
        if self.is_command_in_config(command):
            commands_list = Config().get()["commands"][command]["steps"]
            for command_item in commands_list:
                if command_item["action"].lower() == 'command_with_match':
                    command_item_command = command_item["command"]
                    match = command_item["match"]
                    match_result = self.cmd_hnd.run_command_get_match(command_item_command, match)
                    try_set_var = command_item.get("try_set", None)
                    if try_set_var and match:
                        self.set_variable_for_command(try_set_var, match_result)

    def set_variable_for_command(self, variable_name, variable_value):
        variables_dict = Config().get()["variables"]
        if self.is_variable_in_config(variable_name) and variable_value:
            Config().get()["variables"][variable_name] = variable_value

    def is_variable_in_config(self, variable_name):
        variable_exists = Config().get()["variables"].get(variable_name, None)
        return variable_exists != None

    def is_command_in_config(self, command):
        commands_dict = Config().get()["commands"].get(command, None)
        return commands_dict != None
