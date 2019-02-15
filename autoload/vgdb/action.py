import importlib
import sys
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
from logging_decorator import logging

ACTIONS_LIST = []

@logging
def run_action(action_name, args_dict):
    get_actions_list()
    if action_name.lower() in ACTIONS_LIST:
        return __call_action_class(action_name, args_dict)
    else:
        raise TypeError("error: action: " + action_name + " is not a valid action")

@logging
def get_actions_list():
    if not ACTIONS_LIST:
        script_path = os.path.dirname(os.path.realpath(__file__))
        actions_path = os.path.join(script_path, "actions")
        action_files = [f for f in listdir(actions_path) if isfile(join(actions_path, f))]
        for action_file in action_files:
            if Path(action_file).suffix.lower() == ".py" and action_file.lower() != "__init__.py":
                ACTIONS_LIST.append(Path(action_file).stem.lower())
    return ACTIONS_LIST

@logging
def __call_action_class(action_name, args_dict):
    action_module = "actions." + action_name
    importlib.import_module(action_module)
    action = getattr(sys.modules[action_module], action_name)
    return action().run(**args_dict)
