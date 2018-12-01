import pexpect
import vim
import shutil
import re
import filter as Filter
import log as Log
import symbols_status as SymbolsStatus

class CommandHandler(object):

    def __init__(self, startup_commands):
        self.child = None
        gdb_path = shutil.which("gdb")
        self.child = pexpect.spawnu(gdb_path +  ' -q --interpreter=mi2 ' + startup_commands)
        self.child.expect('\(gdb\)')
        lines = self.get_filtered_output()
        SymbolsStatus.set_binary_symbols_status(lines)

    def run_command(self, command, buffer_name=''):
        try:
            self.child.sendline(command)
            self.child.expect('\(gdb\)')
            lines = self.get_filtered_output(buffer_name)
            self.check_set_remote(command, lines)
            return lines
        except Exception as ex:
            print("error in CommandHandler.run_command(): " + ex)

    def check_set_remote(self, command, lines):
        if 'target remote' in command.lower():
            SymbolsStatus.set_binary_symbols_status(lines)
            vim.command("let g:vg_remote_target = 1")

    def get_filtered_output(self, buffer_name=''):
        buffer_string = self.seek_to_end_of_tty()
        Log.write_to_log(buffer_string)
        lines = Filter.call_filter_class(buffer_string, 'vg_base')
        if buffer_name != '':
            lines = Filter.filter_lines_for_buffer(lines, buffer_name)
        return lines

    def seek_to_end_of_tty(self, timeout=0.05):
        buffer_string = self.child.before
        try:
            while not self.child.expect(r'.+', timeout=timeout):
                buffer_string += self.child.match.group(0)
        except:
            pass
        return buffer_string

    def run_command_get_match(self, command, regex_match):
        lines = self.run_command(command)
        return self.get_match(regex_match, lines)

    def get_match(self, regex_match, lines):
        match_string = None
        pattern = re.compile(regex_match)
        for line in lines:
            if re.search(pattern, line):
                match = re.search(pattern, line)
                if match != None:
                    match_string = match.group(1)
        return match_string
