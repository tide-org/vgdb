import pexpect
import vim
import shutil
import re
import filter as Filter
import log as Log
import symbols_status as SymbolsStatus
from config import Config

class CommandHandler(object):

    def __init__(self, startup_commands):
        self.get_config_settings()
        self.set_process_path()
        self.spawn_child_process(startup_commands)

    def spawn_child_process(self, startup_commands):
        self.child = pexpect.spawnu(self.process_path + self.process_settings["main_process_default_arguments"] + startup_commands)
        self.child.expect(self.end_of_output_regex)
        lines = self.get_filtered_output()
        SymbolsStatus.set_binary_symbols_status(lines)

    def get_config_settings(self):
        self.child = None
        self.config_settings = Config().get()["settings"]
        self.process_settings = self.config_settings["process"]
        self.main_process_name = self.process_settings["main_process_name"]
        self.end_of_output_regex = self.process_settings["end_of_output_regex"]
        self.ttl_stream_timeout = self.process_settings["ttl_stream_timeout"]
        self.base_buffer_filter = self.config_settings["buffers"]["base_filter"]

    def set_process_path(self):
        if self.process_settings["find_full_process_name"]:
            self.process_path = shutil.which(self.main_process_name)
        else:
            self.process_path = self.main_process_name

    def run_command(self, command, buffer_name=''):
        try:
            self.child.sendline(command)
            self.child.expect(self.end_of_output_regex)
            lines = self.get_filtered_output(buffer_name)
            self.check_set_remote(command, lines)
            return lines
        except Exception as ex:
            print("error in CommandHandler.run_command(): " + ex)

    def check_set_remote(self, command, lines):
        if 'target remote' in command.lower():
            SymbolsStatus.set_binary_symbols_status(lines)
            Config().get()['variables']['remote_target'] = 1

    def get_filtered_output(self, buffer_name=''):
        buffer_string = self.seek_to_end_of_tty()
        Log.write_to_log(buffer_string)
        lines = Filter.call_filter_class(buffer_string, self.base_buffer_filter)
        if buffer_name != '':
            lines = Filter.filter_lines_for_buffer(lines, buffer_name)
        return lines

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

    def run_command_get_match(self, command, regex_match):
        lines = self.run_command(command)
        return self.get_match(regex_match, lines)

    def get_match(self, regex_match, lines):
        match_string = None
        for line in lines:
            if re.search(regex_match, line):
                match = re.search(regex_match, line)
                match_string = match.group()
        return match_string
