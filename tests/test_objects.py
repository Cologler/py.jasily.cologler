#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from pytest import raises

from jasily.objects import uint, char, Key

def test_uint():
    with raises(ValueError):
        uint(-2)
    with raises(ValueError):
        uint(-1)
    assert uint(0) == 0
    assert uint(1) == 1

def test_char():
    with raises(ValueError):
        char('')
    with raises(ValueError):
        char('ss')
    with raises(ValueError):
        char('sss')
    with raises(ValueError):
        char(-5)

    assert char('5') == '5'
    assert char('s') == 's'
    assert char('S') == 'S'

    assert char(0) == chr(0)
    assert char(5) == chr(5)
    assert char(10) == chr(10)

def test_key():
    class Any:
        pass

    any_with_obj = Any()
    vars(any_with_obj)[object()] = 15
    with raises(TypeError):
        dir(any_with_obj)

    any_with_key = Any()
    vars(any_with_key)[Key()] = 15
    dir(any_with_key)
