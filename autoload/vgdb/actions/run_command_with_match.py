from config import Config
from command_handler import CommandHandler
from action_predicate_base import action_predicate_base

class run_command_with_match(action_predicate_base):

    def run(self, command_item, buffer_name=''):
        command_item_command = command_item["command"]
        match = command_item["match"]
        match_result = CommandHandler().run_command_get_match(command_item_command, match)
        try_set_var = command_item.get("try_set", None)
        if try_set_var and match_result:
            Config().get()["variables"][try_set_var] = match_result

