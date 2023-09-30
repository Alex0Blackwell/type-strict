import pdb
from typing import List
import pytest
from python_typing.strict import strict


def test_string_arg():
    @strict
    def _func(_: str):
        pass
    _func("arg1")


def test_int_arg():
    @strict
    def _func(_: int):
        pass
    _func(1)


def test_custom_arg():
    class CustomType():
        pass

    @strict
    def _func(_: CustomType):
        pass

    custom_obj = CustomType()
    _func(custom_obj)


def test_string_arg_fails():
    @strict
    def _func(_: str):
        pass
    with pytest.raises(TypeError) as err:
        _func(1)
    assert str(err.value) == 'value (1) in function "_func(...)" is not of type str'


def test_custom_arg_fails():
    class CustomType():
        pass

    @strict
    def _func(_: CustomType):
        pass

    with pytest.raises(TypeError) as err:
        _func(1)
    assert str(err.value) == 'value (1) in function "_func(...)" is not of type CustomType'


def test_list_arg():
    @strict
    def _func(_: List[int]):
        pass
    _func([1,2,3])


def test_malformed_list_arg():
    @strict
    def _func(_: List[int]):
        pass
    with pytest.raises(TypeError) as err:
        _func([1,2,'whoops!',3])
    assert str(err.value) == 'value (whoops!) in function "_func(...)" is not of type int'

