import os
from os.path import abspath

VALID_PLUGIN_NAMES = [
    'actions',
    'config',
    'editor_wrappers',
    'filters',
    'functions',
    'templates'
]

def resolve_plugin_path(plugin_name):
    validate_plugin_name(plugin_name)
    start_path = get_start_path(plugin_name)
    if os.path.isdir(start_path):
        return abspath(start_path)
    plugin_path = get_plugin_path(start_path)
    if os.path.isdir(plugin_path):
        return abspath(plugin_path)
    raise RuntimeError("error: could not resolve " + plugin_name + ": " + start_path)

def validate_plugin_name(plugin_name):
    if plugin_name not in VALID_PLUGIN_NAMES:
        raise RuntimeError("error: plugin name: " + plugin_name + " is invalid")

def get_start_path(plugin_name):
    import config_source as Cs
    plugin_settings = plugin_name + "_path"
    return Cs.CONFIG_OBJECT["settings"]["plugins"][plugin_settings]

def get_plugin_path(start_path):
    import config_source as Cs
    return os.path.join(Cs.FULL_CONFIG_LOCATION, start_path)

def get_vgdb_base_path():
    join_paths = get_python_scripts_base_path(), "..", ".."
    return os.path.join(*join_paths)

def get_python_scripts_base_path():
    return os.path.dirname(os.path.realpath(__file__))
