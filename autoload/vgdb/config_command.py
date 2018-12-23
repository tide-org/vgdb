import vim
from singleton import singleton
from config import Config
import os
import importlib
import sys

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
                command_action = command_item["action"].lower()
                if command_action == 'command_with_match':
                    command_item_command = command_item["command"]
                    match = command_item["match"]
                    match_result = self.cmd_hnd.run_command_get_match(command_item_command, match)
                    try_set_var = command_item.get("try_set", None)
                    if try_set_var and match:
                        self.set_variable_for_command(try_set_var, match_result)
                elif command_action == 'python_function':
                    python_function = self.get_python_function(command_item)

    def get_python_function(self, command_item):
        function_file = command_item["function_file"]
        function_name = command_item["function_name"]
        input_args = command_item.get("input_args", {})
        set_on_return = command_item.get("set_on_return", None)
        script_path = os.path.dirname(os.path.realpath(__file__))
        functions_path = os.path.join(script_path, "./functions")
        function_file_path = os.path.join(functions_path, function_file)
        print("function path: " + function_file_path + " function name: " + function_name)
        function_module_name = "functions." + function_file.replace(".py", "")
        function_module = importlib.import_module(function_module_name)
        function = getattr(sys.modules[function_module_name], function_name)
        interpolated_input_args = {}
        for key, value in input_args.items():
            interpolated_input_args[key] = Config().get()["variables"][value]
        print("ia: " + str(input_args))
        print("iia: " + str(interpolated_input_args))
        function_result = function(**interpolated_input_args)
        print("fr: " + str(function_result))
        if set_on_return:
            Config().get()["variables"][set_on_return] = function_result


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
