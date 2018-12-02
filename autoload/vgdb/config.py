from poyo import parse_string, PoyoException
import vim
import os
import codecs

class Config:

    __config_dictionary = None

    def __init__(self):
        if not self.__config_dictionary:
            self.set()

    def get(self):
        return self.__config_dictionary

    def set(self):
        full_template_location = self.__get_full_template_location()
        with codecs.open(full_template_location, encoding='utf-8') as ymlfile:
            ymlstring = ymlfile.read()
        try:
            config = parse_string(ymlstring)
            self.__config_dictionary = config
            self.__set_vim_globals(config)
        except PoyoException as exc:
            print("error setting config: " + str(exc))

    def __get_full_template_location(self):
        template_location = vim.eval("g:vg_config_location")
        full_template_location =  os.path.join(os.getcwd(), template_location)
        return full_template_location

    def __set_vim_globals(self, config):
        config_string = str(config).replace(": False", ": 'False'").replace(": True", ": 'True'")
        vim.command("let g:vg_config_dictionary = " + config_string)
        self.__set_vim_buffer_config(config)

    def __set_vim_buffer_config(self, config):
        for buffer_item in config["buffers"]:
            vim.command("let g:vg_config_buffers = add(g:vg_config_buffers, '" + buffer_item + "')")
            if "on_startup" in config["buffers"][buffer_item]:
                if config["buffers"][buffer_item]["on_startup"] == True:
                    vim.command("let g:vg_config_startup_buffers = add(g:vg_config_startup_buffers, '" + buffer_item + "')")

