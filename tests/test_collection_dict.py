# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from pytest import raises

from jasily.collection.dict import (
    AttrDict, DefAttrDict, AutoAttrDict
)

def _test_attr_dict(test_dict):
    size = len(test_dict)

    test_dict.__setattr__ = 1
    assert test_dict.__setattr__ == 1
    assert len(test_dict) == size + 1

    test_dict.__dict__ = 2
    assert test_dict.__dict__ == 2
    assert len(test_dict) == size + 2

    test_dict.__getattribute__ = 3
    assert test_dict.__getattribute__ == 3
    assert len(test_dict) == size + 3

    test_dict.__getattr__ = 4
    assert test_dict.__getattr__ == 4
    assert len(test_dict) == size + 4

def test_attr_dict():
    test_dict = AttrDict(c='c')

    # should can test type
    assert isinstance(test_dict, AttrDict)

    # should can init from kwargs
    assert test_dict.c == 'c'

    # should raise as KeyError
    assert 'd' not in test_dict
    assert not hasattr(test_dict, 'd')
    with raises(AttributeError):
        assert test_dict.d == 2 # `d` is not exists

    # should can add item
    test_dict.d = 4
    assert 'd' in test_dict
    assert test_dict.d == 4
    assert hasattr(test_dict, 'd')

    # access inner dict
    assert type(test_dict).__data_dict__['d'] == 4

    _test_attr_dict(test_dict)

def test_def_attr_dict():
    test_dict = DefAttrDict(list)
    assert isinstance(test_dict, DefAttrDict)
    assert isinstance(test_dict.x, list)
    _test_attr_dict(test_dict)

def test_auto_attr_dict():
    test_dict = AutoAttrDict()
    assert isinstance(test_dict, AutoAttrDict)
    assert isinstance(test_dict.a.b.c.d, AutoAttrDict)
    _test_attr_dict(test_dict)
