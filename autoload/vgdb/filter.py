import importlib
import sys
from os import listdir
from os.path import isfile, join
import path_helpers as PathHelpers

FILTERED_BUFFERS_LIST = []

def filter_lines_for_buffer(lines, buffer_name):
    __get_filtered_buffers_list()
    if buffer_name.lower() in FILTERED_BUFFERS_LIST:
        lines = filter_string(lines, buffer_name)
    return lines

def filter_string(lines, filter_name):
    __get_filtered_buffers_list()
    buffer_filter = __get_buffer_filter(filter_name)
    return buffer_filter(lines).processed_lines

def __get_buffer_filter(filter_name):
    importlib.import_module(filter_name)
    return getattr(sys.modules[filter_name], filter_name)

def __get_filtered_buffers_list():
    if not FILTERED_BUFFERS_LIST:
        filter_files = __get_files_from_path()
        __add_files_to_list(filter_files)

def __get_files_from_path():
    filters_path = PathHelpers.resolve_plugin_path('filters')
    sys.path.insert(0, filters_path)
    return [f for f in listdir(filters_path) if isfile(join(filters_path, f))]

def __add_files_to_list(filter_files):
    for filter_file in filter_files:
        if filter_file[-3:].lower() == ".py" and filter_file.lower() != "__init__.py":
            FILTERED_BUFFERS_LIST.append(filter_file[:-3])
