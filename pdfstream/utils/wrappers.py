"""Decorators API."""
from functools import wraps
from typing import Callable


def report_stage(func: Callable):
    """Add 'start' at the beginning and 'finish' at the end."""

    @wraps(func)
    def _func(*args, **kwargs):
        print(f"start {func.__name__}")
        returns = func(*args, **kwargs)
        print(f"finish {func.__name__}")
        return returns

    return _func


def take_in_namespace(func: Callable):
    """Make function take a dictionary and return the name space. Flatten the kwargs in name space."""

    @wraps(func)
    def _func(namespace: dict, **kwargs):
        # pop out not used kwargs and unpack and put back to dictionary
        namespace.update(kwargs)
        namespace = func(**namespace)
        namespace.update(namespace.pop('kwargs', {}))
        return namespace

    return _func
