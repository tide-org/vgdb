import vim
from singleton import singleton
from config import Config
import action as Action
from config_command_item import ConfigCommandItem

@singleton
class ConfigCommand(object):

    metadata_dict_keys = [ 'when' ]

    def run_config_command(self, cci):
        for command_action in cci.command_action_list:
            command_action_type = next(iter(command_action))
            command_action_value = next(iter(command_action.values()))
            if self.is_ok_to_run(command_action_value):
                self.initialise_buffer(cci.buffer_name)
                event_input_args = command_action.get("event_input_args", "")
                action_args = {
                        "command_item": command_action_value,
                        "buffer_name": cci.buffer_name
                }
                if event_input_args:
                    action_args["command_item"]["event_input_args"] = event_input_args
                if cci.args_dict:
                    action_args["command_args"] = cci.args_dict
                lines = Action.run_action(command_action_type, action_args)
                self.set_buffer_lines(lines, cci.buffer_name, command_action_type, command_action)

    def is_ok_to_run(self, command_action):
        when_condition = command_action.get("when", '')
        if when_condition:
            try:
                eval_when_condition = eval(self.process_when_condition(when_condition))
            except SyntaxError:
                return False
            return eval_when_condition
        return True

    def process_when_condition(self, when_condition):
        variable_names = Config().get()["variables"].keys()
        for variable in variable_names:
            if variable in when_condition:
                config_variable = str(Config().get()["variables"][variable])
                if " " in config_variable:
                    config_variable = "'" + config_variable + "'"
                when_condition = when_condition.replace(variable, config_variable)
        return when_condition

    def initialise_buffer(self, buffer_name):
        if buffer_name not in Config().get()["internal"]["buffer_caches"]:
            Config().get()["internal"]["buffer_caches"][buffer_name] = []

    def set_buffer_lines(self, lines, buffer_name, command_action_name, command_action):
        if lines:
            if buffer_name == '':
                lines.insert(0, "no buffer name. command_action_name: " + command_action_name + " command_action: " + str(command_action) )
                internal_buffer_name = 'default'
            else:
                internal_buffer_name = buffer_name
            Config().get()["internal"]["buffer_caches"][internal_buffer_name] = lines
