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

def from_dict(cls: Type[T], d: dict) -> T:
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
    for k, v in d.items():
        if k not in type_hints:
            raise TypeError(f'dict key {k} in not a member of {cls}')
        type_hint = type_hints[k]
        if isinstance(v, dict):
            v = from_dict(type_hint, v)
        setattr(obj, k, v)
    obj.__class__ = cls
    return cast(T, obj)

def to_dict(obj) -> dict:
    '''
    map a dict to a cls.
    '''
    new_dict = {}
    type_hints = get_type_hints(type(obj))
    obj_dict = vars(obj)
    for k in type_hints:
        if k in obj_dict:
            v = obj_dict[k]
            if not isinstance(v, DIRECT_TYPES):
                v = to_dict(v)
            new_dict[k] = v
    return new_dict
