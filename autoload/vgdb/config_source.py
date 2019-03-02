import os
from os.path import abspath
import path_helpers as Ph
from yamlreader import yaml_load

_config_path = "config"
_config_location_file = "config_location.yaml"
_config_location_variable = "config_location"
_config_defaults_file = "default_config.yaml"
_config_environment_variable ="VGDB_CONFIG_LOCATION"

def __get_config_location_from_environment_variable():
    config_location = os.environ.get(_config_environment_variable)
    if config_location:
        if os.path.isdir(config_location):
            return abspath(config_location)
        base_path = Ph.get_python_scripts_base_path()
        path_from_scripts = os.path.join(base_path, config_location)
        if path_from_scripts and os.path.isdir(path_from_scripts):
            return abspath(path_from_scripts)

def __get_config_location_from_default_location_file():
    base_path = Ph.get_python_scripts_base_path()
    config_location_location = os.path.join(base_path, _config_path, _config_location_file)
    location_config = yaml_load(config_location_location)
    config_location = location_config[_config_location_variable]
    if config_location:
        full_config_location = os.path.join(base_path, config_location)
        if os.path.isdir(full_config_location):
            return abspath(full_config_location)

def __get_base_config_location():
    environment_config_path = __get_config_location_from_environment_variable()
    if environment_config_path:
        return environment_config_path
    location_file_path = __get_config_location_from_default_location_file()
    if location_file_path:
        return location_file_path
    raise RuntimeError("error: unable to find a matching path for the config. please either set the environment variable VGDB_CONFIG_LOCATION or specify in the file config_location.yaml")

def __get_default_config_path():
    base_path = Ph.get_python_scripts_base_path()
    return os.path.join(base_path, _config_path, _config_defaults_file)

def __get_default_config():
    default_config = __get_default_config_path()
    return yaml_load(default_config)

def __get_single_config(path):
    return yaml_load(path)

def __get_all_configs():
    full_config = {}
    for config_path in CONFIG_LOCATION_ARRAY:
        if not full_config:
            full_config = __get_single_config(config_path)
        else:
            full_config = yaml_load(config_path, full_config)
    return full_config

def __get_config_path_from_settings(current_config):
    if not current_config:
        return ''
    settings = current_config.get("settings", "")
    if not settings:
        return ''
    plugins = settings.get("plugins", "")
    if not plugins:
        return ''
    config_path = plugins.get("config_path", "")
    if not config_path:
        return ''
    return config_path

def __get_all_config_locations():
    config_locations = []
    config_path = ''
    base_config_path = FULL_CONFIG_LOCATION
    current_config = __get_single_config(base_config_path)
    while True:
        temp_config_path = os.path.join(base_config_path, config_path)
        if os.path.isdir(config_path):
            temp_config_path = config_path
        if os.path.isdir(temp_config_path):
            config_locations.append(abspath(temp_config_path))
            current_config = __get_single_config(temp_config_path)
            config_path = __get_config_path_from_settings(current_config)
            if not config_path:
                break
            base_config_path = temp_config_path
        else:
            break
    config_locations.append(__get_default_config_path())
    return config_locations[::-1]

FULL_CONFIG_LOCATION = __get_base_config_location()

CONFIG_LOCATION_ARRAY = __get_all_config_locations()

CONFIG_OBJECT = __get_all_configs()
