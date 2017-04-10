#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------


class DataCommandWrapper:
    def __init__(self, data):
        self._data = data


class ValueCommandWrapper(DataCommandWrapper):
    def get(self):
        return self._data


class SubscriptableCommandWrapper(DataCommandWrapper):
    def get(self, idx: int):
        if 0 <= idx < len(self._data):
            return self._data[idx]
        raise ValueError


class DictCommandWrapper(DataCommandWrapper):
    def get(self, key: str):
        return self._data.get(key, None)


class IterableCommandWrapper(DataCommandWrapper):
    def get(self, idx: int):
        for item in self._data:
            if idx == 0:
                return item
            idx -= 1
        raise ValueError


def wrap(obj):
    if isinstance(obj, type):
        return obj()
    elif isinstance(obj, (list, tuple)):
        return SubscriptableCommandWrapper(obj)
    elif isinstance(obj, dict):
        return DictCommandWrapper(obj)
    elif isinstance(obj, (int, float, str)):
        return ValueCommandWrapper(obj)
    raise NotImplementedError
