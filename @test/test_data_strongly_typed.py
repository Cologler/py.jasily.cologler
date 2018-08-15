# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import pytest

from jasily.data import make_strongly_typed

def test_make_strongly_typed():
    class SubExampleClass:
        sa: int
        sb: int = 1
        sc: int = 2

    class ExampleClass:
        a: int
        b: int = 1
        c: int = 2
        d: SubExampleClass
        e: SubExampleClass

    data = {
        'b': 3,
        'd': {
            'sb': 15
        }
    }

    obj: ExampleClass = make_strongly_typed(ExampleClass, data)

    # getter
    assert isinstance(obj, ExampleClass)
    with pytest.raises(AttributeError):
        _ = obj.a
    assert obj.b == 3
    assert obj.c == 2
    assert isinstance(obj.d, SubExampleClass)

    # setter
    obj.a = 10
    obj.b = 11
    obj.c = 12
    obj.d = SubExampleClass()
    assert obj.a == 10
    assert obj.b == 11
    assert obj.c == 12
    assert data == {'a': 10, 'b': 11, 'c': 12, 'd': {}}

    # setter sub class can be none
    obj.d = None
    assert data == {'a': 10, 'b': 11, 'c': 12, 'd': None}

    # assign with type check
    with pytest.raises(TypeError):
        obj.d = 1

    # with sub class
    obj.d = SubExampleClass()
    obj.d.sa = 12
    obj.d.sb = 'abc' # will not type check
    assert data == {'a': 10, 'b': 11, 'c': 12, 'd': {'sa': 12, 'sb': 'abc'}}

    # with del
    del obj.d.sa
    assert data == {'a': 10, 'b': 11, 'c': 12, 'd': {'sb': 'abc'}}
