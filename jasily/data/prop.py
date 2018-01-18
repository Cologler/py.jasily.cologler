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

class _Descriptor:

    def __init__(self, base_descriptor):
        self._base_descriptor = base_descriptor

    def __get__(self, obj, objtype):
        return self._base_descriptor.__get__(obj, objtype)


class _CacheDescriptor(_Descriptor):
    def __init__(self, base_descriptor, store):
        super().__init__(base_descriptor)

        if store is None:
            field = get_descriptor_name(base_descriptor) or self
            store = FieldStore(field)
        self._store = store

    def __get__(self, obj, objtype):
        value = self._store.get(self, obj, objtype, defval=NOVALUE)
        if value is NOVALUE:
            value = super().__get__(obj, objtype)
            self._store.set(self, obj, value)
        return value


class _DataDescriptor(_Descriptor):

    def __set__(self, obj, value):
        return self._base_descriptor.__set__(obj, value)


class _CacheDataDescriptor(_DataDescriptor):

    def __init__(self, base_descriptor, store):
        super().__init__(base_descriptor)

        if store is None:
            field = get_descriptor_name(base_descriptor) or self
            store = FieldStore(field)
        self._store = store

    def __get__(self, obj, objtype):
        value = self._store.get(self, obj, objtype, defval=NOVALUE)
        if value is NOVALUE:
            value = super().__get__(obj, objtype)
            self._store.set(self, obj, value)
        return value


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
    if store is not None and not isinstance(store, IStore):
        raise TypeError(f'store must be a {IStore}.')

    if not hasattr(descriptor, '__get__'):
        raise TypeError(f'{descriptor} is not a descriptor.')

    if hasattr(descriptor, '__set__'):
        return _CacheDataDescriptor(descriptor, store=store)
    else:
        return _CacheDescriptor(descriptor, store=store)


class getonly_property:
    '''
    a getonly property just like `property`.
    but, this is **NOT** a data descriptor.
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
