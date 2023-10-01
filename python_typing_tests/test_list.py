from typing import List, Union

import pytest

from python_typing.strict import strict


def test_list_arg():
    @strict
    def _func(_: List[int]):
        pass

    _func([1, 2, 3])


def test_list_non_typing():
    @strict
    def _func(_: list[int]):
        pass

    _func([1, 2, 3])


def test_list_non_typing_wrong_type():
    @strict
    def _func(_: list[int]):
        pass

    with pytest.raises(TypeError) as err:
        _func(["a", "b", "c"])
    assert str(err.value) == 'Value (a) in "_func(_=list)" is not of type int'


def test_string_arg_expect_list():
    @strict
    def _func(_: List[str]):
        pass

    with pytest.raises(TypeError) as err:
        _func("arg")
    assert (
        str(err.value)
        == 'Value (arg) in "_func(_=typing.List[str])" is not of type list'
    )


def test_list_arg_as_dict():
    @strict
    def _func(_: List[int]):
        pass

    with pytest.raises(TypeError) as err:
        _func({"arg": 1})
    assert (
        str(err.value)
        == 'Expected type typing.List[int] in "_func(_=typing.List[int])" got dict'
    )


def test_malformed_list_arg():
    @strict
    def _func(_: List[int]):
        pass

    with pytest.raises(TypeError) as err:
        _func([1, 2, "whoops!", 3])
    assert (
        str(err.value)
        == 'Value (whoops!) in "_func(_=typing.List[int])" is not of type int'
    )


def test_malformed_list_arg_multiple_valid_types():
    @strict
    def _func(_: List[Union[int, str]]):
        pass

    _func([1, 2, "whoops!", 3])


def test_return_str_expect_list():
    @strict
    def _func() -> List[int]:
        return 1

    with pytest.raises(TypeError) as err:
        _func()
    assert (
        str(err.value)
        == 'Return value (1) in "_func() -> typing.List[int]" is not of type list'
    )


def test_return_list():
    @strict
    def _func() -> List[int]:
        return [1, 2, 3]

    _func()
