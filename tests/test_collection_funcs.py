# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from pytest import raises

from jasily.collection.funcs import CallableList

def test_call_list():
    ls = []
    with raises(TypeError):
        # pylint: disable=E1102
        ls()

def test_call_callable_list():
    ls = CallableList()
    # call empty
    assert ls() is None
    ls.append(lambda: 3)
    ls.append(lambda: 4)
    # return value should be return value of the last func
    assert ls() == 4
