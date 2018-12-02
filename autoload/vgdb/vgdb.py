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
        self.load_disassembly_on_start = vim.eval('g:vg_load_disassembly_on_start')
        self.startup_commands = ''
        self.current_command = ''
        self.cmd_hnd = None
        self.entrypoint = None
        self.current_frame_address = ''
        self.config_dictionary = {}

    def start_gdb(self, commands):
        try:
            self.startup_commands = commands
            self.cmd_hnd = CommandHandler(commands)
        except Exception as ex:
            print("error in Vgdb.start_gdb(): " + ex)

    def run_command_with_result(self, command, buffer_name=''):
        try:
            vim.command("let g:vg_query_result = []")
            lines = self.cmd_hnd.run_command(command, buffer_name)
            if lines:
                for line in lines:
                    vim.command("call add(g:vg_query_result, '" + line + "' )")
        except Exception as ex:
            print("error in Vgdb.run_command(): " + ex)

    def run_stepi(self):
        self.current_frame_address = self.cmd_hnd.run_command_get_match("stepi", '(0x[0-9a-f]{2,16})')
        self.try_set_breakpoint()

    def run_continue(self):
        self.current_frame_address = self.cmd_hnd.run_command_get_match("continue", '(0x[0-9a-f]{2,16})')
        self.try_set_breakpoint()

    def try_set_breakpoint(self):
        if self.current_frame_address:
            vim.command("let g:vg_current_frame_address = '" + self.current_frame_address + "'")

    def display_disassembly(self):
        self.get_set_entrypoint()
        self.run_command_with_result("info breakpoints", "vg_breakpoints")
        self.run_command_with_result("disassemble", 'vg_disassembly')

    def get_set_entrypoint(self):
        if not self.entrypoint:
            self.entrypoint = self.cmd_hnd.run_command_get_match("info file", 'Entry point: (0x[0-9a-f]{2,16})')
            if self.entrypoint:
                self.entrypoint = self.pad_hexadecimal_to_64bit(self.entrypoint)
                self.current_frame_address = self.entrypoint
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
        self.config_dictionary = Config().get
