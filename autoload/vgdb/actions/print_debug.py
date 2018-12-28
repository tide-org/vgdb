import vim
import os
from config import Config
import plugin_helpers as Plugins
from action_predicate_base import action_predicate_base

class print_debug(action_predicate_base):

    def run(self, command_item, buffer_name=''):
        msg = command_item.get("msg", '')
        interpolated_message = self.interpolate_variables(msg)
        print_buffer_name = command_item.get("buffer_name", 0)
        if print_buffer_name:
            print("print_debug - buffer name: " + buffer_name)
        print("print_debug - " + str(interpolated_message))

    def interpolate_variables(self, msg):
        variable_names = Config().get()["variables"].keys()
        for variable in variable_names:
            moustache_variable = "{{ " + variable + " }}"
            if moustache_variable in msg:
                msg = msg.replace(moustache_variable, str(Config().get()["variables"][variable]))
        return msg

