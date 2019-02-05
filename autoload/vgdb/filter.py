import vim
import importlib
import sys
import os
from os import listdir
from os.path import isfile, join
from config import Config
import plugin_helpers as plugins

filtered_buffers_list = []

def filter_lines_for_buffer(lines, buffer_name):
    __get_filtered_buffers_list()
    if buffer_name.lower() in filtered_buffers_list:
        lines = call_filter_class(lines, buffer_name)
    return lines

def __get_filtered_buffers_list():
    if not filtered_buffers_list:
        filters_path = plugins.resolve_plugin_path('filters')
        sys.path.insert(0, filters_path)
        filter_files = [f for f in listdir(filters_path) if isfile(join(filters_path, f))]
        for filter_file in filter_files:
            if filter_file[-3:].lower() == ".py" and filter_file.lower() != "__init__.py":
                filtered_buffers_list.append(filter_file[:-3])

def call_filter_class(lines, filter_name):
    __get_filtered_buffers_list()
    buffer_filter = importlib.import_module(filter_name)
    buffer_filter = getattr(sys.modules[filter_name], filter_name)
    processor = buffer_filter(lines)
    return processor.processed_lines
