import re
from config import Config
from command_handler import CommandHandler
from action_predicate_base import action_predicate_base

class run_command_with_match(action_predicate_base):

    def run(self, command_item, buffer_name=''):
        command_item_command = command_item["command"]
        regex_match = command_item["match"]
        lines = CommandHandler().run_command(command_item_command)
        match_result = self.get_match(regex_match, lines)
        try_set_var = command_item.get("try_set", None)
        if try_set_var and match_result:
            Config().get()["variables"][try_set_var] = match_result

    def get_match(self, regex_match, lines):
        match_string = None
        for line in lines:
            if re.search(regex_match, line):
                match = re.search(regex_match, line)
                match_string = match.group()
        return match_string
