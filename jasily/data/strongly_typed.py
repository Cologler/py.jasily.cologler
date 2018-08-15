# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

'''
# example:

``` py
class A:
    b: int
    c: int = 10

a = make_strongly_typed(A, {'b': 1})
assert isinstance(a, A)
assert a.c == 10
```
'''

from typing import Type, TypeVar, get_type_hints

T = TypeVar('T')

NOT_OBJECT_TYPES = (type(None), bool, int, float, str, list, dict)

def _create_fget(cls: type, d: dict, name: str):
    def fget(_):
        try:
            return d[name]
        except KeyError:
            return getattr(cls, name)
    return fget

def _create_fget_deep(cls: type, d: dict, name: str, type_hint: type):
    fget_raw = _create_fget(cls, d, name)
    def fget(self):
        data = fget_raw(self)
        return make_strongly_typed(type_hint, data)
    return fget

def _create_fset(cls: type, d: dict, name: str):
    def fset(_, value):
        d[name] = value
    return fset

def _create_fset_deep(cls: type, d: dict, name: str, type_hint: type):
    fset_raw = _create_fset(cls, d, name)
    def fset(self, value):
        data = None
        if value is not None:
            if not isinstance(value, type_hint):
                raise TypeError(f'type of {cls.__name__}.{name} must be {type_hint.__name__}; '
                                f'got {type(value).__name__} instead')
            data = vars(value).copy()
        fset_raw(self, data)
    return fset

def _create_fdel(cls: type, d: dict, name: str):
    def fdel(_):
        del d[name]
    return fdel

def make_strongly_typed(cls: Type[T], d: dict) -> T:
    '''
    return a object which create by cls
    '''
    if not isinstance(d, dict):
        raise TypeError

    attr_dict = {}
    type_hints = get_type_hints(cls)
    for k, type_hint in type_hints.items():
        if isinstance(type_hint, type) and type_hint not in NOT_OBJECT_TYPES:
            fget = _create_fget_deep(cls, d, k, type_hint)
            fset = _create_fset_deep(cls, d, k, type_hint)
        else:
            fget = _create_fget(cls, d, k)
            fset = _create_fset(cls, d, k)
        fdel = _create_fdel(cls, d, k)
        prop = property(fget, fset, fdel)
        attr_dict[k] = prop
    new_cls = type(cls.__name__, (cls, ), attr_dict)
    ret = new_cls()
    return ret
