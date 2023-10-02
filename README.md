# Py-Strict
## Python's missing runtime type checker

Readme incoming.

Basic usage:

```py
from py_strict import strict

@strict
def person_age(name: str, age: int) -> str
    return f"{name} is {age}"

# If the values mismatch the types, a TypeError is thrown.
person_age(...)
```