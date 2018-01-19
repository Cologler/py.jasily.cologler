#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from collections import KeysView, ValuesView, ItemsView, MutableMapping

_NO_VALUE = object()

class ContextDict(MutableMapping):
    '''context dict can override base_dict.'''

    def __init__(self, base_dict: dict, *args, **kwargs):
        if base_dict is None:
            raise ValueError('base_dict cannot be None')

        self._base_dict = base_dict
        self._data = dict(*args, **kwargs) # data maybe not empty.

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __getitem__(self, key):
        value = self._data.get(key, _NO_VALUE)
        if value is _NO_VALUE:
            value = self._base_dict[key]
        return value

    def __iter__(self):
        for k in self._data:
            yield k
        for k in self._base_dict:
            if k not in self._data:
                yield k

    def __len__(self):
        # base dict may change, so we cannot cache the size.
        d1 = self._data
        d2 = self._base_dict
        d1_len = len(d1)
        d2_len = len(d2)
        if d1_len > d2_len: # ensure d1 < d2
            d1, d2 = d2, d1
        total_size = d1_len + d2_len
        for k in d1:
            if k in d2:
                total_size -= 1
        return total_size

    def scope(self):
        '''create a scoped dict.'''
        return ContextDict(self)

    def __enter__(self):
        '''return a new context dict.'''
        return self.scope()

    def __exit__(self, *args):
        pass
