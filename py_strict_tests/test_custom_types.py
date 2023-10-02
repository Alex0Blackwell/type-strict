import heapq

import pytest

from py_strict.strict import strict


def test_custom_arg():
    class CustomType:
        pass

    @strict
    def _func(_: CustomType):
        pass

    custom_obj = CustomType()
    _func(custom_obj)


def test_custom_arg_fails():
    class CustomType:
        pass

    @strict
    def _func(_: CustomType):
        pass

    with pytest.raises(TypeError) as err:
        _func(1)
    assert (
        str(err.value) == 'Value (1) in "_func(_=CustomType)" is not of type CustomType'
    )


def test_heap():
    @strict
    def _func(_: list):
        pass

    q = []
    heapq.heappush(q, (1, "test"))
    _func(q)


def test_heap_expect_dict():
    @strict
    def _func(_: dict):
        pass

    q = []
    heapq.heappush(q, (1, "test"))
    with pytest.raises(TypeError) as err:
        _func(q)
    assert str(err.value) == 'Expected type dict in "_func(_=dict)" got list'
