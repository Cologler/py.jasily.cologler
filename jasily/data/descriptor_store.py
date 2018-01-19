#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from abc import abstractmethod
from weakref import WeakKeyDictionary
import threading

from ..lang.ext_with import with_objattr

NOVALUE = object()

class IStore:

    @abstractmethod
    def has(self, descriptor, obj) -> bool:
        '''whether has value.'''
        raise NotImplementedError

    @abstractmethod
    def get(self, descriptor, obj, *, defval=NOVALUE) -> object:
        '''get value.'''
        raise NotImplementedError

    @abstractmethod
    def pop(self, descriptor, obj, *, defval=NOVALUE) -> object:
        '''get and remove value.'''
        raise NotImplementedError

    @abstractmethod
    def set(self, descriptor, obj, value):
        '''set value.'''
        raise NotImplementedError

    @abstractmethod
    def add(self, descriptor, obj, value):
        '''add value if does not exists.'''
        raise NotImplementedError


class FieldStore(IStore):

    def __init__(self, field):
        self._field = field

    def has(self, descriptor, obj):
        return self._field in vars(obj)

    def get(self, descriptor, obj, *, defval=NOVALUE):
        return vars(obj).get(self._field, defval)

    def pop(self, descriptor, obj, *, defval=NOVALUE):
        return vars(obj).pop(self._field, defval)

    def set(self, descriptor, obj, value):
        vars(obj)[self._field] = value

    def add(self, descriptor, obj, value):
        vars(obj).setdefault(obj, value)


class DictStore(IStore):

    def __init__(self, store_dict: dict=None):
        '''
        if `store_dict` is `None`, use default dict: `WeakKeyDictionary`.
        '''
        if store_dict is None:
            store_dict = WeakKeyDictionary()
        self._data = store_dict

    def has(self, descriptor, obj):
        return obj in self._data

    def get(self, descriptor, obj, *, defval=NOVALUE):
        return self._data.get(obj, defval)

    def set(self, descriptor, obj, value):
        self._data[obj] = value

    def add(self, descriptor, obj, value):
        self._data.setdefault(obj, value)

    def pop(self, descriptor, obj, *, defval=NOVALUE):
        self._data.pop(obj, defval)


class ConcurrentDictStore(DictStore):
    def __init__(self, store_dict: dict=None):
        super().__init__(store_dict)
        self._lock = threading.RLock()

for name in ('has', 'get', 'set', 'pop'):
    func = vars(DictStore)[name]
    newfunc = with_objattr('_lock')(func)
    setattr(ConcurrentDictStore, name, newfunc)
