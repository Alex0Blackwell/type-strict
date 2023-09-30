import logging
from copy import deepcopy
import pdb
from inspect import getfullargspec
# from typing import Iterable
# from collections.abc import Iterable
from collections import abc



class Typing:
    def __init__(self, log_errors=False) -> None:
        self._log_errors = log_errors
        self._func_name = "unknown"

    def check_types(self, func, arg_values, kwargs):
        self._func_name = func.__name__
        arg_spec = getfullargspec(func)

        args_to_kwargs = {key: value for key, value in zip(arg_spec.args, arg_values)}
        kwargs = deepcopy(kwargs)
        kwargs.update(args_to_kwargs)

        for key, value in kwargs.items():
            self._is_of_type(value, arg_spec.annotations[key])
    
    def _assert_type(self, value, expected_types):
        multiple_valid_types = False
        is_an_expected_type = False
        if isinstance(expected_types, tuple):
            # Union of many valid types
            multiple_valid_types = len(expected_types) > 1
            for type_ in expected_types:
                is_an_expected_type = is_an_expected_type or isinstance(value, type_)
            valid_types = ",".join([type_.__name__ for type_ in expected_types])
        else:
            is_an_expected_type = isinstance(value, expected_types)
            valid_types = expected_types.__name__
        
        if multiple_valid_types:
            valid_types_msg = f"is not any of the valid types ({valid_types})"
        else:
            valid_types_msg = f'is not of type {valid_types}'

        if not is_an_expected_type:
            msg = f'value ({value}) in function "{self._func_name}(...)" ' + valid_types_msg
            if not self._log_errors:
                raise TypeError(msg)
            logging.warning(msg)

    def _is_of_type_list(self, values: list, type: type):
        for value in values:
            self._is_of_type(value, type)

    def _is_of_type_dict(self, key_to_value: dict, type_to_type: tuple):
        key_type, value_type = type_to_type
        for key, value in key_to_value.items():
            self._is_of_type(key, key_type)
            self._is_of_type(value, value_type)

    def _is_of_type_set(self, values: set, type: type):
        pass

    def _is_of_type(self, value, type):
        if value is None:
            return
        if isinstance(value, dict):
            assert type.__origin__ is dict
            return self._is_of_type_dict(value, type.__args__)
        if isinstance(value, list):
            assert type.__origin__ is list
            return self._is_of_type_list(value, type.__args__)
        if isinstance(value, set):
            return self._is_of_type_set()
        if isinstance(value, tuple):
            return self._is_of_type_tuple()
        self._assert_type(value, type)


def strict(func):
    def inner(*arg_values, **kwargs):
        typing = Typing()
        typing.check_types(func, arg_values, kwargs)
        func(*arg_values, **kwargs)
    return inner
