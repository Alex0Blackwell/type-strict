import heapq
from typing import Optional

import pytest

from py_strict.strict import strict


def test_default():
    @strict
    def _func(_: str = "one"):
        pass

    _func()


def test_single_default():
    @strict
    def _func(one: int, two: str = "one"):
        pass

    _func(1)


def test_single_default_both_specified():
    @strict
    def _func(one: int, two: str = "one"):
        pass

    _func(1, "two")


def test_single_default_specified():
    @strict
    def _func(one: int, two: str = "one"):
        pass

    _func(1, two="two")


def test_single_specified_with_default():
    @strict
    def _func(one: int, two: int, three: str = "three"):
        pass

    _func(1, two=2)


def test_default_wrong_type():
    @strict
    def _func(_: str = 1):
        pass

    with pytest.raises(TypeError) as err:
        _func()
    assert str(err.value) == 'Value (1) in "_func(_=str)" is not of type str'


def test_one_arg_wrong():
    @strict
    def _func(one: int, two: int, three: str = "three"):
        pass

    with pytest.raises(TypeError) as err:
        _func(1, two="oops!")
    assert str(err.value) == 'Value (oops!) in "_func(two=int)" is not of type int'


def test_some_specified_some_not():
    @strict
    def _func(one: str, two, three: int):
        pass

    _func("arg", 2, 3)


def test_arg_optional():
    @strict
    def _func(_: Optional[str]):
        pass

    _func("arg")


def test_arg_optional_none_specified():
    @strict
    def _func(_: Optional[str]):
        # Note the arg isn't actually optional here
        pass

    with pytest.raises(TypeError) as err:
        _func()
    # Assert "in" for python 3.10+ compatibility
    assert "_func() missing 1 required positional argument: '_'" in str(err.value)


def test_arg_optional_give_none():
    @strict
    def _func(_: Optional[str] = None):
        pass

    _func()


def test_arg_optional_give_correct_default():
    @strict
    def _func(_: Optional[str] = "string"):
        pass

    _func()


def test_arg_optional_give_wrong_default():
    @strict
    def _func(_: Optional[str] = 1):
        pass

    with pytest.raises(TypeError) as err:
        _func()
    assert (
        str(err.value)
        == 'Value (1) in "_func(_=typing.Optional[str])" is not any of the valid types (str, NoneType)'
    )
