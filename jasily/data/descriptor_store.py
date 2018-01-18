#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from abc import abstractmethod
from weakref import WeakKeyDictionary

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
    def set(self, descriptor, obj, value, *, overwrite=True):
        '''set value.'''
        raise NotImplementedError

    @abstractmethod
    def pop(self, descriptor, obj, *, defval=NOVALUE) -> object:
        '''get and remove value.'''
        raise NotImplementedError


class FieldStore(IStore):

    def __init__(self, field):
        self._field = field

    def has(self, descriptor, obj):
        return self._field in vars(obj)

    def get(self, descriptor, obj, *, defval=NOVALUE):
        return vars(obj).get(self._field, defval)

    def set(self, descriptor, obj, value, *, overwrite=True):
        if overwrite or self._field not in vars(obj):
            vars(obj)[self._field] = value

    def pop(self, descriptor, obj, *, defval=NOVALUE):
        return vars(obj).pop(self._field, defval)


class WeakMapStore(IStore):

    def __init__(self):
        self._data = WeakKeyDictionary()

    def has(self, descriptor, obj):
        return obj in self._data

    def get(self, descriptor, obj, *, defval=NOVALUE):
        return self._data.get(obj, defval)

    def set(self, descriptor, obj, value, *, overwrite=True):
        if overwrite or obj not in self._data:
            self._data[obj] = value

    def pop(self, descriptor, obj, *, defval=NOVALUE):
        self._data.pop(obj, defval)
