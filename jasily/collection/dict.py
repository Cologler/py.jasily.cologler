# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import Dict
from collections.abc import MutableMapping

from .comparer import IComparer, Wrap, ObjectComparer

class Dictionary(MutableMapping):
    def __init__(self, comparer: IComparer = None):
        self._comparer = comparer or ObjectComparer()
        self._data: Dict[Wrap, object] = {}

    def __getitem__(self, key):
        return self._data[Wrap(self._comparer, key)]

    def __setitem__(self, key, value):
        self._data[Wrap(self._comparer, key)] = value

    def __delitem__(self, key):
        del self._data[Wrap(self._comparer, key)]

    def __iter__(self):
        for wraped_key in self._data:
            yield wraped_key.unwrap()

    def __len__(self):
        return len(self._data)
