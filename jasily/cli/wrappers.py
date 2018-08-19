#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
# wrap any obj as a command class.
# ----------

from ..objects import uint


class CommandObject:
    def __init__(self, data):
        self._data = data


class ValueCommandObject(CommandObject):
    def get(self):
        '''show value.'''
        return self._data


class SubscriptableCommandObject(CommandObject):
    def get(self, index: uint):
        '''get value from sequence by index.'''
        index = int(index)
        if index < len(self._data):
            return self._data[index]
        raise ValueError


class DictCommandObject(CommandObject):
    def get(self, key: str):
        '''get value from dict by key.'''
        return self._data.get(key, None)


class IterableCommandObject(CommandObject):
    def get(self, index: int):
        '''get value from sequence by index.'''
        for item in self._data:
            if index == 0:
                return item
            index -= 1
        raise ValueError


def wrap(obj):
    if isinstance(obj, (list, tuple)):
        return SubscriptableCommandObject(obj)
    elif isinstance(obj, dict):
        return DictCommandObject(obj)
    elif isinstance(obj, (int, float, str)):
        return ValueCommandObject(obj)
    raise NotImplementedError(type(obj))
