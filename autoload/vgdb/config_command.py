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

    valid_actions = [
            'run_command_with_match',
            'run_python_function',
            'create_interpolated_string',
            'run_command',
            'run_command_string',
            'run_vim_function',
            'run_config_command'
    ]

    def __init__(self):
        self.default_input_buffer_variable = Config().get()["settings"]["buffers"]["default_input_buffer_variable"]

    def set_command_handler(self, command_handler):
        self.cmd_hnd = command_handler

    def run_config_command(self, command, buffer_name=''):
        if self.is_command_in_config(command):
            commands_list = Config().get()["commands"][command]["steps"]
            for command_item in commands_list:
                lines = []
                vim.command("let " + self.default_input_buffer_variable + " = []")
                command_action = command_item["action"].lower()
                lines = self.run_command_action(command_action, command_item, buffer_name)
                if lines and len(lines) > 0:
                    self.add_lines_to_input_buffer(lines)

    def run_command_action(self, command_action, command_item, buffer_name):
        if command_action in self.valid_actions:
            if command_action == 'run_command_with_match':
                return self.run_command_with_match(command_item, buffer_name)
            elif command_action == 'run_python_function':
                return self.run_python_function(command_item)
            elif command_action == 'run_config_command':
                return self.run_config_command(command_item['name'], buffer_name)
            elif command_action == 'create_interpolated_string':
                return self.create_interpolated_string(command_item, buffer_name)
            elif command_action == 'run_command_string':
                return self.run_command_string(command_item, buffer_name)
            elif command_action == 'run_command':
                return self.cmd_hnd.run_command(command_item['command'], buffer_name)
            elif command_action == 'run_vim_function':
                return self.run_vim_function(command_item)

    def run_command_with_match(self, command_item, buffer_name=''):
        command_item_command = command_item["command"]
        match = command_item["match"]
        match_result = self.cmd_hnd.run_command_get_match(command_item_command, match)
        try_set_var = command_item.get("try_set", None)
        if try_set_var and match_result:
            Config().get()["variables"][try_set_var] = match_result

    def run_vim_function(self, command_item, buffer_name=''):
        function_name = command_item["function_name"]
        vim_command = "call " + function_name + "()"
        vim.command(vim_command)

    def run_command_string(self, command_item, buffer_name=''):
        variable_name = command_item['variable_name']
        variable_value = Config().get()["variables"][variable_name]
        return self.cmd_hnd.run_command(variable_value, buffer_name)

    def create_interpolated_string(self, command_item, buffer_name=''):
        variable_name = command_item["variable_name"]
        string_value = command_item["value"]
        args = command_item["args"]
        resolved_args = []
        for arg in args:
            resolved_args.append(Config().get()["variables"][arg])
        result_string = string_value.format(*resolved_args)
        Config().get()["variables"][variable_name] = result_string

    def run_python_function(self, command_item, buffer_name=''):
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

    def add_lines_to_input_buffer(self, lines):
        if lines:
            for line in lines:
                vim.command("call add(" + self.default_input_buffer_variable + ", '" + line + "' )")

    def is_command_in_config(self, command):
        commands_dict = Config().get()["commands"].get(command, None)
        return commands_dict != None
