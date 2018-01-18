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
    def has(self, descriptor, obj, objtype):
        raise NotImplementedError

    @abstractmethod
    def get(self, descriptor, obj, objtype, *, defval=NOVALUE):
        raise NotImplementedError

    @abstractmethod
    def set(self, descriptor, obj, value, *, overwrite=True):
        raise NotImplementedError


class FieldStore(IStore):

    def __init__(self, field):
        self._field = field

    def has(self, descriptor, obj, objtype):
        if obj is None:
            return False

        return self._field in vars(obj)

    def get(self, descriptor, obj, objtype, *, defval=NOVALUE):
        if obj is None:
            return defval

        return vars(obj).get(self._field, defval)

    def set(self, descriptor, obj, value, *, overwrite=True):
        if obj is None:
            return

        if overwrite or self._field not in vars(obj):
            vars(obj)[self._field] = value

class WeakMapStore(IStore):

    def __init__(self):
        self._data = WeakKeyDictionary()

    def has(self, descriptor, obj, objtype):
        if obj is None:
            return False

        return obj in self._data

    def get(self, descriptor, obj, objtype, *, defval=NOVALUE):
        if obj is None:
            return defval

        return self._data.get(obj, defval)

    def set(self, descriptor, obj, value, *, overwrite=True):
        if obj is None:
            return

        if overwrite or obj not in self._data:
            self._data[obj] = value
