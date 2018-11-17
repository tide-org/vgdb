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

    def start_gdb(self, commands):
        try:
            self.startup_commands = commands
            self.cmd_hnd = CommandHandler(commands)
        except Exception as ex:
            print("error in Vgdb.start_gdb(): " + ex)

    def run_command_with_result(self, command):
        try:
            vim.command("let g:vg_query_result = []")
            lines = self.cmd_hnd.run_command(command)
            for line in lines:
                vim.command("call add(g:vg_query_result, '" + line + "' )")
        except Exception as ex:
            print("error in Vgdb.run_command(): " + ex)

    def display_disassembly(self):
        self.get_set_entrypoint()
        self.run_command_with_result("disassemble " + self.entrypoint)

    def get_set_entrypoint(self):
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
