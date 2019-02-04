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
from config_command import ConfigCommand
from config_command_item import ConfigCommandItem

@singleton
class CommandHandler:

    def __init__(self):
        pass

    def initialise(self, startup_commands):
        self.child = None
        self.config_settings = Config().get()["settings"]
        self.set_process_path()
        self.spawn_child_process(startup_commands)

    def spawn_child_process(self, startup_commands):
        try:
            self.child = pexpect.spawnu(self.process_path + self.config_settings["process"]["main_process_default_arguments"] + " " + startup_commands)
            self.child.expect(self.config_settings["process"]["end_of_output_regex"])
            lines = self.get_filtered_output()
        except Exception as ex:
            print("error in command_handler.spawn_child_process(): " + str(ex))
            print(traceback.format_exc())

    def close_command_handler(self):
        del self.child

    def set_process_path(self):
        if self.config_settings["process"]["find_full_process_name"]:
            self.process_path = shutil.which(self.config_settings["process"]["main_process_name"])
        else:
            self.process_path = self.config_settings["process"]["main_process_name"]
        if not self.process_path:
            raise RuntimeError("error: unable to specify a process name for pexpect")

    def run_command(self, command, buffer_name=''):
        try:
            self.run_event_commands("before_command", command, buffer_name)
            self.child.sendline(command)
            self.child.expect(self.config_settings["process"]["end_of_output_regex"])
            lines = self.get_filtered_output(buffer_name)
            self.run_event_commands("after_command", command, buffer_name, lines)
            return lines
        except Exception as ex:
            print("error in CommandHandler.run_command(): " + str(ex))

    def run_event_commands(self, event_name, process_command, buffer_name, lines=[]):
        print("HERE1")
        for command in (Config().get()["events"][event_name] or []):
            print("HERE2")
            cci = ConfigCommandItem()
            cci.command = command
            cci.buffer_name = buffer_name
            cci.args_dict = args_dict={ 'process_command': process_command, 'lines': lines }
            print("HERE3")
            ConfigCommand().run_config_command(cci)

    def get_filtered_output(self, buffer_name=''):
        buffer_string = self.seek_to_end_of_tty()
        Log.write_to_log(buffer_string)
        # TODO: make these filters configurable from yaml file
        lines = Filter.call_filter_class(buffer_string, self.config_settings["buffers"]["error_filter"])
        self.add_lines_to_error_buffer(lines)
        lines = Filter.call_filter_class(buffer_string, self.config_settings["buffers"]["base_filter"])
        if buffer_name != '':
            lines = Filter.filter_lines_for_buffer(lines, buffer_name)
        return lines

    def add_lines_to_error_buffer(self, lines):
        if lines:
            error_buffer_variable = Config().get()["settings"]['buffers']['error_input_variable']
            Config().get()["internal"]["buffer_caches"][error_buffer_variable] = lines

    def seek_to_end_of_tty(self, timeout=None):
        if not timeout:
            timeout = self.config_settings["process"]["ttl_stream_timeout"]
        buffer_string = self.child.before
        try:
            while not self.child.expect(r'.+', timeout=timeout):
                buffer_string += self.child.match.group(0)
        except:
            pass
        return buffer_string
