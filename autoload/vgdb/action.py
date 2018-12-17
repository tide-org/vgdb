import vim
import importlib
import sys
import os
from os import listdir
from os.path import isfile, join

actions_list = []

def run_action(action_dict, action_name):
    get_actions_list()
    if action_name.lower() in actions_list:
        call_action_class(action_dict, action_name)

def get_actions_list():
    if len(actions_list) == 0:
        script_path = os.path.dirname(os.path.realpath(__file__))
        actions_path = os.path.join(script_path, "actions")
        action_files = [f for f in listdir(actions_path) if isfile(join(actions_path, f))]
        for action_file in action_files:
            if action_file[-3:].lower() == ".py" and action_file.lower() != "__init__.py":
                actions_list.append(actions_file[:-3])

def call_action_class(action_dict, action_name):
    action_module = "actions." + action_name
    action = importlib.import_module(action_module)
    action = getattr(sys.modules[action_module], action_name)
    action(action_dict)
    action.run()
