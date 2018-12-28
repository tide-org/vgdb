import vim
import os
from config import Config
import plugin_helpers as Plugins
from action_predicate_base import action_predicate_base

class run_vim_function(action_predicate_base):

    def run(self, command_item, buffer_name=''):
        function_file = command_item["function_file"]
        function_name = command_item["function_name"]
        functions_path = Config().get()["settings"]["plugins"]["functions_path"]
        function_file_path = os.path.join(functions_path, function_file)
        vim.command("source " + function_file_path)
        kwargs = self.get_interpolated_args(command_item)
        vim_command = "call " + function_name + "(" + str(kwargs) + ")"
        vim.command(vim_command)

    def get_interpolated_args(self, command_item):
        input_args = command_item.get("input_args", {})
        interpolated_input_args = {}
        for key, value in input_args.items():
            interpolated_input_args[key] = Config().get()["variables"][value]
        return interpolated_input_args
