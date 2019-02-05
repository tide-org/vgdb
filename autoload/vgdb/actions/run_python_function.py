import sys
from config import Config
import path_helpers as PathHelpers
import importlib
from action_base import action_base
import interpolate as Interpolate

class run_python_function(action_base):

    _command_item = {}
    _buffer_name = {}
    _command_args = {}
    _function_file = ''
    _function_name = ''
    _input_args = {}
    _set_on_return = ''
    _functions_path = ''

    def run(self, command_item, buffer_name='', command_args={}):
        self.__set_locals(command_item, buffer_name, command_args)
        self.__set_functions_path()
        function_module_name = self._function_file.replace(".py", "")
        function_module = importlib.import_module(function_module_name)
        function = getattr(sys.modules[function_module_name], self._function_name)
        interpolated_input_args = self.get_interpolated_args(self._command_item)
        if self._command_args:
            interpolated_input_args["command_args"] = self._command_args
        function_result = function(**interpolated_input_args)
        if self._set_on_return:
            Config().get()["variables"][self._set_on_return] = function_result

    def __set_functions_path(self):
        if self._functions_path not in sys.path:
            sys.path.insert(0, self._functions_path)

    def __set_locals(self, command_item, buffer_name, command_args):
        self._command_item = command_item
        self._buffer_name = buffer_name
        self._command_args = command_args
        self._function_file = self._command_item["function_file"]
        self._function_name = self._command_item["function_name"]
        self._input_args = self._command_item.get("input_args", {})
        self._set_on_return = self._command_item.get("set_on_return", None)
        self._functions_path = PathHelpers.resolve_plugin_path('functions')

    def get_interpolated_args(self, command_item):
        input_args = command_item.get("input_args", {})
        interpolated_input_args = {}
        for key, value in input_args.items():
            interpolated_input_args[key] = Interpolate.interpolate_variables(value)
        return interpolated_input_args
