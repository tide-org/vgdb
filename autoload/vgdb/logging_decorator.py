import os
import datetime
import inspect
from config import Config
import config_source as Cs

DEBUG_SETTINGS = Cs.CONFIG_OBJECT["settings"]["debugging"]
DEBUG_KEYS = DEBUG_SETTINGS.keys()
LOG_FILENAME = DEBUG_SETTINGS["log_filename"]
LOG_TO_FILE = DEBUG_SETTINGS["log_to_file"]

try:
    os.remove(LOG_FILENAME)
except OSError:
    pass

def logging(func):

    def get_object_name(func, *args):
        if inspect.getargspec(func)[0]:
            return '{}.{}.{}'.format(func.__module__, args[0].__class__.__name__, func.__name__)
        else:
            return '{}.{}'.format(func.__module__, func.__name__)

    def can_process_object():
        for debug_key in DEBUG_KEYS:
            if debug_key.startswith('debug_'):
                temp_key = debug_key.replace('debug_', '')
                debug_this_object = DEBUG_SETTINGS[debug_key]
                if not debug_this_object and (temp_key in func.__module__):
                    return 0
        return 1

    def write_to_log(args, kwargs):
        with open(LOG_FILENAME, 'a+') as file_handle:
            object_name = get_object_name(func, args)

            if object_name == 'singleton.getinstance':
                object_name = str(func)

            file_handle.write(str(datetime.datetime.utcnow()) + " - START - OBJECT: " + object_name + " -- " + str(inspect.getargspec(func)[0]) + " -- ")

            if args:
                file_handle.write(" - ARGS: " + str(args))
            if kwargs:
                file_handle.write(" - KWARGS: " + str(kwargs))

            func_result = func(*args, **kwargs)

            file_handle.write('\n')

            try:
                return_object_values_string = str(vars(func_result))
            except:
                return_object_values_string = str(func_result)

            file_handle.write(str(datetime.datetime.utcnow()) + " - END --- OBJECT: " + object_name + " - RETURN_OBJECT: " + str(func_result) + " - " + "RETURN_OBJECT_VALUES: " + return_object_values_string + '\n')

        return func_result

    def wrapper(*args, **kwargs):
        if LOG_TO_FILE and  can_process_object():
            return write_to_log(args, kwargs)
        return func(*args, **kwargs)

    return wrapper
