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
class CommandHandler:

    def __init__(self):
        pass

    def initialise(self, startup_commands):
        self.get_config_settings()
        self.set_process_path()
        self.spawn_child_process(startup_commands)

    def spawn_child_process(self, startup_commands):
        try:
            args = [startup_commands]
            self.run_event_functions("before_spawn", args)
            self.child = pexpect.spawnu(self.process_path + self.process_settings["main_process_default_arguments"] + startup_commands)
            self.child.expect(self.end_of_output_regex)
            lines = self.get_filtered_output()
            args = [startup_commands, lines]
            self.run_event_functions("after_spawn", args)
        except Exception as ex:
            print("error in command_handler.spawn_child_process(): " + str(ex))
            print(traceback.format_exc())

    def close_command_handler(self):
        del self.child

    def get_config_settings(self):
        self.child = None
        self.config_settings = Config().get()["settings"]
        self.process_settings = self.config_settings["process"]
        self.main_process_name = self.process_settings["main_process_name"]
        self.end_of_output_regex = self.process_settings["end_of_output_regex"]
        self.ttl_stream_timeout = self.process_settings["ttl_stream_timeout"]
        self.base_buffer_filter = self.config_settings["buffers"]["base_filter"]
        self.error_buffer_filter = self.config_settings["buffers"]["error_filter"]

    def set_process_path(self):
        if self.process_settings["find_full_process_name"]:
            self.process_path = shutil.which(self.main_process_name)
        else:
            self.process_path = self.main_process_name
        if not self.process_path:
            raise RuntimeError("error: unable to specify a process name for pexpect")

    def run_command(self, command, buffer_name=''):
        try:
            args_list = [command, buffer_name]
            self.run_event_functions("before_command", args_list)
            self.child.sendline(command)
            self.child.expect(self.end_of_output_regex)
            lines = self.get_filtered_output(buffer_name)
            args_list = [command, buffer_name, lines]
            self.run_event_functions("after_command", args_list)
            return lines
        except Exception as ex:
            print("error in CommandHandler.run_command(): " + str(ex))

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

    def get_filtered_output(self, buffer_name=''):
        buffer_string = self.seek_to_end_of_tty()
        Log.write_to_log(buffer_string)
        lines = Filter.call_filter_class(buffer_string, self.error_buffer_filter)
        self.add_lines_to_error_buffer(lines)
        lines = Filter.call_filter_class(buffer_string, self.base_buffer_filter)
        if buffer_name != '':
            lines = Filter.filter_lines_for_buffer(lines, buffer_name)
        return lines

    def add_lines_to_error_buffer(self, lines):
        if lines:
            error_buffer_variable = Config().get()["settings"]['buffers']['error_input_variable']
            Config().get()["internal"]["buffer_caches"][error_buffer_variable] = lines

    def seek_to_end_of_tty(self, timeout=None):
        if not timeout:
            timeout = self.ttl_stream_timeout
        buffer_string = self.child.before
        try:
            while not self.child.expect(r'.+', timeout=timeout):
                buffer_string += self.child.match.group(0)
        except:
            pass
        return buffer_string
