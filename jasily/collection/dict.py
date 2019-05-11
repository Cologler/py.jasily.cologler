# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import Dict
from collections import defaultdict
from collections.abc import MutableMapping


class AttrDict:
    '''
    a dict with access key as attr.
    you can access inner dict by using `type(?).__data_dict__`

    the ctor as same as `dict()`.
    '''
    @classmethod
    def _make_cls(cls, data_dict):
        class _AttrDict(cls):
            def __getattribute__(self, name):
                try:
                    return data_dict[name]
                except KeyError:
                    raise AttributeError

            def __setattr__(self, name, value):
                data_dict[name] = value

            def __new__(*_args, **_kwargs):
                return object.__new__(*_args, **_kwargs)

            def __len__(self):
                return len(data_dict)

            def __contains__(self, name):
                return name in data_dict

        _AttrDict.__data_dict__ = data_dict # allow access using `type(?).__data_dict__`
        return _AttrDict

    def __new__(cls, *args, **kwargs):
        data_dict = dict(*args, **kwargs)
        return cls._make_cls(data_dict)()


class DefAttrDict(AttrDict):
    '''
    a dict with access key as attr.
    if the key does not exists, create by factory.

    the ctor as same as `defaultdict()`.
    '''

    def __new__(cls, factory):
        data_dict = defaultdict(factory)
        return cls._make_cls(data_dict)()


class AutoAttrDict(AttrDict):
    '''
    a dict with access key as attr.
    if the key does not exists, create by `AutoAttrDict`.
    '''

    def __new__(cls):
        data_dict = defaultdict(AutoAttrDict)
        return cls._make_cls(data_dict)()
