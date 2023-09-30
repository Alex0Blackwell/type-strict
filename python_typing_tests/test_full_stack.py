from typing import Dict, List, Union
import pytest
from python_typing.strict import strict


def test_string_arg():
    @strict
    def _func(_: str):
        pass
    _func("arg")


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
    assert str(err.value) == 'value (1) in "_func(...)" is not of type str'


def test_custom_arg_fails():
    class CustomType():
        pass

    @strict
    def _func(_: CustomType):
        pass

    with pytest.raises(TypeError) as err:
        _func(1)
    assert str(err.value) == 'value (1) in "_func(...)" is not of type CustomType'


def test_list_arg():
    @strict
    def _func(_: List[int]):
        pass
    _func([1,2,3])


def test_list_arg_as_dict():
    @strict
    def _func(_: List[int]):
        pass
    with pytest.raises(TypeError) as err:
        _func({"arg": 1})
    assert str(err.value) == 'Expected type typing.List[int] in "_func(...)" got dict'


def test_malformed_list_arg():
    @strict
    def _func(_: List[int]):
        pass
    with pytest.raises(TypeError) as err:
        _func([1,2,'whoops!',3])
    assert str(err.value) == 'value (whoops!) in "_func(...)" is not of type int'


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
    assert str(err.value) == 'value (3.14) in "_func(...)" is not any of the valid types (int, str)'


def test_malformed_list_arg_multiple_valid_types():
    @strict
    def _func(_: List[Union[int, str]]):
        pass
    _func([1,2,'whoops!',3])


def test_dict_arg():
    @strict
    def _func(_: Dict[str, int]):
        pass
    _func({"arg": 1})


def test_dict_arg_as_list():
    @strict
    def _func(_: Dict[str, int]):
        pass
    with pytest.raises(TypeError) as err:
        _func(["arg", 1])
    assert str(err.value) == 'Expected type typing.Dict[str, int] in "_func(...)" got list'


def test_dict_arg_invalid():
    @strict
    def _func(_: Dict[str, int]):
        pass
    with pytest.raises(TypeError) as err:
        _func({1: 3.14})
    assert str(err.value) == 'value (1) in "_func(...)" is not of type str'


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
    assert str(err.value) == 'value (2) in "_func(...)" is not of type str'


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
        _func({"arg": [1,2,3]})
    assert str(err.value) == 'Expected type typing.Dict[str, float] in "_func(...)" got list'


def test_dict_of_dict_of_list_arg():
    @strict
    def _func(_: Dict[str, Dict[str, List[int]]]):
        pass
    _func({"arg": {"val": [1,2,3]}})

