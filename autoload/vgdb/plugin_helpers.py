import os
from os.path import abspath
from config import Config
import path_helpers as Ph

valid_plugin_names = ['filters', 'actions', 'functions']

def resolve_plugin_path(plugin_name):
    if plugin_name not in valid_plugin_names:
        raise RuntimeError("error: plugin name: " + plugin_name + " is invalid")
    plugin_settings = plugin_name + "_path"
    start_path = Config().get()["settings"]["plugins"][plugin_settings]
    if os.path.isdir(start_path):
        return abspath(start_path)
    base_path = Ph.get_vgdb_base_path()
    filters_path = os.path.join(base_path, start_path)
    if os.path.isdir(filters_path):
        return abspath(filters_path)
    raise RuntimeError("error: could not resolve " + plugin_settings + ": " + start_path)
