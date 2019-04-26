# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
# decorator for instance methods
# ----------

import functools

from ..objects import Key
from ..data.var import get_object_var_factory

def _get_var_factory(var_factory):
    if var_factory is None:
        def var_factory(obj, key):
            return get_object_var_factory(obj)(key)

    return var_factory

def cache(method=None, *, var_factory=None, key=None):
    '''
    cache for none parameters instance methods.

    if the method has parameters, try use `functools.lru_cache`.
    '''

    if method is None:
        return functools.partial(cache, var_factory=var_factory, key=key)

    var_factory = _get_var_factory(var_factory)
    _NOT_FOUND = object()
    if key is None:
        key = Key()

    @functools.wraps(method)
    def wrapper(self):
        var: IVar = var_factory(self, key)
        val = var.get(_NOT_FOUND)
        if val is _NOT_FOUND:
            val = method(self)
            var.set(val)
        return val

    return wrapper


def once(method=None, *, var_factory=None):
    '''
    only call the method once, ignore if call again.

    return value always be `None`.
    '''

    if method is None:
        return functools.partial(once, var_factory=var_factory)

    var_factory = _get_var_factory(var_factory)
    key = Key(f'is {method!r} called')

    @functools.wraps(method)
    def wrapper(self):
        var: IVar = var_factory(self, key)
        if not var.has_value:
            var.set(True)
            method(self)

    return wrapper


def assert_once(method=None, *, var_factory=None):
    '''
    only call the method once, assert false if call again.

    return value always be `None`.
    '''
    if method is None:
        return functools.partial(assert_once, var_factory=var_factory)

    var_factory = _get_var_factory(var_factory)
    key = Key(f'is {method!r} called')

    @functools.wraps(method)
    def wrapper(self):
        var: IVar = var_factory(self, key)
        if not var.has_value:
            var.set(True)
            method(self)
        else:
            assert False, 'method cannot call again'

    return wrapper
