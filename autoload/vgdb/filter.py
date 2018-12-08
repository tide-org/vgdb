import vim
import importlib
import sys
import os
from os import listdir
from os.path import isfile, join

filtered_buffers_list = []

def filter_lines_for_buffer(lines, buffer_name):
    get_filtered_buffers_list()
    if buffer_name.lower() in filtered_buffers_list:
        lines = call_filter_class(lines, buffer_name)
    return lines

def get_filtered_buffers_list():
    if len(filtered_buffers_list) == 0:
        script_path = os.path.dirname(os.path.realpath(__file__))
        filters_path = os.path.join(script_path, "filters")
        filter_files = [f for f in listdir(filters_path) if isfile(join(filters_path, f))]
        for filter_file in filter_files:
            if filter_file[-3:].lower() == ".py" and filter_file.lower() != "__init__.py":
                filtered_buffers_list.append(filter_file[:-3])

def call_filter_class(lines, filter_name):
    filter_module = "filters." + filter_name
    buffer_filter = importlib.import_module(filter_module)
    buffer_filter = getattr(sys.modules[filter_module], filter_name)
    processor = buffer_filter(lines)
    return processor.processed_lines
