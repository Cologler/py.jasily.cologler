# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import Set
from collections.abc import MutableSet

from .comparer import IEqualityComparer, ObjectWrapper, ObjectComparer

class HashSet(MutableSet):
    def __init__(self, comparer: IEqualityComparer = None):
        self._comparer = comparer or ObjectComparer()
        self._data: Set[ObjectWrapper] = set()

    def add(self, value):
        return self._data.add(ObjectWrapper(self._comparer, value))

    def discard(self, value):
        return self._data.discard(ObjectWrapper(self._comparer, value))

    def __contains__(self, value):
        return ObjectWrapper(self._comparer, value) in self._data

    def __iter__(self):
        for wraped in self._data:
            yield wraped.unwrap()

    def __len__(self):
        return len(self._data)
