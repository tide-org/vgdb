import os
from yamlreader import yaml_load
from singleton import singleton
from actionable_dict import ActionableDict
import path_helpers as Ph
from editor_wrapper import EditorWrapper

@singleton
class Config:

    _config_dictionary = None

    _editor_wrapper = None

    def __initialise_objects(self):
        self.__set_config_dictionary()

    def __set_config_dictionary(self):
        if not self._config_dictionary:
            self.set()

    def __set_editor_wrapper(self, editor):
        if not self._editor_wrapper:
            self._editor_wrapper = EditorWrapper(editor)

    def get(self):
        if not self._config_dictionary:
            self.__initialise_objects()
        return self._config_dictionary

    def set(self, force=False):
        if force or not self._config_dictionary:
            full_template_location = self.__get_config_location()
            config = self.__get_all_configs(full_template_location)
            editor = config["settings"]["editor"]["name"]
            self.__set_editor_wrapper(editor)
            callback = self._editor_wrapper.get_set_dictionary_value_callback()
            self._config_dictionary = ActionableDict(config, callback)
            self.__set_editor_dictionary_defaults()
            self.__set_internals()

    def __get_all_configs(self, full_template_location):
        config = yaml_load(full_template_location)
        return config

    def __get_config_location(self):
        base_path = Ph.get_python_scripts_base_path()
        config_location_location = os.path.join(base_path, "config_location.yaml")
        location_config = yaml_load(config_location_location)
        config_location = location_config["config_location"]
        full_config_location = os.path.join(base_path, config_location)
        return full_config_location

    def __set_editor_dictionary_defaults(self):
        self._editor_wrapper.set_editor_dictionary(self._config_dictionary)

    def __set_internals(self):
        session_log_buffer = self._config_dictionary["settings"]["logging"]["session_buffer_name"]
        self._config_dictionary["internal"] = { "buffer_caches": { session_log_buffer: [] }, "variables": {} }
