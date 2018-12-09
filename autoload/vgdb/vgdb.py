import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ptyprocessdir = os.path.join(currentdir, "../lib/ptyprocess")
pexpectdir = os.path.join(currentdir, "../lib/pexpect")
poyodir = os.path.join(currentdir, "../lib/poyo")
sys.path.insert(0, currentdir)
sys.path.insert(0, ptyprocessdir)
sys.path.insert(0, pexpectdir)
sys.path.insert(0, poyodir)

import pexpect

import vim
import re

from command_handler import CommandHandler
from config import Config
import symbols_status as SymbolsStatus

class Vgdb(object):

    def __init__(self):
        self.startup_commands = ''
        self.current_command = ''
        self.cmd_hnd = None
        self.entrypoint = None
        self.config_dictionary = {}
        self.variable_dictionary = {}
        self.default_input_buffer_variable = ''
        self.get_config()

    def start_gdb(self, commands):
        try:
            self.startup_commands = commands
            self.cmd_hnd = CommandHandler(commands)
        except Exception as ex:
            print("error in Vgdb.start_gdb(): " + ex)

    def run_command_with_result(self, command, buffer_name=''):
        try:
            vim.command("let " + self.default_input_buffer_variable + " = []")
            lines = self.cmd_hnd.run_command(command, buffer_name)
            self.add_lines_to_input_buffer(lines)
        except Exception as ex:
            print("error in Vgdb.run_command(): " + ex)

    def add_lines_to_input_buffer(self, lines):
        if lines:
            for line in lines:
                vim.command("call add(" + self.default_input_buffer_variable + ", '" + line + "' )")

    def run_config_command(self, command):
        if self.is_command_in_config(command):
            commands_dict = self.config_dictionary["commands"][command]
            commands_list = list(commands_dict.keys())
            for command_item in commands_list:
                command_values = commands_dict[command_item]
                if command_values["type"].lower() == 'command_with_match':
                  command_item_command = command_values["command"]
                  match = command_values["match"]
                  match_result = self.cmd_hnd.run_command_get_match(command_item_command, match)
                  try_set_var = command_values.get("try_set", None)
                  if try_set_var != None:
                      if match != None:
                          self.set_variable_for_command(try_set_var, match_result)

    def set_variable_for_command(self, variable_name, variable_value):
        variables_dict = self.config_dictionary["variables"]
        if self.is_variable_in_config(variable_name):
            variable_type = variables_dict[variable_name].get("type", None)
            if variable_type != None and variable_value != None:
                self.set_variable_for_type(variable_name, variable_value, variable_type)

    def set_variable_for_type(self, variable_name, variable_value, variable_type):
        if variable_type.lower().__contains__('python'):
            self.variable_dictionary[variable_name] = variable_value
        if variable_type.lower().__contains__('vim'):
            vim.command("let g:vg_" + variable_name + " = " + str(variable_value))

    def is_variable_in_config(self, variable_name):
        vars_dict = self.config_dictionary["variables"]
        variable_exists = vars_dict.get(variable_name, None)
        if variable_exists != None:
            return True
        return False

    def is_command_in_config(self, command):
        config_commands = self.config_dictionary["commands"]
        commands_dict = config_commands.get(command, None)
        if commands_dict != None:
            return True
        return False

    def try_set_breakpoint(self):
        if self.variable_dictionary['current_frame_address']:
            vim.command("let g:vg_current_frame_address = '" + self.variable_dictionary['current_frame_address'] + "'")

    def display_disassembly(self):
        self.get_set_entrypoint()
        self.run_command_with_result("info breakpoints", "vg_breakpoints")
        self.run_command_with_result("disassemble", 'vg_disassembly')

    def get_set_entrypoint(self):
        if not self.entrypoint:
            self.entrypoint = self.cmd_hnd.run_command_get_match("info file", 'Entry point: (0x[0-9a-f]{2,16})')
            if self.entrypoint:
                self.entrypoint = self.pad_hexadecimal_to_64bit(self.entrypoint)
                self.variable_dictionary['current_frame_address'] = self.entrypoint
                vim.command("let g:vg_app_entrypoint = '" + self.entrypoint + "'")
        self.try_set_breakpoint()

    def pad_hexadecimal_to_64bit(self, hex_string):
        return '0x' + hex_string[2:].zfill(16)

    def run_to_entrypoint(self):
        self.get_set_entrypoint()
        if self.entrypoint:
            self.cmd_hnd.run_command("break *" + self.entrypoint)
            remote_target = vim.eval('g:vg_remote_target')
            if remote_target:
                self.cmd_hnd.run_command("continue")
            else:
                self.cmd_hnd.run_command("run")
        else:
            print("error: unable to get entrypoint")

    def get_config(self):
        self.config_dictionary = Config().get()
        self.default_input_buffer_variable = self.config_dictionary["settings"]["buffers"]["default_input_buffer_variable"]
