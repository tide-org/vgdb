import yaml
import vim
import os
import re
import codecs
from singleton import singleton
from actionable_dict import ActionableDict

@singleton
class Config:

    __config_dictionary = None

    def __init__(self):
        if not self.__config_dictionary:
            self.set()

    def get(self):
        return self.__config_dictionary

    def set(self, force=False):
        if force or self.__config_dictionary == None:
            full_template_location = self.__get_full_template_location()
            with codecs.open(full_template_location, encoding='utf-8') as ymlfile:
                ymlstring = ymlfile.read()
                config = yaml.load(ymlstring)
                self.__config_dictionary = ActionableDict(config, self.callback_set_vim_key_value)
                self.__set_vim_globals()
                self.__set_internals()

    @staticmethod
    def callback_set_vim_key_value(parent_keys, value):
        let_string = "let g:vg_config_dictionary"
        for key in parent_keys:
            let_string += "['" + key + "']"
        string_value = str(value).replace(
                "True", "'True'").replace(
                "False", "'False'").replace(
                "None", "'None'").replace(
                ": False", ": 'False'").replace(
                ": True", ": 'True'").replace(
                ": None", ": 'None'").replace(
                "\\\'", "\\\'\'")
        if isinstance(value, str):
            string_value = "'" + string_value + "'"
        let_string += " = " + string_value
        vim.command(let_string)

    def __string_replace_for_vim(self, string_to_replace):
        return str(string_to_replace).replace(
                ": False", ": 'False'").replace(
                ": True", ": 'True'").replace(
                ": None", ": 'None'")

    def __get_full_template_location(self):
        template_location = vim.eval("g:vg_config_location")
        full_template_location =  os.path.join(os.getcwd(), template_location)
        return full_template_location

    def __set_vim_globals(self):
        config_string = self.__string_replace_for_vim(self.__config_dictionary)
        vim.command("let g:vg_config_dictionary = " + config_string)

    def __set_internals(self):
        session_log_buffer = self.__config_dictionary["settings"]["logging"]["session_buffer_name"]
        self.__config_dictionary["internal"] = {"buffer_caches": { session_log_buffer: [] }, "variables": {}}
