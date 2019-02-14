import os
import sys
import inspect
sys.path.insert(0, os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
import traceback
import lib_paths
from command_handler import CommandHandler
from config_command import ConfigCommand
from config_command_item import ConfigCommandItem
from logging_decorator import logging

class Vgdb(object):

    _startup_commands = ''
    _command_handler = None

    @logging
    def start_gdb(self, commands):
        try:
            self._startup_commands = commands
            self._command_handler = CommandHandler()
            self._command_handler.spawn_process(commands)
        except Exception as ex:
            print("error in Vgdb.start_gdb(): " + str(ex))
            print(traceback.format_exc())

    @logging
    def stop_gdb(self):
        self._command_handler.close_command_handler()
        del self._command_handler

    @logging
    def run_config_command(self, command, buffer_name='', event_input_args_name=''):
        config_command_item = ConfigCommandItem()
        config_command_item.command = command
        config_command_item.buffer_name = buffer_name
        config_command_item.event_input_args_name = event_input_args_name
        ConfigCommand().run_config_command(config_command_item)
