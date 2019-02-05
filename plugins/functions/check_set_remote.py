import vim
from config import Config

def check_set_remote(command_args):
    if 'target remote' in command_args["process_command"].lower():
        binary_loaded = False
        no_symbols_found = False
        for line in command_args["lines"]:
            if 'Reading symbols from' in line:
                binary_loaded = True
            if '(no debugging symbols found)' in line:
                no_symbols_found = True
                binary_loaded = True
        symbols_loaded = not no_symbols_found
        if symbols_loaded and not binary_loaded:
            symbols_loaded = False
        Config().get()['variables']['remote_target'] = 1
        Config().get()['variables']['binary_loaded'] = int(binary_loaded)
        Config().get()['variables']['symbols_loaded'] = int(symbols_loaded)
