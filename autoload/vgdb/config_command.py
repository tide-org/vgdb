import vim
from singleton import singleton
from config import Config
import os
import importlib
import sys
import plugin_helpers as plugins


@singleton
class ConfigCommand(object):

    variable_dictionary = {}
    cmd_hnd = None
    valid_actions = ['run_command_with_match', 'run_python_string', 'create_interpolated_string', 'run_command', 'run_command_string']

    def __init__(self):
        pass

    def set_command_handler(self, command_handler):
        self.cmd_hnd = command_handler

    def run_config_command(self, command):
        if self.is_command_in_config(command):
            commands_list = Config().get()["commands"][command]["steps"]
            for command_item in commands_list:
                command_action = command_item["action"].lower()
                print("ci: " + str(command_item))
                if command_action == 'run_command_with_match':
                    command_item_command = command_item["command"]
                    match = command_item["match"]
                    print("rcwm:" + str(command_item_command) + "match: " + match)
                    match_result = self.cmd_hnd.run_command_get_match(command_item_command, match)
                    print("match result: " + str(match_result))
                    try_set_var = command_item.get("try_set", None)
                    if try_set_var and match_result:
                        print("setting")
                        Config().get()["variables"][try_set_var] = match_result
                elif command_action == 'run_python_function':
                    python_function = self.get_python_function(command_item)

    def get_python_function(self, command_item):
        function_file = command_item["function_file"]
        function_name = command_item["function_name"]
        input_args = command_item.get("input_args", {})
        set_on_return = command_item.get("set_on_return", None)
        functions_path = plugins.resolve_plugin_path('functions')
        if functions_path not in sys.path:
            sys.path.insert(0, functions_path)
        function_module_name = function_file.replace(".py", "")
        function_module = importlib.import_module(function_module_name)
        function = getattr(sys.modules[function_module_name], function_name)
        interpolated_input_args = {}
        for key, value in input_args.items():
            interpolated_input_args[key] = Config().get()["variables"][value]
        function_result = function(**interpolated_input_args)
        if set_on_return:
            Config().get()["variables"][set_on_return] = function_result

    def is_command_in_config(self, command):
        commands_dict = Config().get()["commands"].get(command, None)
        return commands_dict != None
