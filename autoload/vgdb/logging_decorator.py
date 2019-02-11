import datetime
import inspect
from config import Config

def logging(func):

    def get_object_name(func, *args):
        if inspect.getargspec(func)[0]:
            return '{}.{}.{}'.format(func.__module__, args[0].__class__.__name__, func.__name__)
        else:
            return '{}.{}'.format(func.__module__, func.__name__)

    def wrapper(*args, **kwargs):
        if Config().get()["settings"]["debugging"]["log_to_file"]:
            filename = Config().get()["settings"]["debugging"]["log_filename"]
            object_name = get_object_name(func, args)
            debug_keys = Config().get()["settings"]["debugging"].keys()
            for debug_key in debug_keys:
                if debug_key.startswith('debug_'):
                    temp_key = debug_key.replace('debug_', '')
                    debug_this_object = Config().get()["settings"]["debugging"][debug_key]
                    if not debug_this_object and (temp_key in func.__module__):
                        return

            with open(filename, 'a+') as file_handle:
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

    return wrapper

