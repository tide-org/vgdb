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
                    print("match:" + match)
                    match_result = self.cmd_hnd.run_command_get_match(command_item_command, match)
                    print("match_result:" + match_result)
                    try_set_var = command_item.get("try_set", None)
                    if try_set_var and match:
                        print("we're here")
                        self.set_variable_for_command(try_set_var, match_result)

    def set_variable_for_command(self, variable_name, variable_value):
        variables_dict = Config().get()["variables"]
        if self.is_variable_in_config(variable_name):
            print("one...")
            variable_type = variables_dict[variable_name].get("type", None)
            print("var type: " + str(variable_type) + " var val: " + str(variable_value))
            if variable_type and variable_value:
                print("two...")
                self.set_variable_for_type(variable_name, variable_value, variable_type)

    def set_variable_for_type(self, variable_name, variable_value, variable_type):
        print("and here")
        if variable_type.lower().__contains__('python'):
            self.variable_dictionary[variable_name] = variable_value
        if variable_type.lower().__contains__('vim'):
            vim.command("let g:vg_" + variable_name + " = " + str(variable_value))

    def is_variable_in_config(self, variable_name):
        variable_exists = Config().get()["variables"].get(variable_name, None)
        return variable_exists != None

    def is_command_in_config(self, command):
        commands_dict = Config().get()["commands"].get(command, None)
        return commands_dict != None
