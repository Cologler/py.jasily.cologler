#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
# provide different ways for make propertys.
# ----------

_UNSET = object()

def prop(func=None, *,
         field = _UNSET,
         get: bool = True, set: bool = True, del_: bool = False,
         default = _UNSET,
         types: tuple = _UNSET):
    '''
    `prop` is a sugar for `property`.

    ``` py
    @prop
    def value(self):
        pass

    # equals:

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
    ```
    '''

    def wrap(func):
        if not callable(func):
            raise TypeError

        prop_name = func.__name__
        key = field
        if key is _UNSET:
            key = '_' + prop_name

        fget, fset, fdel = None, None, None

        if get:
            def fget(self):
                try:
                    return self.__dict__[key]
                except KeyError:
                    if default is not _UNSET:
                        return default
                    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")

        if set:
            def fset(self, val):
                if types is not _UNSET and not isinstance(val, types):
                    if isinstance(types, tuple):
                        types_name = tuple(x.__name__ for x in types)
                    else:
                        types_name = types.__name__
                    raise TypeError(f'type of {type(self).__name__}.{prop_name} must be {types_name}; '
                                    f'got {type(val).__name__} instead')
                self.__dict__[key] = val

        if del_:
            def fdel(self):
                del self.__dict__[key]

        return property(fget, fset, fdel, func.__doc__)

    return wrap(func) if func else wrap

def get_only(field):
    '''
    `get_only` is a sugar for `property`.

    ``` py
    value = get_only('_value')

    # equals:

    @property
    def value(self):
        return getattr(self, '_value')
    ```
    '''
    return property(lambda self: getattr(self, field))

def get_onlys(*fields):
    '''
    `get_onlys` is a sugar for multi-`property`.

    ``` py
    name, age = get_onlys('_name', '_age')

    # equals:

    @property
    def name(self):
        return getattr(self, '_name')

    @property
    def age(self):
        return getattr(self, '_age')
    ```
    '''
    return tuple(property(lambda self, f=f: getattr(self, f)) for f in fields)
