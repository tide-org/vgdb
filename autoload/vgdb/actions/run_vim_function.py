import vim
import os
from config import Config
import plugin_helpers as Plugins
from action_predicate_base import action_predicate_base
import plugin_helpers as Plh

class run_vim_function(action_predicate_base):

    def run(self, command_item, buffer_name=''):
        function_file = command_item["function_file"]
        function_name = command_item["function_name"]
        functions_path = Config().get()["settings"]["plugins"]["functions_path"]
        resolved_functions_path = Plh.resolve_plugin_path("functions")
        function_file_path = os.path.join(resolved_functions_path, function_file)
        vim.command("source " + function_file_path)
        kwargs = self.get_interpolated_args(command_item)
        vim_command = "call " + function_name + "(" + str(kwargs) + ")"
        vim.command(vim_command)

    def interpolate_variables(self, msg):
        variable_names = Config().get()["variables"].keys()
        for variable in variable_names:
            moustache_variable = "{{ " + variable + " }}"
            if moustache_variable in msg:
                msg = msg.replace(moustache_variable, str(Config().get()["variables"][variable]))
        return msg

    def get_interpolated_args(self, command_item):
        input_args = command_item.get("event_input_args", {})
        interpolated_input_args = {}
        for key, value in input_args.items():
            interpolated_input_args[key] = self.interpolate_variables(value)
        return interpolated_input_args
