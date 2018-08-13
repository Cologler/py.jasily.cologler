#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------


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

from ..data.box import Box

def prop(*args, **kwargs):
    '''
    `prop` is a sugar for `property`.

    ``` py
    # mode 1
    @prop
    def value(self): pass

    # mode 2
    @prop(field='_value', get=True, set=True, [default=None])
    def value(self): pass
    ```
    '''
    def wrap(func):
        if not callable(func):
            raise TypeError

        key = kwargs.get('field', '_' + func.__name__)

        default = Box()
        default.load_from_dict(kwargs, 'default')

        fget, fset, fdel = None, None, None

        if kwargs.get('get', True):
            def getter(self):
                try:
                    return self.__dict__[key]
                except KeyError:
                    if default.has_value:
                        return default.value
                    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")
            fget = getter

        if kwargs.get('set', True):
            def setter(self, val):
                self.__dict__[key] = val
            fset = setter

        return property(fget, fset, fdel, func.__doc__)

    return wrap if kwargs else wrap(args[0])
