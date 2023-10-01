from typing import Set, Union

import pytest

from python_typing.strict import strict


def test_set_arg():
    @strict
    def _func(_: Set[str]):
        pass

    _func({"one", "two"})


def test_set_arg_wrong_structure():
    @strict
    def _func(_: Set[str]):
        pass

    with pytest.raises(TypeError) as err:
        _func(["one", "two"])
    assert (
        str(err.value)
        == 'Expected type typing.Set[str] in "_func(_=typing.Set[str])" got list'
    )


def test_set_arg_with_union():
    @strict
    def _func(_: Set[Union[str, int]]):
        pass

    _func({"one", 2})
