import vim
import importlib
import sys

def filter_lines_for_buffer(lines, buffer_name):
    filtered_buffers = vim.eval('g:vg_filtered_buffers')
    if buffer_name.lower() in filtered_buffers:
        lines = call_filter_class(lines, buffer_name)
    return lines

def call_filter_class(lines, filter_name):
    filter_module = "filters." + filter_name
    buffer_filter = importlib.import_module(filter_module)
    buffer_filter = getattr(sys.modules[filter_module], filter_name)
    processor = buffer_filter(lines)
    return processor.processed_lines
