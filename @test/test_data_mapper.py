# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily.data.mapper import from_dict, to_dict

class Model1:
    a: int
    b: str

    def f1(self):
        pass

    @property
    def f2(self):
        pass

class Model2:
    c: Model1

def test_from_dict():
    obj: Model2 = from_dict(Model2, {
        'c': {
            'a': 1,
            'b': '2'
        }
    })
    assert obj.c.a == 1
    assert obj.c.b == '2'

def test_to_dict():
    obj = Model2()
    obj.c = Model1()
    obj.c.a = 1
    assert to_dict(obj) == {
        'c': {
            'a': 1,
        }
    }
