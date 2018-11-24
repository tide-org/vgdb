import vim
import importlib
import sys

def filter_query_result(buffer_result, keep_all=False):
    lines_to_keep = []
    lines =  buffer_result.replace("\r","").replace("'", "''").replace("\\t", "    ").split("\n")
    for line in lines:
        if line.startswith('~"') or keep_all:
            lines_to_keep.append(line.lstrip('~"').rstrip('\\n"'))
    return lines_to_keep

def filter_lines_for_buffer(lines, buffer_name):
    filtered_buffers = vim.eval('g:vg_filtered_buffers')
    if buffer_name.lower() in filtered_buffers:
        filter_module = "filters." + buffer_name
        buffer_filter = importlib.import_module(filter_module)
        buffer_filter = getattr(sys.modules[filter_module], buffer_name)
        processor = buffer_filter(lines)
        lines = processor.processed_lines
    return lines
