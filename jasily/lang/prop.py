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
        '''NO DOC.'''
        if not callable(func):
            raise ValueError
        key = kwargs.get('field', '_' + func.__name__)
        has_default = 'default' in kwargs
        default = kwargs.get('default', None)
        def getter(self):
            '''NO DOC.'''
            if has_default:
                return self.__dict__.get(key, default)
            else:
                try:
                    return self.__dict__[key]
                except KeyError:
                    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")
        def setter(self, val):
            '''NO DOC.'''
            self.__dict__[key] = val
        fget = getter if kwargs.get('get', True) else None
        fset = setter if kwargs.get('set', True) else None
        p = property(fget, fset, None, func.__doc__)
        return p

    if kwargs:
        return wrap
    else:
        return wrap(args[0])
