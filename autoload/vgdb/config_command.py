import vim
from singleton import singleton
from config import Config
import os
import importlib
import sys
import plugin_helpers as Plugins
import action as Action
import config_command_user as ccu

@singleton
class ConfigCommand(object):

    cmd_hnd = None
    metadata_dict_keys = [ 'when' ]

    def __init__(self):
        Action.get_actions_list()
        self.control_chars = [chr(c) for c in range(0x20)]

    def set_command_handler(self, command_handler):
        self.cmd_hnd = command_handler

    def run_config_command(self, command, buffer_name='', event_input_args_name=''):
        (base_command, command_args) = ccu.check_split_command(command)
        if self.is_command_in_config(base_command):
            ccu.set_user_input_args(command_args)
            config_command_list = Config().get()["commands"][base_command]["steps"]
            for config_command_item in config_command_list:
                command_action_name_set = set(config_command_item.keys()) & set(Action.actions_list)
                if len(command_action_name_set) == 1:
                    command_action_name = list(command_action_name_set)[0]
                    command_action = config_command_item[command_action_name]
                    updated_command_action = command_action.copy()
                    event_input_args = self.get_event_input_args(command, buffer_name, event_input_args_name)
                    if event_input_args:
                        updated_command_action["event_input_args"] = event_input_args
                    ok_to_run = self.check_ok_to_run(config_command_item)
                    if ok_to_run:
                        self.run_config_command_action(command_action_name, updated_command_action, buffer_name)

    def get_event_input_args(self, command, buffer_name, event_input_args_name):
        if command and buffer_name and event_input_args_name:
           args_dict = {}
           event_command_list = Config().get()["buffers"][buffer_name]["events"][event_input_args_name]
           for event_command in event_command_list:
               if event_command["command"] == command:
                   return event_command["input_args"]

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

    def run_config_command_action(self, command_action_name, command_action, buffer_name):
        lines = []
        if not Config().get()["internal"]["buffer_caches"].get(buffer_name, None):
            Config().get()["internal"]["buffer_caches"][buffer_name] = []
        lines = Action.run_action(command_action_name, [command_action, buffer_name])
        if lines:
            if buffer_name == '':
                lines.insert(0, "no buffer name. command_action_name: " + command_action_name + " command_action: " + str(command_action) )
                internal_buffer_name = 'default'
            else:
                internal_buffer_name = buffer_name
            self.add_lines_to_input_buffer(lines, internal_buffer_name)

    def add_lines_to_input_buffer(self, lines, internal_buffer_name):
        if lines:
            Config().get()["internal"]["buffer_caches"][internal_buffer_name] = lines

    def is_command_in_config(self, command):
        commands_list = Config().get()["commands"].keys()
        return command in commands_list
