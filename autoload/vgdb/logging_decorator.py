import datetime
import inspect

def logging(func):

    def get_object_name(func, *args):
        try:
            is_method = inspect.getargspec(func)[0][0] == 'self'
        except:
            is_method = False

        if is_method:
            name = '{}.{}.{}'.format(func.__module__, args[0].__class__.__name__, func.__name__)
        else:
            name = '{}.{}'.format(func.__module__, func.__name__)
        return name

    def wrapper(*args, **kwargs):
        object_name = get_object_name(func, args)

        with open('log.txt', 'w') as file_handle:
            file_handle.write(str(datetime.datetime.utcnow()) + " - ")
            file_handle.write(object_name)
            if args:
                file_handle.write(str(args))
            if kwargs:
                file_handle.write(" - kwargs" + str(kwargs))

        return func(*args, **kwargs)

    return wrapper

