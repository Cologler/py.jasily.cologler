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
    @prop # equal `@prop(field='_value', get=True, set=True)`
    def value(self): pass

    # full kwargs
    @prop(field: str = '_value',
          get: bool = True,
          set: bool = True,
          del_: bool = False,
          default: any = AttributeError,
          types: tuple = any, # use `isinstance()` to type checked.
          )
    def value(self): pass
    ```
    '''
    def wrap(func):
        if not callable(func):
            raise TypeError

        prop_name = func.__name__
        key = kwargs.get('field', '_' + prop_name)

        default = Box()
        default.load_from_dict(kwargs, 'default')
        types = Box()
        types.load_from_dict(kwargs, 'types')

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
                if types.has_value and not isinstance(val, types.value):
                    if isinstance(types.value, tuple):
                        types_name = tuple(x.__name__ for x in types.value)
                    else:
                        types_name = types.value.__name__
                    raise TypeError(f'type of {type(self).__name__}.{prop_name} must be {types_name}; '
                                    f'got {type(val).__name__} instead')
                self.__dict__[key] = val
            fset = setter

        if kwargs.get('del_', False):
            def delete(self):
                del self.__dict__[key]
            fdel = delete

        return property(fget, fset, fdel, func.__doc__)

    return wrap if kwargs else wrap(args[0])
