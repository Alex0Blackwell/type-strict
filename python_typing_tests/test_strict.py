from typing import Callable, Union

import pytest

from python_typing.strict import strict


def test_empty():
    @strict
    def _func():
        pass

    _func()


def test_empty_pass_arg():
    @strict
    def _func():
        pass

    with pytest.raises(TypeError) as err:
        _func("arg")
    assert str(err.value) == "_func() takes 0 positional arguments but 1 was given"


def test_arg_pass_nothing():
    @strict
    def _func(_):
        pass

    with pytest.raises(TypeError) as err:
        _func()
    assert str(err.value) == "_func() missing 1 required positional argument: '_'"


def test_arg_no_type():
    @strict
    def _func(_):
        pass

    _func("arg")


def test_string_arg():
    @strict
    def _func(_: str):
        pass

    _func("arg")


def test_string_arg_gets_shortened():
    @strict
    def _func(_: int):
        pass

    with pytest.raises(TypeError) as err:
        _func("loooooooooooooooong")
    assert str(err.value) == 'Value (looooooooo..) in "_func(_=int)" is not of type int'


def test_int_arg():
    @strict
    def _func(_: int):
        pass

    _func(1)


def test_string_arg_fails():
    @strict
    def _func(_: str):
        pass

    with pytest.raises(TypeError) as err:
        _func(1)
    assert str(err.value) == 'Value (1) in "_func(_=str)" is not of type str'


def test_union_arg_first():
    @strict
    def _func(_: Union[int, str]):
        pass

    _func(1)


def test_union_arg_second():
    @strict
    def _func(_: Union[int, str]):
        pass

    _func("arg")


def test_union_arg_many():
    @strict
    def _func(_: Union[int, str, bool, float]):
        pass

    _func(3.14)


def test_union_arg_invalid():
    @strict
    def _func(_: Union[int, str]):
        pass

    with pytest.raises(TypeError) as err:
        _func(3.14)
    assert (
        str(err.value)
        == 'Value (3.14) in "_func(_=typing.Union[int, str])" is not any of the valid types (int, str)'
    )


def test_return_str():
    @strict
    def _func() -> str:
        return "val"

    _func()


def test_return_int():
    @strict
    def _func() -> int:
        return 1

    _func()


def test_return_str_expect_int():
    @strict
    def _func() -> int:
        return "one"

    with pytest.raises(TypeError) as err:
        _func()
    assert str(err.value) == 'Return value (one) in "_func() -> int" is not of type int'


def test_multiple_args():
    @strict
    def _func(_1: int, _2: str):
        pass

    _func(1, "two")


def test_vargs_is_ignored():
    tuple_ = (1, 2, 3)

    @strict
    def _func(*args: int):
        pass

    _func(*tuple_)


def test_kwargs():
    @strict
    def _func(one: str = "one"):
        pass

    _func(one="two")


def test_callable_arg():
    def _some_callable():
        pass

    @strict
    def _func(_: Callable):
        pass

    _func(_some_callable)


def test_callable_arg_not_callable():
    @strict
    def _func(_: Callable):
        pass

    with pytest.raises(TypeError) as err:
        _func(1)
    assert str(err.value) == 'Value (1) in "_func(_=typing.Callable)" is not of type Callable'
