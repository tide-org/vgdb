import yaml
import os
import re
import sys
import codecs
from yamlreader import yaml_load
from singleton import singleton
from actionable_dict import ActionableDict
import path_helpers as Ph
from editor_wrapper import EditorWrapper
import vim

@singleton
class Config:

    _config_dictionary = None

    _editor_wrapper = None

    def __init__(self):
        if not self._config_dictionary:
            self.set()

    def get(self):
        return self._config_dictionary

    def set(self, force=False):
        if force or not self._config_dictionary:
            full_template_location = self.__get_full_template_location()
            config = self.__get_all_configs(full_template_location)
            self._config_dictionary = ActionableDict(config, self._editor_wrapper.set_dictionary_value)
            self.__set_editor_dictionary_defaults()
            self.__set_internals()

    def __set_editor_wrapper(self):
        editor = self._config_dictionary["settings"]["editor"]["name"]
        self._editor_wrapper = EditorWrapper(editor)

    def __get_all_configs(self, full_template_location):
        config = yaml_load(full_template_location)
        return config

    def __get_full_template_location(self):
        template_location = self._editor_wrapper.get_template_location()
        base_path = Ph.get_vgdb_base_path()
        full_template_location = os.path.join(base_path, template_location)
        return full_template_location

    def __set_editor_dictionary_defaults(self):
        self._editor_wrapper.set_editor_dictionary(self._config_dictionary)

    def __set_internals(self):
        session_log_buffer = self._config_dictionary["settings"]["logging"]["session_buffer_name"]
        self._config_dictionary["internal"] = { "buffer_caches": { session_log_buffer: [] }, "variables": {} }
