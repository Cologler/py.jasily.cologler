#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import functools
from .descriptor_store import IStore, FieldStore, NOVALUE

def get_descriptor_name(descriptor):
    if isinstance(descriptor, property):
        funcs = [descriptor.fget, descriptor.fset, descriptor.fdel]
        funcs = [f.__name__ for f in funcs if f is not None]
        return funcs[0]

    if isinstance(descriptor, getonly_property):
        return descriptor.fget.__name__

    return getattr(descriptor, '__name__', None)


class ICacheDescriptor:
    '''the base type for `CacheDescriptor`.'''
    pass


def cache(descriptor=None, *, store: IStore = None):
    '''
    usage:

    ``` py
    @cache
    @property
    def name(self): pass
    ```
    '''

    if descriptor is None:
        return functools.partial(cache, store=store)

    hasattrs = {
        'get': hasattr(descriptor, '__get__'),
        'set': hasattr(descriptor, '__set__'),
        'del': hasattr(descriptor, '__delete__')
    }

    descriptor_name = get_descriptor_name(descriptor)

    # pylint: disable=R0903,C0111
    class CacheDescriptor(ICacheDescriptor):
        def __init__(self):
            if descriptor_name is not None:
                self.__name__ = descriptor_name

        def __getattr__(self, name):
            print(name)
            raise NotImplementedError

        def __getattribute__(self, name):
            raise NotImplementedError

    cache_descriptor = CacheDescriptor()

    if store is None:
        store = FieldStore(cache_descriptor)
    elif not isinstance(store, IStore):
        raise TypeError(f'store must be a {IStore}.')

    if hasattrs['get']:
        def get(self, obj, objtype):
            if obj is None:
                return descriptor.__get__(obj, objtype)
            value = store.get(self, obj, defval=NOVALUE)
            if value is NOVALUE:
                value = descriptor.__get__(obj, objtype)
                store.set(self, obj, value)
            return value

        CacheDescriptor.__get__ = get

    if hasattrs['set']:
        def set(self, obj, value):
            store.pop(self, obj)
            descriptor.__set__(obj, value)

        CacheDescriptor.__set__ = set

    if hasattrs['del']:
        def delete(self, obj):
            store.pop(self, obj)
            descriptor.__delete__(obj)

        CacheDescriptor.__delete__ = delete

    return cache_descriptor


class getonly_property:
    '''
    a getonly property just like `property`.
    but, this is **NOT** a data descriptor.

    usage:

    ``` py
    # example 1: use as default value.
    class A:
        @getonly_property
        def name(self):
            return 'x'
    a = A()
    a.name         # a.name == 'x'
    a.name = '1'   # a.name == '1'
    del a.name     # a.name == 'x'
    ```

    '''

    def __init__(self, fget, doc=None):
        if fget is None:
            raise ValueError('fget cannot be None.')

        self.fget = fget
        if doc is None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        return self.fget(obj)
