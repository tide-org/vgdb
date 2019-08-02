function! set_buffer#for_filename(...)
   let l:event_args = get(a:, 1, {})
endfunction

"
"
"import os
"import vim
"from action_base import action_base
"from config import Config
"import interpolate as Interpolate
"
"class set_buffer(action_base):
"
"    _command_item = ''
"    _calling_buffer_name = ''
"    _buffer_name = ''
"    _file_name = ''
"    _buffer_filename_variable = ''
"    _buffer_filename = ''
"    _buffer_window_number = ''
"
"# rewrite the whole thing in vim
"
"    def run(self, command_item, buffer_name=''):
"        self._command_item = command_item
"        self._calling_buffer_name = buffer_name
"        self._buffer_name = Interpolate.interpolate_variables(self._command_item["buffer_name"])
"        self._file_name = Interpolate.interpolate_variables(self._command_item["file_name"])
"        self._buffer_filename_variable = Config().get()["buffers"][self._buffer_name].get('buffer_filename_variable', '')
"        if self._buffer_filename_variable:
"            self._buffer_filename = Config().get()["variables"].get(self._buffer_filename_variable, '')
"        if self._buffer_filename_variable:
"# here
"            mapped_file_buffers = Config().get()["internal"]["variables"].get("mapped_file_buffers", {})
"            if not mapped_file_buffers:
"                Config().get()["internal"]["variables"]["mapped_file_buffers"] = {}
"            self._buffer_window_number = mapped_file_buffers.get(self._buffer_name, '')
"            if not self._buffer_window_number:
"                self._buffer_window_number = vim.eval("vg_buffer_find#find_window_by_bufname('" + self._buffer_name + "', 1)")    # vim
"                Config().get()["internal"]["variables"]["mapped_file_buffers"][self._buffer_name] = self._buffer_window_number
"                vim.command("set buftype=")                                                                                       # vim
"                vim.command("set modifiable")                                                                                     # vim
"            vim.command(str(self._buffer_window_number) + "wincmd w")                                                             # vim
"            vim.command("silent edit! " + self._buffer_filename)                                                                  # vim
"# to here -> vim
"        else:
"# here
"            if os.path.isfile(self._file_name):
"                file_handle = open(self._file_name, 'r+')
"                lines = [line.rstrip('\n') for line in file_handle.readlines()]
"                file_handle.close()
"                Config().get()["internal"]["buffer_caches"][self._buffer_name] = lines
"            else:
"                raise RuntimeError("error: unable to find file: " + self._file_name)
"            vim.command("call vg_display#default_display_buffer('" + self._buffer_name + "')")                                    # vim
"# to here -> vim
