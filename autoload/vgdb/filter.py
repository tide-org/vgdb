import importlib
import sys
import os
from os import listdir
from os.path import isfile, join
import path_helpers as Ph
from logging_decorator import logging

FILTERED_BUFFERS_LIST = []

@logging
def filter_lines_for_buffer(lines, buffer_name):
    __get_filtered_buffers_list()
    if buffer_name.lower() in FILTERED_BUFFERS_LIST:
        lines = filter_string(lines, buffer_name)
    return lines

@logging
def filter_string(lines, filter_name):
    __get_filtered_buffers_list()
    if filter_name.lower() in FILTERED_BUFFERS_LIST:
        buffer_filter = __get_buffer_filter(filter_name)
        return buffer_filter(lines).processed_lines
    return lines

@logging
def __get_buffer_filter(filter_name):
    filter_paths = Ph.get_paths_for_plugin('filters')
    for filter_path in filter_paths:
        test_file_path = os.path.join(filter_path, filter_name + ".py")
        if os.path.isfile(test_file_path):
            sys.path.insert(0, filter_path)
            break
    importlib.import_module(filter_name)
    return getattr(sys.modules[filter_name], filter_name)

@logging
def __get_filtered_buffers_list():
    if not FILTERED_BUFFERS_LIST:
        filter_files = __get_files_from_path()
        __add_files_to_list(filter_files)

@logging
def __get_files_from_path():
    filter_paths = Ph.get_paths_for_plugin('filters')
    all_filter_files = []
    for filter_path in filter_paths:
        sys.path.insert(0, filter_path)
        all_filter_files.extend( [f for f in listdir(filter_path) if isfile(join(filter_path, f))] )
    print("aff: " + str(all_filter_files))
    return all_filter_files

@logging
def __add_files_to_list(filter_files):
    for filter_file in filter_files:
        if filter_file[-3:].lower() == ".py" and filter_file.lower() != "__init__.py":
            FILTERED_BUFFERS_LIST.append(filter_file[:-3])
