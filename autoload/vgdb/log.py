import filter as Filter
import datetime
import vim
from config import Config

logging_settings = Config().get()["settings"]["logging"]
use_session_log_file = logging_settings["use_session_log_file"]
session_log_filename = logging_settings["session_log_filename"]
session_buffer_name = logging_settings["session_buffer_name"]

if use_session_log_file:
    log_file_handle = open(session_log_filename, "w+")

def write_to_log(log_string):
    if use_session_log_file:
        log_file_handle.write(log_string)
    log_lines = Filter.call_filter_class(log_string, session_buffer_name)
    full_cache = Config().get()["internal"]["buffer_caches"][session_buffer_name]
    if Config().get()["settings"]["logging"]["add_timestamp"]:
        full_cache.append("--- {0} ---".format(datetime.datetime.utcnow()))
    full_cache.extend(log_lines)
    Config().get()["internal"]["buffer_caches"][session_buffer_name] = full_cache
    vim.command("call vg_display#check_update_buffer('" + session_buffer_name + "')")
