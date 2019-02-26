import importlib
import sys
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
from logging_decorator import logging

@logging
def __get_actions_list():
    actions_list = []
    actions_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "actions")
    action_files = [f for f in listdir(actions_path) if isfile(join(actions_path, f))]
    for action_file in action_files:
        if Path(action_file).suffix.lower() == ".py" and action_file.lower() != "__init__.py":
            actions_list.append(Path(action_file).stem.lower())
    return actions_list

ACTIONS_LIST = __get_actions_list()

@logging
def run_action(action_name, args_dict):
    if action_name.lower() in ACTIONS_LIST:
        return __call_action_class(action_name, args_dict)
    else:
        raise TypeError("error: action: " + action_name + " is not a valid action")

@logging
def __call_action_class(action_name, args_dict):
    action_module = "actions." + action_name
    importlib.import_module(action_module)
    action = getattr(sys.modules[action_module], action_name)
    return action().run(**args_dict)
