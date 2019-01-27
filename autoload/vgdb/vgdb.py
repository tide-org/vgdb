import os
import sys
import inspect
import traceback

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ptyprocessdir = os.path.join(currentdir, "../lib/ptyprocess")
pexpectdir = os.path.join(currentdir, "../lib/pexpect")
pyyamldir = os.path.join(currentdir, "../lib/pyyaml/lib3")
jinjadir = os.path.join(currentdir, "../lib/jinja")
markupsafedir = os.path.join(currentdir, "../lib/markupsafe/src")
sys.path.insert(0, currentdir)
sys.path.insert(0, ptyprocessdir)
sys.path.insert(0, pexpectdir)
sys.path.insert(0, pyyamldir)
sys.path.insert(0, jinjadir)
sys.path.insert(0, markupsafedir)

from command_handler import CommandHandler
from config_command import ConfigCommand

class Vgdb(object):

    def start_gdb(self, commands):
        try:
            self.startup_commands = commands
            self.cmd_hnd = CommandHandler()
            self.cmd_hnd.initialise(commands)
            ConfigCommand().set_command_handler(self.cmd_hnd)
        except Exception as ex:
            print("error in Vgdb.start_gdb(): " + str(ex))
            print(traceback.format_exc())

    def stop_gdb(self):
        self.cmd_hnd.close_command_handler()
        del self.cmd_hnd

    def run_config_command(self, command, buffer_name='', event_input_args=''):
        ConfigCommand().run_config_command(command, buffer_name, event_input_args)
