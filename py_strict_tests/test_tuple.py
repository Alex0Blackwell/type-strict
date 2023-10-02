from typing import Tuple

import pytest

from py_strict.strict import strict


def test_tuple_arg():
    @strict
    def _func(_: Tuple[str]):
        pass

    _func(("one", "two"))


def test_tuple_arg_wrong_structure():
    @strict
    def _func(_: Tuple[str]):
        pass

    with pytest.raises(TypeError) as err:
        _func(["one", "two"])
    assert (
        str(err.value)
        == 'Expected type typing.Tuple[str] in "_func(_=typing.Tuple[str])" got list'
    )
