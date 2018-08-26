# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jasily.data.fullvars import fullvars

def test_fullvars_for_default():
    class Class:
        pass
    obj = Class()
    assert vars(obj) is obj.__dict__
    assert vars(obj) is vars(obj)
    assert fullvars(obj) is vars(obj)

def test_fullvars_for_slots():
    class Class:
        __slots__ = ('name', )

    obj = Class()
    proxy = fullvars(obj)
    # not cache:
    assert proxy is not fullvars(obj)
    assert not proxy
    obj.name = 'wtv'
    assert proxy
    assert proxy['name'] == 'wtv'
