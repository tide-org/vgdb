from config import Config
from action_base import action_base
import interpolate as Interpolate

class set_var(action_base):

    def run(self, command_item, buffer_name=''):
        value = command_item.get("value", '')
        interpolated_value = Interpolate.interpolate_variables(value)
        name = command_item.get("name", '')
        if name:
            Config().get()["variables"][name] = interpolated_value
