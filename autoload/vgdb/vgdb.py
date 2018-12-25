import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ptyprocessdir = os.path.join(currentdir, "../lib/ptyprocess")
pexpectdir = os.path.join(currentdir, "../lib/pexpect")
pyyamldir = os.path.join(currentdir, "../lib/pyyaml")
sys.path.insert(0, currentdir)
sys.path.insert(0, ptyprocessdir)
sys.path.insert(0, pexpectdir)
sys.path.insert(0, pyyamldir)

import pexpect

import vim
import re

from command_handler import CommandHandler
from config import Config
from config_command import ConfigCommand

class Vgdb(object):

    def __init__(self):
        self.cmd_hnd = None
        self.config_command = ConfigCommand()

    def start_gdb(self, commands):
        try:
            self.startup_commands = commands
            self.cmd_hnd = CommandHandler(commands)
            self.config_command.set_command_handler(self.cmd_hnd)
        except Exception as ex:
            print("error in Vgdb.start_gdb(): " + ex)

    def run_config_command(self, command, buffer_name=''):
        self.config_command.run_config_command(command, buffer_name)

    def display_disassembly(self):
        pass
        #self.get_set_entrypoint()
        self.run_config_command("list_breakpoints", "vg_breakpoints")
        self.run_config_command("disassemble", 'vg_disassembly')
