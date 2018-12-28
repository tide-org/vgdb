import vim
import os
from config import Config
import plugin_helpers as Plugins
from action_predicate_base import action_predicate_base

class set_var(action_predicate_base):

    def run(self, command_item, buffer_name=''):
        value = command_item.get("value", '')
        interpolated_value = self.interpolate_variables(value)
        name = command_item.get("name", '')
        if name:
            Config().get()["variables"][name] = interpolated_value

    def interpolate_variables(self, msg):
        variable_names = Config().get()["variables"].keys()
        for variable in variable_names:
            moustache_variable = "{{ " + variable + " }}"
            if moustache_variable in msg:
                msg = msg.replace(moustache_variable, str(Config().get()["variables"][variable]))
        return msg
