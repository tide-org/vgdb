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
        self.default_input_buffer_variable = Config().get()["settings"]["buffers"]["default_input_buffer_variable"]

    def set_command_handler(self, command_handler):
        self.cmd_hnd = command_handler

    def run_config_command(self, command, buffer_name=''):
        (base_command, command_args) = self.check_split_command(command)
        if self.is_command_in_config(base_command):
            self.set_user_input_args(command_args)
            config_command_list = Config().get()["commands"][base_command]["steps"]
            for config_command_item in config_command_list:
                ok_to_run = self.check_ok_to_run(config_command_item)
                if ok_to_run:
                    config_command_item = self.check_remove_metadata_keys(config_command_item)
                    self.run_config_command_action(config_command_item, buffer_name)

    def check_split_command(self, command):
        split_command = command.split(' ')
        if len(split_command) > 1:
            return (split_command[0], split_command[1:])
        return (command, [])

    def run_config_command_action(self, config_command_item, buffer_name):
        lines = []
        vim.command("let " + self.default_input_buffer_variable + " = []")
        command_action_name = list(config_command_item.keys())[0].lower()
        command_action = config_command_item[command_action_name]
        lines = Action.run_action(command_action_name, [command_action, buffer_name])
        if lines:
            self.add_lines_to_input_buffer(lines)

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

    def check_ok_to_run(self, config_command_item):
        when_condition = config_command_item.get("when", '')
        if when_condition:
            processed_when_condition = self.process_when_condition(when_condition)
            return eval(processed_when_condition)
        return True

    def set_user_input_args(self, command_args):
        if len(command_args) > 0:
            Config().get()["variables"]["user_input_args"] = " ".join(command_args)

    def process_when_condition(self, when_condition):
        variable_names = Config().get()["variables"].keys()
        for variable in variable_names:
            if variable in when_condition:
                when_condition = when_condition.replace(variable, str(Config().get()["variables"][variable]))
        return when_condition

    def add_lines_to_input_buffer(self, lines):
        if lines:
            for line in lines:
                vim.command("call add(" + self.default_input_buffer_variable + ", '" + line + "' )")

    def is_command_in_config(self, command):
        commands_list = Config().get()["commands"].keys()
        return command in commands_list
