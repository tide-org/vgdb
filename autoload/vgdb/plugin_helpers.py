import os
from os.path import abspath
from config import Config

valid_plugin_names = ['filters', 'actions', 'functions']

def resolve_plugin_path(plugin_name):
    if plugin_name not in valid_plugin_names:
        raise RuntimeError("error: plugin name: " + plugin_name + " is invalid")
    plugin_settings = plugin_name + "_path"
    start_path = Config().get()["settings"]["plugins"][plugin_settings]
    if os.path.isdir(start_path):
        return abspath(start_path)
    script_path = os.path.dirname(os.path.realpath(__file__))
    vgdb_path = os.path.join(script_path, "/../..")
    filters_path = os.path.join(vgdb_path, start_path)
    if os.path.isdir(filters_path):
        return abspath(filters_path)
    raise RuntimeError("error: could not resolve " + plugin_settings + ": " + start_path)
