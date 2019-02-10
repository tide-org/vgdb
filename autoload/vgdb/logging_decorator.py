import datetime
import inspect
from config import Config

def logging(func):

    def get_object_name(func, *args):
        try:
            inspect.getargspec(func)[0][0] == 'self'
            return '{}.{}.{}'.format(func.__module__, args[0].__class__.__name__, func.__name__)
        except:
            return '{}.{}'.format(func.__module__, func.__name__)

    def wrapper(*args, **kwargs):
        if Config().get()["settings"]["debugging"]["log_to_file"]:
            filename = Config().get()["settings"]["debugging"]["log_filename"]
            object_name = get_object_name(func, args)
            debug_actions = Config().get()["settings"]["debugging"]["debug_actions"]

            if (not debug_actions and ("command_action.tuple.CommandAction" in object_name)):
                return func(*args, **kwargs)

            with open(filename, 'a+') as file_handle:
                file_handle.write(str(datetime.datetime.utcnow()) + " - START - OBJECT: " + object_name)
                if args:
                    file_handle.write(" - ARGS: " + str(args))
                if kwargs:
                    file_handle.write(" - KWARGS: " + str(kwargs))
                func_result = func(*args, **kwargs)
                file_handle.write('\n')
                if isinstance(func_result, dict):
                    return_object_values_string = str(vars(func_result))
                else:
                    return_object_values_string = str(func_result)
                file_handle.write(str(datetime.datetime.utcnow()) + " - END --- OBJECT: " + object_name + " - RETURN_OBJECT: " + str(func_result) + " - " + "RETURN_OBJECT_VALUES: " + return_object_values_string + '\n')
        return func_result

    return wrapper

