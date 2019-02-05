from config import Config

class CommandAction(object):

    _command_action = {}

    def __init__(self, value):
        self._command_action = value

    @property
    def command_action(self):
        return self._command_action

    @command_action.setter
    def command_action(self, value):
        self._command_action = value

    def is_ok_to_run(self):
        when_condition = self.__get_when_condition()
        if when_condition:
            try:
                eval_when_condition = eval(self.__process_when_condition(when_condition))
            except SyntaxError:
                return False
            return eval_when_condition
        return True

    def __get_when_condition(self):
        command_action_value = next(iter(self._command_action.values()))
        return command_action_value.get("when", '')

    def __process_when_condition(self, when_condition):
        variable_names = Config().get()["variables"].keys()
        for variable in variable_names:
            if variable in when_condition:
                config_variable = str(Config().get()["variables"][variable])
                if " " in config_variable:
                    config_variable = "'" + config_variable + "'"
                when_condition = when_condition.replace(variable, config_variable)
        return when_condition

    def get_action_args(self, buffer_name, args_dict):
        command_action_value = next(iter(self._command_action.values()))
        event_input_args = self._command_action.get("event_input_args", "")
        action_args = {
                "command_item": command_action_value,
                "buffer_name": buffer_name
        }
        if event_input_args:
            action_args["command_item"]["event_input_args"] = event_input_args
        if args_dict:
            action_args["command_args"] = args_dict
        return action_args

    @property
    def type(self):
        return next(iter(self._command_action))

