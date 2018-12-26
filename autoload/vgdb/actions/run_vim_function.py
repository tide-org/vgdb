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
        vim_command = "call " + function_name + "()"
        vim.command(vim_command)
