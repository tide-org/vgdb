import os
import vim
from action_base import action_base
from config import Config
import interpolate as Interpolate

class set_buffer(action_base):

    _command_item = ''
    _calling_buffer_name = ''
    _buffer_name = ''
    _file_name = ''

    def run(self, command_item, buffer_name=''):
        self.__set_locals(command_item, buffer_name)
        self.__load_buffer_cache_from_file()
        self.__run_vim_command()

    def __load_buffer_cache_from_file(self):
        if os.path.isfile(self._file_name):
            file_handle = open(self._file_name, 'r+')
            lines = [line.rstrip('\n') for line in file_handle.readlines()]
            file_handle.close()
            Config().get()["internal"]["buffer_caches"][self._buffer_name] = lines
        else:
            raise RuntimeError("error: unable to find file: " + self._file_name)

    def __run_vim_command(self):
        vim_command = "call vg_display#default_display_buffer('" + self._buffer_name + "')"
        vim.command(vim_command)

    def __set_locals(self, command_item, buffer_name):
        self._command_item = command_item
        self._calling_buffer_name = buffer_name
        self._buffer_name = Interpolate.interpolate_variables(self._command_item["buffer_name"])
        self._file_name = Interpolate.interpolate_variables(self._command_item["file_name"])
