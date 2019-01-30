from config import Config
from action_base import action_base

class create_interpolated_string(action_base):

    def run(self, command_item, buffer_name=''):
        variable_name = command_item["variable_name"]
        string_value = command_item["value"]
        args = command_item["args"]
        resolved_args = []
        for arg in args:
            resolved_args.append(Config().get()["variables"][arg])
        result_string = string_value.format(*resolved_args)
        Config().get()["variables"][variable_name] = result_string
