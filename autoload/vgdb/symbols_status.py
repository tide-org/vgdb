import vim
from config import Config

def set_binary_symbols_status(lines):
    binary_loaded = False
    no_symbols_found = False
    for line in lines:
        if 'Reading symbols from' in line:
            binary_loaded = True
        if '(no debugging symbols found)' in line:
            no_symbols_found = True
            binary_loaded = True
    symbols_loaded = not no_symbols_found
    # this is an impssible state which can occur if neither string is matched above
    if symbols_loaded == True and binary_loaded == False:
        symbols_loaded = False
    Config().get()['variables']['binary_loaded'] = str(int(binary_loaded))
    Config().get()['variables']['symbols_loaded'] = str(int(symbols_loaded))
