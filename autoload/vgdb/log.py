import filter as Filter
import vim

use_session_log_file = vim.eval('g:vg_use_session_log_file')
session_log_filename = vim.eval('g:vg_session_log_filename')
if use_session_log_file:
    log_file_handle = open(session_log_filename, "w+")

def write_to_log(log_string):
    if use_session_log_file:
        log_file_handle.write(log_string)
    vim.command("let g:vg_full_query_result = []")
    log_lines = Filter.filter_query_result(log_string, True)
    for log_line in log_lines:
        vim.command("call add(g:vg_full_query_result, '" + log_line + "' )")
    vim.command("call vg_display#check_update_session_log()")
