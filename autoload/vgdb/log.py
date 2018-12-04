import filter as Filter
import vim
from config import Config

logging_settings = Config().get()["settings"]["logging"]
use_session_log_file = logging_settings["use_session_log_file"]
session_log_filename = logging_settings["session_log_filename"]
buffer_input_variable = logging_settings["buffer_input_variable"]
session_buffer_name = logging_settings["session_buffer_name"]

if use_session_log_file:
    log_file_handle = open(session_log_filename, "w+")

def write_to_log(log_string):
    if use_session_log_file:
        log_file_handle.write(log_string)
    vim.command("let " + buffer_input_variable  + " = []")
    log_lines = Filter.call_filter_class(log_string, session_buffer_name)
    for log_line in log_lines:
        vim.command("call add(" + buffer_input_variable + ", '" + log_line + "' )")
    vim.command("call vg_display#check_update_session_log()")
