#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from pytest import raises

from jasily.objects import uint, char

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
