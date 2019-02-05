from config import Config
import action as Action
from command_action import CommandAction

class ConfigCommandItem(object):

    def __init__(self):
        Action.get_actions_list()

    _command = ''

    _event_input_args = {}

    base_command = ''

    user_command_args = []

    command_action_name = ''

    config_command_item = {}

    buffer_name = ''

    @property
    def event_input_args(self):
        return self._event_input_args

    @event_input_args.setter
    def event_input_args(self, value):
        self._event_input_args = value

    event_input_args_name = ''

    args_dict = {}

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, value):
        split_command = value.split(' ')
        if len(split_command) > 1:
            self.base_command = split_command[0]
            self.user_command_args = split_command[1:]
        else:
            self.base_command = value
        self.__validate_command()
        self.__set_config_for_user_command_args()

    @property
    def command_action_list(self):
        cal = list(Config().get()["commands"][self.base_command]["steps"])
        ucal = []
        for command_action in cal:
            updated_command_action = command_action.copy()
            event_input_args = self.__get_event_input_args()
            if event_input_args:
                self.event_input_args = event_input_args
                updated_command_action["event_input_args"] = event_input_args
            ucal.append(CommandAction(updated_command_action))
        return ucal

    @property
    def command_action_names(self):
        command_action_names = []
        for config_command_action in Config().get()["commands"][self.base_command]["steps"]:
            command_action_name_set = set(config_command_action.keys()) & set(Action.actions_list)
            if len(command_action_name_set) == 1:
                command_action_names.append(list(command_action_name_set)[0])
        return command_action_names

    def __get_event_input_args(self):
        if self.base_command and self.buffer_name and self.event_input_args_name:
           args_dict = {}
           event_command_list = Config().get()["buffers"][self.buffer_name]["events"][self.event_input_args_name]
           for event_command in event_command_list:
               if event_command["command"] == self.base_command:
                   return event_command["input_args"]

    def __set_config_for_user_command_args(self):
        if len(self.user_command_args) > 0:
            Config().get()["variables"]["user_input_args"] = " ".join(self.user_command_args)

    def __validate_command(self):
        commands_list = Config().get()["commands"].keys()
        if not self.base_command in commands_list:
            raise RuntimeError("error: command " + self.base_command + " does not exist in config")

    def print_properties(self):
        print("ConfigCommandItem properties:")
        print("  command:               " + str(self.command))
        print("  base_command:          " + str(self.base_command))
        print("  user_commands:         " + str(self.user_command_args))
        print("  command_action_name:   " + str(self.command_action_name))
        print("  config_command_item:   " + str(self.config_command_item))
        print("  buffer_name:           " + str(self.buffer_name))
        print("  event_input_args:      " + str(self.event_input_args))
        print("  event_input_args_name: " + str(self.event_input_args_name))
        print("  args_dict:             " + str(self.args_dict))

