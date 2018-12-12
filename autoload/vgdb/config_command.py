import vim
from singleton import singleton

@singleton
class ConfigCommand(object):

    variable_dictionary = {}
    config_dictionary = {}
    cmd_hnd = None

    def __init__(self, config_dictionary):
        self.config_dictionary = config_dictionary

    def set_command_handler(self, command_handler):
       self.cmd_hnd = command_handler

    def run_config_command(self, command):
        if self.is_command_in_config(command):
            commands_list = self.config_dictionary["commands"][command]["steps"]
            for command_item in commands_list:
                if command_item["type"].lower() == 'command_with_match':
                  command_item_command = command_item["command"]
                  match = command_item["match"]
                  match_result = self.cmd_hnd.run_command_get_match(command_item_command, match)
                  try_set_var = command_item.get("try_set", None)
                  if try_set_var != None:
                      if match != None:
                          self.set_variable_for_command(try_set_var, match_result)

    def set_variable_for_command(self, variable_name, variable_value):
        variables_dict = self.config_dictionary["variables"]
        if self.is_variable_in_config(variable_name):
            variable_type = variables_dict[variable_name].get("type", None)
            if variable_type != None and variable_value != None:
                self.set_variable_for_type(variable_name, variable_value, variable_type)

    def set_variable_for_type(self, variable_name, variable_value, variable_type):
        if variable_type.lower().__contains__('python'):
            self.variable_dictionary[variable_name] = variable_value
        if variable_type.lower().__contains__('vim'):
            vim.command("let g:vg_" + variable_name + " = " + str(variable_value))

    def is_variable_in_config(self, variable_name):
        vars_dict = self.config_dictionary["variables"]
        variable_exists = vars_dict.get(variable_name, None)
        if variable_exists != None:
            return True
        return False

    def is_command_in_config(self, command):
        config_commands = self.config_dictionary["commands"]
        commands_dict = config_commands.get(command, None)
        if commands_dict != None:
            return True
        return False

