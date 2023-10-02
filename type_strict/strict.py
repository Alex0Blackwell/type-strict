import typing
from copy import deepcopy
from inspect import _empty, getfullargspec, isclass, signature


class Typing:
    def __init__(self) -> None:
        self._func_name = "unknown"
        self._return_type = None
        self._arg_name = None
        self._arg_type = None

    def check_arg_types(self, func, arg_values, kwargs):
        try:
            self._func_name = func.__name__
            arg_spec = getfullargspec(func)
            sig = signature(func)
            kwargs = deepcopy(kwargs)

            # set the default values
            for arg, value in sig.parameters.items():
                if arg not in kwargs:
                    kwargs[arg] = value.default if value.default != _empty else None

            # set the args
            args_to_kwargs = {
                key: value for key, value in zip(arg_spec.args, arg_values)
            }
            kwargs.update(args_to_kwargs)

            for key, value in kwargs.items():
                self._arg_name = key
                if key in arg_spec.annotations:
                    self._arg_type = arg_spec.annotations[key]
                    self._is_of_type(value, self._arg_type)
        except TypeError:
            raise
        except:
            # Any errors that are not TypeErrors are bugs that should not
            # impact users of this library
            pass

    def check_return_type(self, func, return_value):
        try:
            arg_spec = getfullargspec(func)
            if "return" in arg_spec.annotations:
                self._return_type = arg_spec.annotations["return"]
                self._is_of_type(return_value, self._return_type)
        except TypeError:
            raise
        except:
            # Any errors that are not TypeErrors are bugs that should not
            # impact users of this library
            pass

    def _format_type(self, type_):
        # Get rid of <class ...> repr
        return type_.__name__ if isclass(type_) else type_

    def _assert_type_helper(self, value, expected_types):
        multiple_valid_types = False
        is_an_expected_type = False
        if isinstance(expected_types, tuple):
            # Union of many valid types
            multiple_valid_types = len(expected_types) > 1
            for type_ in expected_types:
                is_an_expected_type = is_an_expected_type or isinstance(value, type_)
            valid_types = ", ".join([type_.__name__ for type_ in expected_types])
        else:
            valid_types = expected_types.__name__
            is_an_expected_type = isinstance(value, expected_types)

        if multiple_valid_types:
            valid_types_msg = f"is not any of the valid types ({valid_types})"
        else:
            valid_types_msg = f"is not of type {valid_types}"

        if not is_an_expected_type:
            msg = ""
            if self._return_type is not None:
                msg += "return "
                return_type = self._format_type(self._return_type)
                func_sig = f'"{self._func_name}() -> {return_type}" '
            else:
                arg_type = self._format_type(self._arg_type)
                func_sig = f'"{self._func_name}({self._arg_name}={arg_type})" '

            shortened_value = str(value)[:10] + (str(value)[10:] and "..")
            msg += f"value ({shortened_value}) in " + func_sig + valid_types_msg

            msg = msg[:1].upper() + msg[1:]
            raise TypeError(msg)

    def _assert_type(self, value, expected_types):
        try:
            if expected_types.__origin__ is typing.Union:
                self._assert_type_helper(value, expected_types.__args__)
            else:
                self._assert_type_helper(value, expected_types.__origin__)
        except AttributeError:
            self._assert_type_helper(value, expected_types)

    def _assert_structure(self, structure, expected_structure):
        expected_structure_type = getattr(
            expected_structure, "__origin__", expected_structure
        )
        if structure is not expected_structure_type:
            arg_type = self._format_type(self._arg_type)
            msg = (
                f"Expected type {arg_type} in "
                f'"{self._func_name}({self._arg_name}={arg_type})" '
                f"got {structure.__name__}"
            )
            raise TypeError(msg)

    def _is_of_type_list(self, values: list, type_: type):
        for value in values:
            self._is_of_type(value, type_)

    def _is_of_type_dict(self, key_to_value: dict, key_to_value_type: tuple):
        key_type, value_type = key_to_value_type
        for key, value in key_to_value.items():
            self._is_of_type(key, key_type)
            self._is_of_type(value, value_type)

    def _is_of_type_set(self, values: set, type_: type):
        return self._is_of_type_list(values, type_)

    def _is_of_type_tuple(self, values: set, type_: type):
        return self._is_of_type_list(values, type_)

    def _is_of_type(self, value, type_):
        if value is None:
            return
        if isinstance(value, dict):
            self._assert_structure(dict, expected_structure=type_)
            return self._is_of_type_dict(value, type_.__args__)
        elif isinstance(value, list):
            self._assert_structure(list, expected_structure=type_)
            return self._is_of_type_list(value, type_.__args__[0])
        elif isinstance(value, set):
            self._assert_structure(set, expected_structure=type_)
            return self._is_of_type_set(value, type_.__args__[0])
        elif isinstance(value, tuple):
            self._assert_structure(tuple, expected_structure=type_)
            return self._is_of_type_tuple(value, type_.__args__[0])
        self._assert_type(value, type_)


def strict(func):
    """
    Raises a TypeError if any specified argument or return type mismatches its value.
    """

    def inner(*arg_values, **kwargs):
        typing = Typing()
        typing.check_arg_types(func, arg_values, kwargs)
        return_value = func(*arg_values, **kwargs)
        typing.check_return_type(func, return_value)

    return inner
