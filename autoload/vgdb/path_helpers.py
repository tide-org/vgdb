import os
from os.path import abspath

VALID_PLUGIN_NAMES = [
    'filters',
    'actions',
    'functions',
    'editor_wrappers'
]

def resolve_plugin_path(plugin_name):
    validate_plugin_name(plugin_name)
    start_path = get_start_path(plugin_name)
    if os.path.isdir(start_path):
        return abspath(start_path)
    filters_path = get_filters_path(start_path)
    if os.path.isdir(filters_path):
        return abspath(filters_path)
    raise RuntimeError("error: could not resolve " + plugin_name + ": " + start_path)

def validate_plugin_name(plugin_name):
    if plugin_name not in VALID_PLUGIN_NAMES:
        raise RuntimeError("error: plugin name: " + plugin_name + " is invalid")

def get_start_path(plugin_name):
    from config import Config
    plugin_settings = plugin_name + "_path"
    return Config().get()["settings"]["plugins"][plugin_settings]

def get_filters_path(start_path):
    base_path = get_vgdb_base_path()
    return os.path.join(base_path, start_path)

def get_vgdb_base_path():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    join_paths = script_dir, "..", ".."
    return os.path.join(*join_paths)

def get_python_scripts_base_path():
    return os.path.dirname(os.path.realpath(__file__))
