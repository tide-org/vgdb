import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ptyprocessdir = os.path.join(currentdir, "../lib/ptyprocess")
pexpectdir = os.path.join(currentdir, "../lib/pexpect")
sys.path.insert(0, currentdir)
sys.path.insert(0, ptyprocessdir)
sys.path.insert(0, pexpectdir)

import pexpect
import vim
import re
from command_handler import CommandHandler
import symbols_status as SymbolsStatus

class Vgdb(object):

    def __init__(self):
        self.load_disassembly_on_start = vim.eval('g:vg_load_disassembly_on_start')
        self.startup_commands = ''
        self.current_command = ''
        self.cmd_hnd = None
        self.entrypoint = ''
        self.current_breakpoint = vim.eval('g:vg_current_breakpoint')

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
        self.current_breakpoint = self.cmd_hnd.run_command_get_match("stepi", '(0x[0-9a-f]{6,12})')
        if self.current_breakpoint != None:
            vim.command("let g:vg_current_breakpoint = '" + self.current_breakpoint + "'")
        print("current breakpoint: " + self.current_breakpoint)

    def display_disassembly(self):
        self.get_set_entrypoint()
        self.run_command_with_result("disassemble " + self.entrypoint, 'vg_disassembly')

    def get_set_entrypoint(self):
        if self.entrypoint == '':
            self.entrypoint = self.cmd_hnd.run_command_get_match("info file", 'Entry point: (0x[0-9a-f]{6,12})')
            vim.command("let g:vg_app_entrypoint = '" + self.entrypoint + "'")

    def run_to_entrypoint(self):
        self.get_set_entrypoint()
        self.cmd_hnd.run_command("b *" + self.entrypoint)
        remote_target = vim.eval('g:vg_remote_target')
        if remote_target:
            self.cmd_hnd.run_command("continue")
        else:
            self.cmd_hnd.run_command("run")
