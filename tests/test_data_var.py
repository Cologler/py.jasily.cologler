# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily.data.var import (
    get_object_var_factory
)

def assert_var_factory(cls, examples):
    for _ in range(5):
        obj = cls()
        vf = get_object_var_factory(obj)
        for k, v in examples:
            var = vf(k)
            assert not var.has_value
            var.set(v)
            assert var.has_value
            assert var.get() == v

def test_get_object_var_factory_for_dict():
    class A:
        pass

    assert_var_factory(A, [('ss', 1), (object(), 2), (int, 3)])

def test_get_object_var_factory_for_slots():
    class A:
        __slots__ = ('ss')
        pass

    assert_var_factory(A, [('ss', 1)])
