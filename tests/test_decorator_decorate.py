# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily.decorator.decorate import decorate
from functools import wraps

def decorater_ret_origin(target):
    @decorate(target)
    def func(*args, **kwargs):
        return target(*args, **kwargs)
    return func

def test_decorate_func():
    @decorater_ret_origin
    def abc():
        return 15
    assert not isinstance(abc, type)
    assert abc() == 15

def test_decorate_class():
    @decorater_ret_origin
    class C:
        pass

    assert isinstance(C, type)
    assert isinstance(C(), C)
