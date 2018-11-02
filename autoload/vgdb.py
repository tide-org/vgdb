import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ptyprocessdir = os.path.join(currentdir, "lib/ptyprocess")
pexpectdir = os.path.join(currentdir, "lib/pexpect")
sys.path.insert(0, ptyprocessdir)
sys.path.insert(0, pexpectdir)

import pexpect
import vim
import shutil

class Vgdb(object):

    def start_gdb(self, commands):
        try:
            gdb_path = shutil.which("gdb")
            self.child = pexpect.spawnu(gdb_path +  ' --interpreter=mi2 ' + commands)
            self.child.expect('\(gdb\)')
            return 0
        except Exception as ex:
            print("error in start_gdb: " + ex)
            return 1

    def run_command(self, command):
        try:
            self.child.sendline(command)
            self.child.expect('\(gdb\)')
            vim.command("let g:query_result = []")
            lines = self.child.before.replace("\r","").replace("'", "''").split("\n")
            for line in lines:
                vim.command("call add(g:query_result, '" + line + "' )")
            return 0
        except Exception as ex:
            print("error in run_command: " + ex)
            return 1

