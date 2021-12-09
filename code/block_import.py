import inspect, os
from functools import wraps, partial


class CannotImport(Exception):
    pass

class CannotCall(Exception):
    pass


def parameterized_decorator(decorator):
    @wraps(decorator) 
    def outer(*args, **kwargs):
        def inner(func):
            return decorator(func, *args, **kwargs)
        return inner
    return outer


def block_imports(allowed_modules=None):
    my_name = __name__

    if allowed_modules:
        for frame in inspect.stack()[2:]: #1 if you are putting this directly in the module to be blocked, 2 if you are putting this into another module for import into the lib you want to block
            importer = frame.filename
            if importer[0] != '<': # The first non-internal lib
                importer_module_name = importer[importer.rfind(os.sep)+1:]
                if importer_module_name not in allowed_modules:
                    raise CannotImport(f"{importer_module_name} is not permitted to import {my_name}")
                break
    else:
        raise CannotImport("{my_name} is not permitted to be imported.")


@parameterized_decorator
def block_calls(func, allowed_modules=None):
    @wraps(func)
    def inner(*args, **kwargs):
        caller_module = inspect.stack()[1].filename
        caller_name = caller_module[caller_module.rfind(os.sep)+1:]
        if caller_name not in allowed_modules:
            raise CannotCall(f"Code from {caller_name} is not permitted to call {func.__name__}")
        func(*args, **kwargs)
    return inner
