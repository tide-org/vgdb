from config import Config
import action as Action

class ConfigCommandItem(object):

    _command = ''

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
        print("cci cal:" + str(cal))
        print("bc:" + str(self.base_command))
        ucal = []
        for command_action in cal:
            updated_command_action = command_action.copy()
            event_input_args = self.__get_event_input_args(self.command, self.buffer_name, self.event_input_args_name)
            if event_input_args:
                updated_command_action["event_input_args"] = event_input_args
            ucal.append(updated_command_action)
        return ucal

    def __get_event_input_args(self, command, buffer_name, event_input_args_name):
        if command and buffer_name and event_input_args_name:
           args_dict = {}
           event_command_list = Config().get()["buffers"][buffer_name]["events"][event_input_args_name]
           for event_command in event_command_list:
               if event_command["command"] == command:
                   return event_command["input_args"]

    @property
    def command_action_names(self):
        command_action_names = []
        for config_command_action in Config().get()["commands"][self.base_command]["steps"]:
            command_action_name_set = set(config_command_action.keys()) & set(Action.actions_list)
            if len(command_action_name_set) == 1:
                command_action_names.append(list(command_action_name_set)[0])
        return command_action_names

    base_command = ''

    user_command_args = []

    command_action_name = ''

    config_command_item = {}

    buffer_name = ''

    event_input_args = ''

    event_input_args_name = ''

    args_dict = {}

    def __set_config_for_user_command_args(self):
        if len(self.user_command_args) > 0:
            Config().get()["variables"]["user_input_args"] = " ".join(self.user_command_args)

    def __validate_command(self):
        commands_list = Config().get()["commands"].keys()
        if not self.base_command in commands_list:
            raise RuntimeError("error: command " + self.base_command + " does not exist in config")
