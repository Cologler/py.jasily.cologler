# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from collections.abc import MutableMapping

class _SlotsProxy(MutableMapping):
    def __init__(self, obj, slotsnames):
        self._obj = obj
        self._slotsnames = frozenset(slotsnames)

    def __getitem__(self, key):
        return getattr(self._obj, key)

    def __setitem__(self, key, value):
        return setattr(self._obj, key, value)

    def __delitem__(self, key):
        return delattr(self._obj, key)

    def __iter__(self):
        for name in self._slotsnames:
            if hasattr(self._obj, name):
                yield name

    def __len__(self):
        return len(list(iter(self)))

def fullvars(obj):
    try:
        return vars(obj)
    except TypeError:
        pass

    # __slots__
    slotsnames = set()
    for cls in type(obj).__mro__:
        __slots__ = getattr(cls, '__slots__', None)
        if __slots__:
            slotsnames.update(__slots__)
    return _SlotsProxy(obj, slotsnames)
