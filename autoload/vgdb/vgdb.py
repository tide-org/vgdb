import os
import sys
import inspect
import traceback

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir)

import lib_paths
from command_handler import CommandHandler
from config_command import ConfigCommand
from config_command_item import ConfigCommandItem

class Vgdb(object):

    def start_gdb(self, commands):
        try:
            self.startup_commands = commands
            self.cmd_hnd = CommandHandler()
            self.cmd_hnd.initialise(commands)
        except Exception as ex:
            print("error in Vgdb.start_gdb(): " + str(ex))
            print(traceback.format_exc())

    def stop_gdb(self):
        self.cmd_hnd.close_command_handler()
        del self.cmd_hnd

    def run_config_command(self, command, buffer_name='', event_input_args_name=''):
        config_command_item = ConfigCommandItem()
        config_command_item.command = command
        config_command_item.buffer_name = buffer_name
        config_command_item.event_input_args_name = event_input_args_name
        ConfigCommand().run_config_command(config_command_item)
