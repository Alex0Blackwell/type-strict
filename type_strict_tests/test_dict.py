from typing import Dict, List, Union

import pytest

from type_strict.strict import strict


def test_dict_arg():
    @strict
    def _func(_: Dict[str, int]):
        pass

    _func({"arg": 1})


def test_dict_non_typing_arg():
    @strict
    def _func(_: dict[str, int]):
        pass

    _func({"arg": 1})


def test_dict_arg_as_list():
    @strict
    def _func(_: Dict[str, int]):
        pass

    with pytest.raises(TypeError) as err:
        _func(["arg", 1])
    assert (
        str(err.value)
        == 'Expected type typing.Dict[str, int] in "_func(_=typing.Dict[str, int])" got list'
    )


def test_dict_non_typing_arg_as_list():
    @strict
    def _func(_: dict[str, int]):
        pass

    with pytest.raises(TypeError) as err:
        _func(["arg", 1])
    assert str(err.value) == 'Expected type dict in "_func(_=dict)" got list'


def test_dict_arg_invalid():
    @strict
    def _func(_: Dict[str, int]):
        pass

    with pytest.raises(TypeError) as err:
        _func({1: 3.14})
    assert (
        str(err.value)
        == 'Value (1) in "_func(_=typing.Dict[str, int])" is not of type str'
    )


def test_dict_arg_multiple_key_values():
    @strict
    def _func(_: Dict[str, int]):
        pass

    _func(
        {
            "arg1": 1,
            "arg2": 2,
            "arg3": 3,
        }
    )


def test_dict_arg_malformed_multiple_key_values():
    @strict
    def _func(_: Dict[str, int]):
        pass

    with pytest.raises(TypeError) as err:
        _func(
            {
                "arg1": 1,
                2: "arg2",
                "arg3": 3,
            }
        )
    assert (
        str(err.value)
        == 'Value (2) in "_func(_=typing.Dict[str, int])" is not of type str'
    )


def test_dict_arg_multiple_valid_types():
    @strict
    def _func(_: Dict[Union[str, float], int]):
        pass

    _func({"arg": 1})
    _func({3.14: 1})


def test_dict_of_dict_arg():
    @strict
    def _func(_: Dict[str, Dict[str, float]]):
        pass

    _func({"arg": {"val": 3.14}})


def test_dict_of_dict_arg_give_list():
    @strict
    def _func(_: Dict[str, Dict[str, float]]):
        pass

    with pytest.raises(TypeError) as err:
        _func({"arg": [1, 2, 3]})
    assert (
        str(err.value)
        == 'Expected type typing.Dict[str, typing.Dict[str, float]] in "_func(_=typing.Dict[str, typing.Dict[str, float]])" got list'
    )


def test_dict_of_dict_of_list_arg():
    @strict
    def _func(_: Dict[str, Dict[str, List[int]]]):
        pass

    _func({"arg": {"val": [1, 2, 3]}})


def test_return_dict():
    @strict
    def _func() -> Dict[str, int]:
        return {"one": 1, "two": 2}

    _func()
