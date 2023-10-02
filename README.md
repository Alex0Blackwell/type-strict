# Type-Strict
Python's missing runtime type checker

## Installation

```
pip install type-strict
```

## Usage

```py
from type_strict import strict

@strict
def person_age(name: str, age: int) -> str
    return f"{name} is {age}"

# If the values mismatch the types, a TypeError is thrown.
person_age(...)
```

## Use Cases
If you ever find yourself asserting all your types are correct, for example...
```py
def func(person: Person, employee: Employee):
    if not isinstance(person, Person):
        raise TypeError("Expected person to be of type Person")
    if not isinstance(employee, Employee):
        raise TypeError("Expected employee to be of type Employee")
    ...
```
this library can simplify the same functionality into the following:
```py
@strict
def func(person: Person, employee: Employee):
    ...
```

## Features
1. Python 3.9+ support. 
2. Works with the `typing` library and default/custom Python types.
3. Checks embedded types recursively. (Eg `Dict[str, List[int]]`.)
4. Checks return type if specified.
5. Works with any combination of args, kwargs, and defaults.
6. Informative error messages.
7. In the event of a failure, type-strict swallows the error to avoid user impact.

## Limitations
1. **Performance:** Type checking is done at _runtime_. So, there is a performance
impact—especially if the value has many members, for example, a long list. For
static type checking consider [mypy](https://pypi.org/project/mypy/).
2. Ignores variable-length args (varargs).

## Examples
Wrong value.
```py
@strict
def my_func(arg1: List[int]):
    ...

# Raises:
# TypeError('Value (whoops!) in "my_func(arg1=typing.List[int])" is not of type int')
my_func([1, 2, "whoops!", 3])
```

Wrong data structure.
```py
@strict
def my_func(arg1: Dict[str, int]):
    ...

# Raises:
# TypeError('Expected type typing.Dict[str, int] in "my_func(arg1=typing.Dict[str, int])" got list')
my_func([1, 2, 3])
```

Wrong return type.
```py
@strict
def my_func() -> int:
    return "one"

# Raises:
# TypeError('Return value (one) in "my_func() -> int" is not of type int')
my_func()
```
