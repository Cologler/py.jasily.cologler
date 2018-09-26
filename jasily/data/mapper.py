# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
# map a dict to a class or map a class to a dict
# ----------

'''
map a dict to a model (class) (without any type check).

for example:

``` py
class A:
    a: int
    b: str = ''

a: A = from_dict(A, {'b': 1})
assert a.b == 1
_ = a.a # AttributeError
```
'''

from typing import Type, TypeVar, get_type_hints, cast

from .fullvars import fullvars

DIRECT_TYPES = (type(None), bool, int, float, str, list, dict)

T = TypeVar('T')


class AttrOptions:
    def __init__(self):
        self.is_ignored = False

    def ignore(self):
        self.is_ignored = True
        return self


class Mapper:
    '''
    map dict to model; or map model to dict.
    '''
    _DEF_OPTIONS = AttrOptions()

    def __init__(self):
        self._attrs = {}
        self.direct_types = DIRECT_TYPES
        self.strict = True

    def attr(self, name):
        options = self._attrs.get(name)
        if options is None:
            self._attrs[name] = options = AttrOptions()
        return options

    def from_dict(self, cls: Type[T], d: dict) -> T:
        obj = self.create_instance(cls)
        type_hints = get_type_hints(cls)
        for key, value in d.items():
            options = self._attrs.get(key, self._DEF_OPTIONS)
            if options.is_ignored:
                continue
            if key in type_hints:
                type_hint = type_hints[key]
                if value is not None and not isinstance(value, type_hint):
                    value = from_dict(type_hint, value)
            elif self.strict:
                raise TypeError(f'dict key {key} in not a member of {cls}')
            setattr(obj, key, value)
        return cast(T, obj)

    def to_dict(self, obj) -> dict:
        '''
        map a model object to a dict.
        '''
        new_dict = {}
        type_hints = get_type_hints(type(obj))
        obj_dict = fullvars(obj)
        for key in obj_dict:
            options = self._attrs.get(key, self._DEF_OPTIONS)
            if options.is_ignored:
                continue
            if key in type_hints:
                value = obj_dict[key]
                if not isinstance(value, self.direct_types):
                    value = self.to_dict(value)
                new_dict[key] = value
        return new_dict

    def create_instance(self, cls: type):
        class _Any(cls):
            __slots__ = ()
        obj = _Any()
        # pylint: disable=W0201,E0237
        obj.__class__ = cls
        return obj

def from_dict(cls: Type[T], d: dict, *, strict=True) -> T:
    mapper = Mapper()
    mapper.strict = strict
    return mapper.from_dict(cls, d)

def to_dict(obj) -> dict:
    '''
    map a model object to a dict.
    '''
    mapper = Mapper()
    return mapper.to_dict(obj)
