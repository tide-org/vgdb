import vim
from singleton import singleton
from config import Config
import action as Action
from config_command_item import ConfigCommandItem

@singleton
class ConfigCommand(object):

    metadata_dict_keys = [ 'when' ]

    def run_config_command(self, cci):
        print("HERE4")
        cci.print_properties()
        print("HERE5")
        for command_action in cci.command_action_list:
            print("CA: " + str(command_action))
            print("HERE6")
            command_action_type = next(iter(command_action))
            command_action_value = next(iter(command_action.values()))
            print("CAT: " + str(command_action_type))
            print("CAV: " + str(command_action_value))
            if self.is_ok_to_run(command_action_value):
                print("HERE7")
                self.initialise_buffer(cci.buffer_name)
                print("HERE8")
                action_args = {
                        "command_item": command_action,
                        "buffer_name": cci.buffer_name
                }
                #command_action["command_item"] = command_action_value
                #command_action["command_name"] = cci.base_command
                #command_action["buffer_name"] = cci.buffer_name
                #command_action["command_args"] = cci.args_dict
                if cci.args_dict:
                    print("HERE9")
                    action_args["command_args"] = cci.args_dict
                print("HERE10")
                print("ActionArgs: " + str(action_args))
                lines = Action.run_action(command_action_type, action_args)
                print("HERE11")
                self.set_buffer_lines(lines, cci.buffer_name, command_action_type, command_action)
                print("HERE12")
        cci.print_properties()

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
