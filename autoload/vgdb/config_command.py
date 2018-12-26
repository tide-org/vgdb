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

    variable_dictionary = {}
    cmd_hnd = None

    def __init__(self):
        self.default_input_buffer_variable = Config().get()["settings"]["buffers"]["default_input_buffer_variable"]

    def set_command_handler(self, command_handler):
        self.cmd_hnd = command_handler

    def run_config_command(self, command, buffer_name=''):
        if self.is_command_in_config(command):
            commands_list = Config().get()["commands"][command]["steps"]
            for command_item in commands_list:
                when_condition = command_item.get("when", '')
                ok_to_run = True
                if when_condition:
                    processed_when_condition = self.process_when_condition(when_condition)
                    ok_to_run = eval(processed_when_condition)
                if ok_to_run:
                    lines = []
                    vim.command("let " + self.default_input_buffer_variable + " = []")
                    command_action = command_item["action"].lower()
                    lines = Action.run_action(command_action, [command_item, buffer_name])
                    if lines:
                        self.add_lines_to_input_buffer(lines)

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
        commands_dict = Config().get()["commands"].get(command, None)
        return commands_dict != None
