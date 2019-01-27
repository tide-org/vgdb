import pexpect
import vim
import shutil
import sys
import re
import traceback
import importlib
import filter as Filter
import log as Log
from config import Config
from singleton import singleton
import plugin_helpers as Plugin

@singleton
class CommandHandlerEvent:

    def __init__(self):
        pass

    def initialise(self, startup_commands):
        self.child = None
        self.config_settings = Config().get()["settings"]
        self.set_process_path()
        self.spawn_child_process(startup_commands)


    def run_event_functions(self, event, args_list):
        functions = Config().get()["events"][event]
        if functions:
            for function in functions:
                function_file = function["function_file"]
                function_name = function["function_name"]
                functions_path = Plugin.resolve_plugin_path('functions')
                if functions_path not in sys.path:
                    sys.path.insert(0, functions_path)
                function_module_name = function_file.replace(".py", "")
                function_module = importlib.import_module(function_module_name)
                function = getattr(sys.modules[function_module_name], function_name)
                function_result = function(*args_list)
