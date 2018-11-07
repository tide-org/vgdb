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
import re

class Vgdb(object):

    def start_gdb(self, commands):
        try:
            gdb_path = shutil.which("gdb")
            self.child = pexpect.spawnu(gdb_path +  ' -q --interpreter=mi2 ' + commands)
            self.child.expect('\(gdb\)')
            lines = self.get_filtered_output()
            self.set_binary_symbols_status(lines)
            return 0
        except Exception as ex:
            print("error in start_gdb: " + ex)
            return 1

    def set_binary_symbols_status(self, lines):
        binary_loaded = False
        no_symbols_found = False
        for line in lines:
            if 'Reading symbols from' in line:
                binary_loaded = True
            if '(no debugging symbols found)' in line:
                no_symbols_found = True
                binary_loaded = True
        symbols_loaded = not no_symbols_found
        # this is an impssible state which can occur if neither string is matched above
        if symbols_loaded == True and binary_loaded == False:
            symbols_loaded = False
        vim.command("let g:vg_binary_loaded = " + str(int(binary_loaded)))
        vim.command("let g:vg_symbols_loaded = " + str(int(symbols_loaded)))

    def run_command_with_result(self, command):
        try:
            vim.command("let g:query_result = []")
            lines = self.run_command(command)
            for line in lines:
                vim.command("call add(g:query_result, '" + line + "' )")
            return 0
        except Exception as ex:
            print("error in run_command: " + ex)
            return 1

    def run_to_entrypoint(self):
        entrypoint = self.get_entrypoint()
        vim.command("let g:app_entrypoint = '" + entrypoint + "'")
        self.run_command("b *" + entrypoint)
        self.run_command("run")

    def run_command_get_match(self, command, regex_match):
        match_string = None
        lines = self.run_command(command)
        return self.get_match(regex_match, lines)

    def get_match(self, regex_match, lines):
        pattern = re.compile(regex_match)
        for line in lines:
            if re.search(pattern, line):
                match = re.search(pattern, line)
                if match != None:
                    match_string = match.group(1)
        return match_string

    def get_entrypoint(self):
        return self.run_command_get_match("info file", 'Entry point: (0x[0-9a-f]{6,12})')

    def run_command(self, command):
        try:
            self.child.sendline(command)
            self.child.expect('\(gdb\)')
            lines = self.get_filtered_output()
            self.set_binary_symbols_status(lines)
            if 'target' in command.lower():
                self.set_binary_symbols_status(lines)
            buffer_string = self.seek_to_end_of_tty()
            return self.filter_command_result(buffer_string)
        except Exception as ex:
            print("error in run_command: " + ex)

    def get_filtered_output(self):
        buffer_string = self.seek_to_end_of_tty()
        return self.filter_command_result(buffer_string)

    def seek_to_end_of_tty(self, timeout=0.05):
        buffer_string = self.child.before
        try:
            while not self.child.expect(r'.+', timeout=timeout):
                buffer_string += self.child.match.group(0)
        except:
            pass
        return buffer_string

    def filter_command_result(self, buffer_result):
        lines_to_keep = []
        lines =  buffer_result.replace("\r","").replace("'", "''").split("\n")
        for line in lines:
            if line.startswith('~"'):
                lines_to_keep.append(line.lstrip('~"').rstrip('\\n"'))
        return lines_to_keep






