# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
# map a dict to a class or map a class to a dict
# ----------

from typing import Type, TypeVar, get_type_hints, cast

DIRECT_TYPES = (type(None), bool, int, float, str, list, dict)

T = TypeVar('T')

class _Any:
    pass

def from_dict(cls: Type[T], d: dict, *, strict=True) -> T:
    '''
    map a dict to a cls (without type check).

    for example:

    ``` py
    class A:
        a: int
        b: str = ''

    a: A = from_dict(A, {'b': 1})
    assert a.b == 1 # no type checked
    _ = a.a # AttributeError
    ```
    '''
    obj = _Any()
    type_hints = get_type_hints(cls)
    for key, value in d.items():
        if key in type_hints:
            type_hint = type_hints[key]
            if value is not None and not isinstance(value, type_hint):
                value = from_dict(type_hint, value)
        elif strict:
            raise TypeError(f'dict key {key} in not a member of {cls}')
        setattr(obj, key, value)
    obj.__class__ = cls
    return cast(T, obj)

def to_dict(obj, *, direct_types=DIRECT_TYPES) -> dict:
    '''
    map a model object to a dict.
    '''
    new_dict = {}
    type_hints = get_type_hints(type(obj))
    obj_dict = vars(obj)
    for key in obj_dict:
        if key in type_hints:
            value = obj_dict[key]
            if not isinstance(value, direct_types):
                value = to_dict(value)
            new_dict[key] = value
    return new_dict
