from typing import Dict, List, Set, Tuple, Union
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
    assert str(err.value) == 'Value (1) in "_func(_=...)" is not of type str'


def test_custom_arg_fails():
    class CustomType():
        pass

    @strict
    def _func(_: CustomType):
        pass

    with pytest.raises(TypeError) as err:
        _func(1)
    assert str(err.value) == 'Value (1) in "_func(_=...)" is not of type CustomType'


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
    assert str(err.value) == 'Expected type typing.List[int] in "_func(_=...)" got dict'


def test_malformed_list_arg():
    @strict
    def _func(_: List[int]):
        pass
    with pytest.raises(TypeError) as err:
        _func([1,2,'whoops!',3])
    assert str(err.value) == 'Value (whoops!) in "_func(_=...)" is not of type int'


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
    assert str(err.value) == 'Value (3.14) in "_func(_=...)" is not any of the valid types (int, str)'


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
    assert str(err.value) == 'Expected type typing.Dict[str, int] in "_func(_=...)" got list'


def test_dict_arg_invalid():
    @strict
    def _func(_: Dict[str, int]):
        pass
    with pytest.raises(TypeError) as err:
        _func({1: 3.14})
    assert str(err.value) == 'Value (1) in "_func(_=...)" is not of type str'


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
    assert str(err.value) == 'Value (2) in "_func(_=...)" is not of type str'


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
    assert str(err.value) == 'Expected type typing.Dict[str, float] in "_func(_=...)" got list'


def test_dict_of_dict_of_list_arg():
    @strict
    def _func(_: Dict[str, Dict[str, List[int]]]):
        pass
    _func({"arg": {"val": [1,2,3]}})

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
    assert str(err.value) == 'Expected type typing.Set[str] in "_func(_=...)" got list'


def test_set_arg_with_union():
    @strict
    def _func(_: Set[Union[str, int]]):
        pass
    _func({"one", 2})


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
    assert str(err.value) == 'Expected type typing.Tuple[str] in "_func(_=...)" got list'


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


# def test_return_str_expect_int():
#     @strict
#     # def _func() -> int:
#     def _func() -> List[int]:
#         return "one"
#     with pytest.raises(TypeError) as err:
#         _func()
#     assert str(err.value) == 'return Value (one) in "_func(_=...)" is not of type int'


def test_return_str_expect_int():
    @strict
    def _func() -> int:
        return "one"
    with pytest.raises(TypeError) as err:
        _func()
    assert str(err.value) == 'Return value (one) in "_func() -> int" is not of type int'




def test_return_dict():
    @strict
    def _func() -> Dict[str, int]:
        return {"one": 1, "two": 2}
    _func()


def test_return_list():
    @strict
    def _func() -> List[int]:
        return [1,2,3]
    _func()


def test_multiple_args():
    @strict
    def _func(_1: int, _2: str):
        pass
    _func(1, "two")


def test_vargs_is_ignored():
    tuple_ = (1,2,3)
    @strict
    def _func(*args: int):
        pass
    _func(*tuple_)


def test_kwargs():
    @strict
    def _func(one: str = "one"):
        pass
    _func(one="two")

# Testing defaults

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
    assert str(err.value) == 'Value (1) in "_func(_=...)" is not of type str'

# _func(_:str=1) expects type str but got type int.
