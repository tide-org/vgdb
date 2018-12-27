import vim
import os
from config import Config
import plugin_helpers as Plugins
from action_predicate_base import action_predicate_base

class set_var(action_predicate_base):

    def run(self, command_item, buffer_name=''):
        value = command_item.get("value", '')
        name = command_item.get("name", '')
        if name:
            Config().get()["variables"][name] = value
