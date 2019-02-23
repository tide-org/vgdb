import os
from os.path import abspath
import path_helpers as Ph
from yamlreader import yaml_load

def __get_config_location_from_environment_variable():
    config_location = os.environ.get("VGDB_CONFIG_LOCATION")
    if config_location:
        if os.path.isdir(config_location):
            return abspath(config_location)
        base_path = Ph.get_python_scripts_base_path()
        path_from_scripts = os.path.join(base_path, config_location)
        if path_from_scripts and os.path.isdir(path_from_scripts):
            return abspath(path_from_scripts)

def __get_config_location_from_default_location_file():
    base_path = Ph.get_python_scripts_base_path()
    config_location_location = os.path.join(base_path, "yaml", "config_location.yaml")
    location_config = yaml_load(config_location_location)
    config_location = location_config["config_location"]
    if config_location:
        full_config_location = os.path.join(base_path, config_location)
        if os.path.isdir(full_config_location):
            return abspath(full_config_location)

def __get_config_location():
    environment_config_path = __get_config_location_from_environment_variable()
    if environment_config_path:
        return environment_config_path
    location_file_path = __get_config_location_from_default_location_file()
    if location_file_path:
        return location_file_path
    raise RuntimeError("error: unable to find a matching path for the config. please either set the environment variable VGDB_CONFIG_LOCATION or specify in the file config_location.yaml")

def __get_default_config():
    base_path = Ph.get_python_scripts_base_path()
    default_config = os.path.join(base_path, "yaml", "default_config.yaml")
    return yaml_load(default_config)

def __get_all_configs():
    default_config = __get_default_config()
    full_template_location = __get_config_location()
    return yaml_load(full_template_location, default_config)

CONFIG_OBJECT = __get_all_configs()
