import vim
from singleton import singleton
from config import Config
import os
import importlib
import sys
import plugin_helpers as Plugins
import action as Action

@singleton
class ConfigCommand(object):

    cmd_hnd = None
    metadata_dict_keys = [ 'when' ]

    def __init__(self):
        Action.get_actions_list()
        self.control_chars = [chr(c) for c in range(0x20)]

    def set_command_handler(self, command_handler):
        self.cmd_hnd = command_handler

    def run_config_command(self, command, buffer_name=''):
        (base_command, command_args) = self.check_split_command(command)
        if self.is_command_in_config(base_command):
            self.set_user_input_args(command_args)
            config_command_list = Config().get()["commands"][base_command]["steps"]
            for config_command_item in config_command_list:

                command_action_name_set = set(config_command_item.keys()) & set(Action.actions_list)
                if len(command_action_name_set) == 1:
                    command_action_name = list(command_action_name_set)[0]
                    command_action = config_command_item[command_action_name]
                    ok_to_run = self.check_ok_to_run(config_command_item)
                    if ok_to_run:
                        self.run_config_command_action(command_action_name, command_action, buffer_name)

    def check_ok_to_run(self, config_command_item):
        when_condition = config_command_item.get("when", '')
        if when_condition:
            processed_when_condition = self.process_when_condition(when_condition)
            eval_when_condition = eval(processed_when_condition)
            return eval_when_condition
        return True

    def process_when_condition(self, when_condition):
        variable_names = Config().get()["variables"].keys()
        for variable in variable_names:
            if variable in when_condition:
                config_variable = str(Config().get()["variables"][variable])
                if " " in config_variable:
                    config_variable = "'" + config_variable + "'"
                when_condition = when_condition.replace(variable, config_variable)
        return when_condition

    def check_split_command(self, command):
        split_command = command.split(' ')
        if len(split_command) > 1:
            return (split_command[0], split_command[1:])
        return (command, [])

    def run_config_command_action(self, command_action_name, command_action, buffer_name):
        lines = []
        if buffer_name == '':
            internal_buffer_name = 'default'
        else:
            internal_buffer_name = buffer_name
        Config().get()["internal"]["buffer_caches"][internal_buffer_name] = []
        lines = Action.run_action(command_action_name, [command_action, buffer_name])
        if lines:
            self.add_lines_to_input_buffer(lines, internal_buffer_name)

    def check_remove_metadata_keys(self, config_command_item):
        new_dict = config_command_item
        for meta_dict_key in self.metadata_dict_keys:
            if meta_dict_key in config_command_item:
                new_dict = self.remove_meta_dict_key(config_command_item, meta_dict_key)
        return new_dict

    def remove_meta_dict_key(self, original_dict, dict_key):
        new_dict = dict(original_dict)
        del new_dict[dict_key]
        return new_dict

    def set_user_input_args(self, command_args):
        if len(command_args) > 0:
            Config().get()["variables"]["user_input_args"] = " ".join(command_args)

    def add_lines_to_input_buffer(self, lines, internal_buffer_name):
        if lines:
            Config().get()["internal"]["buffer_caches"][internal_buffer_name] = lines

    def is_command_in_config(self, command):
        commands_list = Config().get()["commands"].keys()
        return command in commands_list
