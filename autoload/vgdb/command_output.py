import shutil
import traceback
import pexpect
import filter as Filter
import log as Log
from config import Config
from singleton import singleton
from config_command import ConfigCommand
from config_command_item import ConfigCommandItem
from command_process import CommandProcess

@singleton
class CommandHandler:

    def __init__(self):
        self._child = None
        self._config_settings = Config().get()["settings"]
        self._command_process = CommandProcess()

    def spawn_process(self, startup_commands):
        try:
            self._command_process.spawn_process(startup_commands)
            self.__get_and_handle_filtered_output()
        except Exception as ex:
            print("error in command_handler.spawn_child_process(): " + str(ex) + "\n" + traceback.format_exc())

    def run_command(self, command, buffer_name=''):
        try:
            self.__run_event_commands("before_command", command, buffer_name)
            self._command_process.send_command_to_process(command)
            lines = self.__get_and_handle_filtered_output(buffer_name)
            self.__run_event_commands("after_command", command, buffer_name, lines)
            return lines
        except Exception as ex:
            print("error in CommandHandler.run_command(): " + str(ex) + "\n" + traceback.format_exc())

    def close_command_handler(self):
        self._command_process.close_command_process()

    def __run_event_commands(self, event_name, process_command, buffer_name, lines=[]):
        for command in Config().get()["events"][event_name] or []:
            cci = ConfigCommandItem()
            cci.command = command
            cci.buffer_name = buffer_name
            cci.args_dict = {'process_command': process_command, 'lines': lines}
            ConfigCommand().run_config_command(cci)

    def __get_and_handle_filtered_output(self, buffer_name=''):
        output_string = self._command_process.seek_to_end_of_tty()
        Log.write_to_log(output_string)
        self.__handle_output_for_errors(output_string)
        lines = self.__handle_output_for_buffers(output_string, buffer_name)
        return lines

    def __handle_output_for_buffers(self, output_string, buffer_name):
        lines = Filter.call_filter_class(output_string, self._config_settings["buffers"]["base_filter_name"])
        if buffer_name:
            lines = Filter.filter_lines_for_buffer(lines, buffer_name)
        return lines

    def __handle_output_for_errors(self, output_string):
        lines = Filter.call_filter_class(output_string, self._config_settings["buffers"]["error_filter_name"])
        self.__add_lines_to_error_buffer(lines)

    def __add_lines_to_error_buffer(self, lines):
        if lines:
            error_buffer_variable = Config().get()["settings"]['buffers']['error_input_variable']
            Config().get()["internal"]["buffer_caches"][error_buffer_variable] = lines
