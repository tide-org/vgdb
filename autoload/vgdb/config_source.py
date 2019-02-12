import os
import path_helpers as Ph
from yamlreader import yaml_load

def __get_config_location():
    base_path = Ph.get_python_scripts_base_path()
    config_location_location = os.path.join(base_path, "config_location.yaml")
    location_config = yaml_load(config_location_location)
    config_location = location_config["config_location"]
    full_config_location = os.path.join(base_path, config_location)
    return full_config_location

def __get_all_configs():
    full_template_location = __get_config_location()
    return yaml_load(full_template_location)

CONFIG_OBJECT = __get_all_configs()
