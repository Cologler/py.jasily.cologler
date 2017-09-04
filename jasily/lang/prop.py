#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from .stdlib_errors import object_has_no_attr

'''
`prop` is a sugar for `property`.

``` py
@prop
def value(self):
    pass
```

As same as

``` py
@property
def value(self):
    return self._value

@value.setter
def value(self, val):
    self._value = val
```
'''

def prop(*args, **kwargs):
    '''
    `prop` is a sugar for `property`.

    ``` py
    # mode 1
    @prop
    def value(self): pass

    # mode 2
    @prop(field='_value', get=True, set=True)
    def value(self): pass
    ```
    '''
    def wrap(func):
        if not callable(func):
            raise ValueError
        key = kwargs.get('field', '_' + func.__name__)
        def getter(self):
            try:
                return self.__dict__[key]
            except KeyError:
                object_has_no_attr(type(self), key)
        def setter(self, val):
            self.__dict__[key] = val
        fget = getter if kwargs.get('get', True) else None
        fset = setter if kwargs.get('set', True) else None
        p = property(fget, fset, None, func.__doc__)
        return p

    if kwargs:
        return wrap
    else:
        return wrap(args[0])
